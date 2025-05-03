/*
 * mini_webserver.c
 *
 * A minimal multi-process HTTP server in C that serves only static HTML files from a single directory.
 *
 * Features:
 * - Serves only files with .html extension from a specified directory
 * - Only supports GET requests
 * - Listens on a configurable port (default: 8881)
 * - No directory traversal (.. is blocked)
 * - No MIME type detection (always serves text/html)
 * - Multi-process: forks a child for each client
 * - FIFO queue: logs each request path to a named pipe (mini_webserver_fifo)
 *
 * Usage:
 *   ./mini_webserver <directory> [port]
 *
 * Example:
 *   ./mini_webserver ./public_html 8881
 *
 * To test:
 *   curl http://localhost:8881/index.html
 *   cat mini_webserver_fifo   # to see the logged requests
 *
 * Build:
 *   gcc -Wall -Wextra -o mini_webserver mini_webserver.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
#include <signal.h>

#define DEFAULT_PORT 8881
#define BUF_SIZE 4096
#define MAX_PATH 512
#define FIFO_NAME "mini_webserver_fifo"

// Send a simple HTTP response with a given status and message
void send_response(int client_fd, int status, const char *msg) {
    char buf[BUF_SIZE];
    snprintf(buf, sizeof(buf),
        "HTTP/1.1 %d %s\r\nContent-Type: text/html\r\nContent-Length: %zu\r\nConnection: close\r\n\r\n%s",
        status, (status == 200 ? "OK" : (status == 404 ? "Not Found" : "Bad Request")), strlen(msg), msg);
    write(client_fd, buf, strlen(buf));
}

// Serve a static HTML file
void serve_file(int client_fd, const char *filepath) {
    int fd = open(filepath, O_RDONLY);
    if (fd < 0) {
        send_response(client_fd, 404, "<h1>404 Not Found</h1>");
        return;
    }
    struct stat st;
    if (fstat(fd, &st) < 0 || !S_ISREG(st.st_mode)) {
        close(fd);
        send_response(client_fd, 404, "<h1>404 Not Found</h1>");
        return;
    }
    char header[BUF_SIZE];
    snprintf(header, sizeof(header),
        "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %ld\r\nConnection: close\r\n\r\n",
        st.st_size);
    write(client_fd, header, strlen(header));
    ssize_t n;
    char buf[BUF_SIZE];
    while ((n = read(fd, buf, sizeof(buf))) > 0) {
        write(client_fd, buf, n);
    }
    close(fd);
}

// SIGCHLD handler to reap zombie children
void sigchld_handler(int signo) {
    (void)signo;
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main(int argc, char *argv[]) {
    if (argc < 2 || argc > 3) {
        fprintf(stderr, "Usage: %s <directory> [port]\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    char *base_dir = argv[1];
    int port = (argc == 3) ? atoi(argv[2]) : DEFAULT_PORT;
    if (port <= 0 || port > 65535) {
        fprintf(stderr, "Invalid port: %d\n", port);
        exit(EXIT_FAILURE);
    }
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);

    // Create FIFO for logging if it doesn't exist
    if (access(FIFO_NAME, F_OK) == -1) {
        if (mkfifo(FIFO_NAME, 0666) < 0) {
            perror("mkfifo");
            exit(EXIT_FAILURE);
        }
    }

    // Set up SIGCHLD handler to avoid zombies
    struct sigaction sa;
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    sigaction(SIGCHLD, &sa, NULL);

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        if (errno == EADDRINUSE) {
            fprintf(stderr, "Error: Port %d is already in use.\n", port);
        } else {
            perror("bind");
        }
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 5) < 0) {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    printf("mini_webserver: Serving %s on http://localhost:%d\n", base_dir, port);
    printf("mini_webserver: Logging requests to FIFO: %s\n", FIFO_NAME);

    while (1) {
        client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            close(client_fd);
            continue;
        }
        if (pid == 0) { // Child process
            close(server_fd); // Child doesn't need the listening socket
            char req[BUF_SIZE] = {0};
            read(client_fd, req, sizeof(req) - 1);
            // Only handle GET requests
            if (strncmp(req, "GET ", 4) != 0) {
                send_response(client_fd, 400, "<h1>400 Bad Request</h1>");
                close(client_fd);
                exit(0);
            }
            // Parse the requested path
            char path[MAX_PATH] = {0};
            sscanf(req + 4, "%s", path);
            // Block directory traversal
            if (strstr(path, "..")) {
                send_response(client_fd, 400, "<h1>400 Bad Request</h1>");
                close(client_fd);
                exit(0);
            }
            // Only serve .html files
            if (!strstr(path, ".html")) {
                send_response(client_fd, 404, "<h1>404 Not Found</h1>");
                close(client_fd);
                exit(0);
            }
            // Build the full file path
            char filepath[MAX_PATH];
            snprintf(filepath, sizeof(filepath), "%s/%s", base_dir, path+1); // skip leading /
            // Log the request path to the FIFO
            int fifo_fd = open(FIFO_NAME, O_WRONLY | O_NONBLOCK);
            if (fifo_fd >= 0) {
                dprintf(fifo_fd, "%s\n", path);
                close(fifo_fd);
            }
            serve_file(client_fd, filepath);
            close(client_fd);
            exit(0);
        } else {
            close(client_fd); // Parent doesn't need the connected socket
        }
    }
    close(server_fd);
    return 0;
} 
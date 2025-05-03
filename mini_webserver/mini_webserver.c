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
 * - Multi-process: pre-forks N children (default: 1, configurable)
 * - Logs each request path to access.log
 *
 * Usage:
 *   ./mini_webserver <directory> [port] [num_children]
 *
 * Example:
 *   ./mini_webserver ./public_html 8881 4
 *
 * To test:
 *   curl http://localhost:8881/index.html
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
#include <sys/wait.h>
#include <dirent.h>

#define DEFAULT_PORT 8881
#define BUF_SIZE 4096
#define MAX_PATH 512
#define LOG_FILE "access.log"
#define DEFAULT_CHILDREN 1

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

// Send a directory listing as an HTML page (only .html files)
void send_directory_listing(int client_fd, const char *dirpath, const char *req_path) {
    DIR *dir = opendir(dirpath);
    if (!dir) {
        send_response(client_fd, 404, "<h1>404 Not Found</h1>");
        return;
    }
    char html[BUF_SIZE * 2];
    snprintf(html, sizeof(html), "<html><head><title>Directory listing for %s</title></head><body><h1>Directory listing for %s</h1><ul>", req_path, req_path);
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            const char *name = entry->d_name;
            size_t len = strlen(name);
            if (len > 5 && strcmp(name + len - 5, ".html") == 0) {
                char link[MAX_PATH];
                if (strcmp(req_path, "/") == 0) {
                    snprintf(link, sizeof(link), "/%s", name);
                } else {
                    snprintf(link, sizeof(link), "%s/%s", req_path, name);
                }
                strncat(html, "<li><a href=\"", sizeof(html) - strlen(html) - 1);
                strncat(html, link, sizeof(html) - strlen(html) - 1);
                strncat(html, "\">", sizeof(html) - strlen(html) - 1);
                strncat(html, name, sizeof(html) - strlen(html) - 1);
                strncat(html, "</a></li>", sizeof(html) - strlen(html) - 1);
            }
        }
    }
    closedir(dir);
    strncat(html, "</ul></body></html>", sizeof(html) - strlen(html) - 1);
    send_response(client_fd, 200, html);
}

// SIGCHLD handler to reap zombie children
void sigchld_handler(int signo) {
    (void)signo;
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

void child_loop(int server_fd, char *base_dir) {
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    while (1) {
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }
        char req[BUF_SIZE] = {0};
        read(client_fd, req, sizeof(req) - 1);
        // Only handle GET requests
        if (strncmp(req, "GET ", 4) != 0) {
            send_response(client_fd, 400, "<h1>400 Bad Request</h1>");
            close(client_fd);
            continue;
        }
        // Parse the requested path
        char path[MAX_PATH] = {0};
        sscanf(req + 4, "%s", path);
        // Block directory traversal
        if (strstr(path, "..")) {
            send_response(client_fd, 400, "<h1>400 Bad Request</h1>");
            close(client_fd);
            continue;
        }
        // Build the full file path
        char filepath[MAX_PATH];
        snprintf(filepath, sizeof(filepath), "%s/%s", base_dir, path+1); // skip leading /
        // Log the request path to access.log
        FILE *logf = fopen(LOG_FILE, "a");
        if (logf) {
            fprintf(logf, "%s\n", path);
            fclose(logf);
        }
        struct stat st;
        if (stat(filepath, &st) == 0 && S_ISREG(st.st_mode) && strstr(path, ".html")) {
            // Serve the file if it exists and is .html
            serve_file(client_fd, filepath);
        } else {
            // If it's a directory or file doesn't exist, serve directory listing
            char dirpath[MAX_PATH];
            if (stat(filepath, &st) == 0 && S_ISDIR(st.st_mode)) {
                // Requested path is a directory
                snprintf(dirpath, sizeof(dirpath), "%s/%s", base_dir, path+1);
            } else {
                // If root or file not found, try to list the directory containing the file
                if (strcmp(path, "/") == 0) {
                    snprintf(dirpath, sizeof(dirpath), "%s", base_dir);
                } else {
                    // Remove the last component to get the directory
                    char *last_slash = strrchr(path, '/');
                    if (last_slash && last_slash != path) {
                        size_t dirlen = last_slash - path;
                        char subdir[MAX_PATH];
                        strncpy(subdir, path + 1, dirlen - 1); // skip leading /
                        subdir[dirlen - 1] = '\0';
                        snprintf(dirpath, sizeof(dirpath), "%s/%s", base_dir, subdir);
                    } else {
                        snprintf(dirpath, sizeof(dirpath), "%s", base_dir);
                    }
                }
            }
            send_directory_listing(client_fd, dirpath, path);
        }
        close(client_fd);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2 || argc > 4) {
        fprintf(stderr, "Usage: %s <directory> [port] [num_children]\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    char *base_dir = argv[1];
    int port = (argc >= 3) ? atoi(argv[2]) : DEFAULT_PORT;
    int num_children = (argc == 4) ? atoi(argv[3]) : DEFAULT_CHILDREN;
    if (port <= 0 || port > 65535) {
        fprintf(stderr, "Invalid port: %d\n", port);
        exit(EXIT_FAILURE);
    }
    if (num_children <= 0 || num_children > 128) {
        fprintf(stderr, "Invalid number of children: %d\n", num_children);
        exit(EXIT_FAILURE);
    }
    int server_fd;
    struct sockaddr_in server_addr;

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
    printf("mini_webserver: Logging requests to %s\n", LOG_FILE);
    printf("mini_webserver: Forking %d child process(es)\n", num_children);

    // Pre-fork children
    for (int i = 0; i < num_children; ++i) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            exit(EXIT_FAILURE);
        }
        if (pid == 0) {
            // Child process: handle requests
            child_loop(server_fd, base_dir);
            exit(0);
        }
    }
    // Parent: just wait forever
    while (1) pause();
    close(server_fd);
    return 0;
} 
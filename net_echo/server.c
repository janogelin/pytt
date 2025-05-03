#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUF_SIZE 1024

/*
 * Simple TCP/UDP Echo Server
 *
 * Listens on a port and protocol specified by the user, accepts incoming TCP connections
 * or UDP datagrams, and echoes back any data received from the client.
 *
 * Usage: ./server <tcp|udp> <port>
 */

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <tcp|udp> <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int is_tcp = 0;
    if (strcmp(argv[1], "tcp") == 0) {
        is_tcp = 1;
    } else if (strcmp(argv[1], "udp") == 0) {
        is_tcp = 0;
    } else {
        fprintf(stderr, "Protocol must be 'tcp' or 'udp'\n");
        exit(EXIT_FAILURE);
    }

    int port = atoi(argv[2]);
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    char buffer[BUF_SIZE];
    ssize_t n;

    // Create socket (SOCK_STREAM for TCP, SOCK_DGRAM for UDP)
    if ((sockfd = socket(AF_INET, is_tcp ? SOCK_STREAM : SOCK_DGRAM, 0)) < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Prepare the sockaddr_in structure for the server
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    // Bind the socket to the specified port
    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    if (is_tcp) {
        // TCP mode
        if (listen(sockfd, 5) < 0) {
            perror("listen");
            close(sockfd);
            exit(EXIT_FAILURE);
        }
        printf("TCP echo server listening on port %d...\n", port);
        while (1) {
            int client_fd = accept(sockfd, (struct sockaddr *)&client_addr, &client_addr_len);
            if (client_fd < 0) {
                perror("accept");
                continue;
            }
            printf("TCP client connected.\n");
            while ((n = read(client_fd, buffer, BUF_SIZE)) > 0) {
                write(client_fd, buffer, n); // Echo back
            }
            printf("TCP client disconnected.\n");
            close(client_fd);
        }
    } else {
        // UDP mode
        printf("UDP echo server listening on port %d...\n", port);
        while (1) {
            n = recvfrom(sockfd, buffer, BUF_SIZE, 0, (struct sockaddr *)&client_addr, &client_addr_len);
            if (n < 0) {
                perror("recvfrom");
                continue;
            }
            // Echo back to sender
            sendto(sockfd, buffer, n, 0, (struct sockaddr *)&client_addr, client_addr_len);
        }
    }
    close(sockfd);
    return 0;
} 
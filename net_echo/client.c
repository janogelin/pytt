#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUF_SIZE 1024

/*
 * Simple TCP/UDP Echo Client
 *
 * Connects to a server at a given IP and port using TCP or UDP, sends a message,
 * and prints the echoed response from the server.
 *
 * Usage: ./client <tcp|udp> <ip> <port> <message>
 */

int main(int argc, char *argv[]) {
    // Check for correct number of arguments
    if (argc != 5) {
        fprintf(stderr, "Usage: %s <tcp|udp> <ip> <port> <message>\n", argv[0]);
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

    char *ip = argv[2];
    int port = atoi(argv[3]);
    char *message = argv[4];
    int sockfd;
    struct sockaddr_in server_addr;
    char buffer[BUF_SIZE];
    ssize_t n;

    // Create a socket (SOCK_STREAM for TCP, SOCK_DGRAM for UDP)
    if ((sockfd = socket(AF_INET, is_tcp ? SOCK_STREAM : SOCK_DGRAM, 0)) < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Prepare the sockaddr_in structure for the server
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    if (inet_pton(AF_INET, ip, &server_addr.sin_addr) <= 0) {
        fprintf(stderr, "Invalid address/ Address not supported\n");
        exit(EXIT_FAILURE);
    }

    if (is_tcp) {
        // TCP mode: connect to the server
        if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            perror("connect");
            close(sockfd);
            exit(EXIT_FAILURE);
        }
        // Send the message to the server
        write(sockfd, message, strlen(message));
        // Receive the echoed message from the server
        n = read(sockfd, buffer, BUF_SIZE-1);
        if (n > 0) {
            buffer[n] = '\0';
            printf("Echoed from server: %s\n", buffer);
        } else {
            printf("No response from server.\n");
        }
    } else {
        // UDP mode: sendto/recvfrom
        socklen_t addrlen = sizeof(server_addr);
        if (sendto(sockfd, message, strlen(message), 0, (struct sockaddr *)&server_addr, addrlen) < 0) {
            perror("sendto");
            close(sockfd);
            exit(EXIT_FAILURE);
        }
        n = recvfrom(sockfd, buffer, BUF_SIZE-1, 0, NULL, NULL);
        if (n > 0) {
            buffer[n] = '\0';
            printf("Echoed from server: %s\n", buffer);
        } else {
            printf("No response from server.\n");
        }
    }

    close(sockfd); // Close the socket
    return 0;
} 
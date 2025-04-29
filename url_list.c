#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define the structure for a node in the linked list
typedef struct URLNode {
    char *url;
    struct URLNode *next;
} URLNode;

// Function to create a new node
URLNode* create_node(const char *url) {
    URLNode *node = (URLNode*)malloc(sizeof(URLNode));
    if (node == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    
    // Allocate memory for the URL string and copy it
    node->url = strdup(url);
    if (node->url == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        free(node);
        exit(1);
    }
    
    node->next = NULL;
    return node;
}

// Function to add a node to the end of the list
void append_node(URLNode **head, const char *url) {
    URLNode *new_node = create_node(url);
    
    if (*head == NULL) {
        *head = new_node;
        return;
    }
    
    URLNode *current = *head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
}

// Function to free the entire list
void free_list(URLNode *head) {
    URLNode *current = head;
    while (current != NULL) {
        URLNode *next = current->next;
        free(current->url);
        free(current);
        current = next;
    }
}

// Function to print the list
void print_list(URLNode *head) {
    URLNode *current = head;
    int count = 1;
    
    while (current != NULL) {
        printf("%d. %s\n", count++, current->url);
        current = current->next;
    }
}

int main() {
    FILE *file;
    char line[1024];  // Buffer for reading lines
    URLNode *head = NULL;
    
    // Open the file
    file = fopen("urls.txt", "r");
    if (file == NULL) {
        fprintf(stderr, "Error: Could not open file urls.txt\n");
        return 1;
    }
    
    // Read URLs line by line
    while (fgets(line, sizeof(line), file)) {
        // Remove newline character if present
        size_t len = strlen(line);
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
        }
        
        // Skip empty lines
        if (strlen(line) > 0) {
            append_node(&head, line);
        }
    }
    
    // Close the file
    fclose(file);
    
    // Print the list
    printf("URLs in the list:\n");
    print_list(head);
    
    // Free the list
    free_list(head);
    
    return 0;
} 
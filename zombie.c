#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t child_pid;

    printf("Parent process (PID: %d) starting...\n", getpid());

    // Create a child process
    child_pid = fork();

    if (child_pid < 0) {
        perror("fork failed");
        exit(1);
    }

    if (child_pid == 0) {
        // Child process
        printf("Child process (PID: %d) created\n", getpid());
        printf("Child process exiting...\n");
        exit(0);  // Child exits immediately
    } else {
        // Parent process
        printf("Parent process created child with PID: %d\n", child_pid);
        printf("Parent process sleeping for 30 seconds...\n");
        printf("During this time, run 'ps aux | grep zombie' in another terminal to see the zombie process\n");
        sleep(30);  // Parent sleeps, not calling wait()
        
        // After sleep, parent will exit and the zombie will be cleaned up
        printf("Parent process exiting...\n");
    }

    return 0;
} 
CC = gcc
CFLAGS = -Wall -Wextra
TARGET = mini_webserver

all: $(TARGET)

$(TARGET): mini_webserver.c
	$(CC) $(CFLAGS) -o $(TARGET) mini_webserver.c

clean:
	rm -f $(TARGET) mini_webserver_fifo 
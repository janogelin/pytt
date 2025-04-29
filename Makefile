CC = gcc
CFLAGS = -Wall -Wextra -g
TARGET = url_list

all: $(TARGET)

$(TARGET): url_list.c
	$(CC) $(CFLAGS) -o $(TARGET) url_list.c

clean:
	rm -f $(TARGET)

.PHONY: all clean 
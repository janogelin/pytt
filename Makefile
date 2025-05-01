CC = gcc
CFLAGS = -Wall -Wextra

all: zombie

zombie: zombie.c
	$(CC) $(CFLAGS) -o zombie zombie.c

clean:
	rm -f zombie 
# net_echo

A simple TCP/UDP echo server and client in C.

## Build

```sh
cd net_echo
make
```

## Usage

### Server
Start the echo server on a specific port and protocol (e.g., TCP on 54321):
```
./server <tcp|udp> <port>
```
Examples:
```
./server tcp 54321
./server udp 54321
```
The server will listen for incoming TCP connections or UDP datagrams on the specified port. For each client/message, it will echo back any data received. The server prints connection/disconnection messages for TCP and echoes datagrams for UDP.

### Client
Connect to the server at a given IP and port using TCP or UDP, send a message, and print the echoed response:
```
./client <tcp|udp> <ip> <port> <message>
```
Examples:
```
./client tcp 127.0.0.1 54321 "Hello, TCP echo server!"
./client udp 127.0.0.1 54321 "Hello, UDP echo server!"
```
The client will connect (TCP) or send a datagram (UDP) to the server, send the message, and print the echoed response from the server. If the server is not running or the connection fails, an error will be shown.

## Test

Run the test script (requires bash):
```sh
./test_echo.sh
```
This script will:
- Start the server in the background (TCP)
- Run the client to send a test message (TCP)
- Check that the echoed message matches the sent message
- Stop the server

For UDP, you can manually test with:
```sh
./server udp 54321 &
./client udp 127.0.0.1 54321 "Hello, UDP!"
```

## Coverage

To check code coverage (requires `gcov`):

```sh
make clean
make CFLAGS="-Wall -Wextra -fprofile-arcs -ftest-coverage"
./server tcp 54321 &
SERVER_PID=$!
sleep 1
./client tcp 127.0.0.1 54321 testmsg
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null || true
gcov server.c client.c
```

This will generate `server.c.gcov` and `client.c.gcov` with coverage info.

## Notes
- The server must be started before running the client.
- The server handles one TCP client at a time (for simplicity).
- Both programs print errors to stderr if something goes wrong.
- The test script is a basic functional test for TCP; for UDP, test manually as shown above. 
# mini_webserver

A minimal multi-process HTTP server in C that serves only static HTML files from a single directory.

## Features
- Serves only `.html` files from a specified directory
- Only supports GET requests
- Listens on port 8080
- Blocks directory traversal (.. is blocked)
- Always serves `text/html` MIME type
- Multi-process: forks a child for each client
- FIFO queue: logs each request path to a named pipe (`mini_webserver_fifo`)

## Build

```sh
cd mini_webserver
make
```

## Usage

Start the server, serving files from a directory (e.g., `public_html`):

```sh
./mini_webserver <directory>
```

Example:
```sh
./mini_webserver public_html
```

Visit [http://localhost:8080/index.html](http://localhost:8080/index.html) in your browser or use curl:

```sh
curl http://localhost:8080/index.html
```

## FIFO Logging

Each request path is logged to a named pipe (`mini_webserver_fifo`). You can view the log in real time with:

```sh
tail -f mini_webserver_fifo
```

## Test

A test script is provided:

```sh
./test_webserver.sh
```

This script will:
- Build the server
- Start the server in the background
- Make a request to `/index.html`
- Check that the HTML content is served
- Check that the request path is logged to the FIFO
- Stop the server

## Notes
- The server is single-port (8080) and single-root (one directory).
- Only `.html` files are served; all other requests return 404.
- The server is for demonstration/educational use and is not secure for production. 
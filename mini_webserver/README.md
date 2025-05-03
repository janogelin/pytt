# mini_webserver

> **WARNING: This server is for demonstration and educational purposes only. It is NOT secure and must NOT be used for any production or internet-facing deployment.**

A minimal multi-process HTTP server in C that serves only static HTML files from a single directory.

## Features
- Serves only `.html` files from a specified directory
- Only supports GET requests
- Listens on port 8881 by default (can be set via command line)
- Blocks directory traversal (.. is blocked)
- Always serves `text/html` MIME type
- Multi-process: forks a child for each client
- Logs each request path to `access.log`

## Build

```sh
cd mini_webserver
make
```

## Usage

Start the server, serving files from a directory (e.g., `public_html`):

```sh
./mini_webserver <directory> [port]
```

Example:
```sh
./mini_webserver public_html
```

Visit [http://localhost:8881/index.html](http://localhost:8881/index.html) in your browser or use curl:

```sh
curl http://localhost:8881/index.html
```

## Logging

Each request path is logged to `access.log` in the current directory. You can view the log in real time with:

```sh
tail -f access.log
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
- Check that the request path is logged to `access.log`
- Stop the server

## Docker

You can run mini_webserver using Docker from Docker Hub:

```sh
docker pull jangelinav/mini_webserver:latest
docker run -p 8881:8881 jangelinav/mini_webserver:latest
```

This will serve files from the default `public_html` directory on port 8881.

## Notes
- The server is single-port (default 8881) and single-root (one directory).
- Only `.html` files are served; all other requests return 404.
- The server is for demonstration/educational use and is not secure for production. 
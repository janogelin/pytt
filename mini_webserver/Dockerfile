# Use Alpine Linux for build stage
FROM alpine:latest AS build

RUN apk add --no-cache gcc make musl-dev
WORKDIR /src
COPY . .
RUN make

# Create a minimal runtime image with Alpine
FROM alpine:latest
WORKDIR /srv
COPY --from=build /src/mini_webserver /usr/local/bin/mini_webserver
COPY public_html ./public_html
EXPOSE 8881
ENTRYPOINT ["/usr/local/bin/mini_webserver", "./public_html", "8881"] 
# Use the latest Ubuntu image
FROM alpine:latest

RUN mkdir app
# Set the working directory
WORKDIR /app


# Install necessary packages
RUN apk update && \
	apk add --no-cache gcc make libc-dev linux-headers netcat-openbsd
# Copy the source code to the container
COPY . /app/

# Compile the server code
RUN gcc -pthread server.c queue.c -o server

# Expose the port the server will run on
EXPOSE 50000

# Command to run the server
CMD ["./server", "0.0.0.0"]

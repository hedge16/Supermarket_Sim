# Use the latest Ubuntu image
FROM alpine:latest

RUN mkdir app
# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apk update &&  \
    apk add gcc libc-dev
# Copy the source code to the container
COPY . /app/

# Compile the server code
RUN gcc server.c queue.c -o server -lpthread

# Expose the port the server will run on
EXPOSE 50000

# Command to run the server
CMD ["./server", "0.0.0.0"]
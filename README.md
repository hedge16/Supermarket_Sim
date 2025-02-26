# Supermarket Sim
This is a client-server supermarket simulation. The server is written in C and the client is written in Python. The server is multithreaded and uses a thread pool to handle multiple clients. The client is a simple command line interface that allows the user to interact with the server.
# How to run
To run the server, navigate to the server directory and run the following commands:
``` docker-compose up --build ``` <br>
To run the client, navigate to the client directory and run the following commands:
``` python3 client.py ```
# Features
- The server can handle multiple clients at once
- The number of clients the server can handle is configurable
- The server can handle multiple requests from the same client at once
- The client can add items to the cart
- The client can view the cart
- The client can remove items from the cart
- The client can checkout


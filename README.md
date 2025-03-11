# Supermarket Sim
This is a client-server supermarket simulation. The server is written in C and the client is written in Python. The server is multithreaded and uses a thread pool to handle multiple clients. The client is a simple Ui-based application that allows the user to interact with the server.
# Project structure
```
.
├── README.md
├── client
│   ├── cart.py
│   ├── cart_ui.ui
│   ├── client.py
│   ├── client_ui.py
│   └── client_ui.ui
├── doc
│   └── documentazione.pdf
└── server
    ├── CMakeLists.txt
    ├── Dockerfile
    ├── client.c
    ├── colors.h
    ├── docker-compose.yml
    ├── queue.c
    ├── queue.h
    └── server.c
```
# How to run
To run the server, navigate to the server directory and run the following commands:
``` 
docker-compose up --build 
``` 
To run the client, navigate to the client directory and run the following commands:
``` 
pip install PyQt5
python3 client.py 
``` 
In the server directory there is also a C program to test the connection of multiple clients at once (configured to 25). To use it run:
```
gcc client.c -o client
./client
```


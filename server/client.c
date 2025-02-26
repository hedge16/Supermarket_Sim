#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

typedef struct {
    char *name;
    int price;
} Product;

typedef struct {
    int id;
    int time;
    int nProducts;
    Product *products;
} Customer;

int main(int argc, char* argv[]) {
    // Crea una socket e si connette al server
    int clientSocket;
    int i;
    struct sockaddr_in serverAddr;
    const int PORT = 50000;

    for (i = 0; i < 25; i++) {
        clientSocket = socket(AF_INET, SOCK_STREAM, 0);
        if (clientSocket < 0) {
            perror("Errore nella creazione del socket");
            exit(1);
        }
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(PORT);
        serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
        if (connect(clientSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr)) < 0) {
            perror("Errore nella connessione al server");
            exit(1);
        }
        Product products[] = {{"Prodotto", i+10}};
        Customer client = {i, i+3, products, 1};// Assegna un ID univoco al cliente
        send(clientSocket, &client, sizeof(Customer), 0);
        close(clientSocket);
    }
    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "queue.h"
#include "colors.h"

#define MAX_CUSTOMERS 10
#define E 5
#define NUM_CASSE 3
#define PORT 50000

typedef struct {
    int id;
    char *name;
    int price;
} Product;

typedef struct {
    int id;
    int time;
    int nProducts;
    Product *products;
} Customer;

typedef struct {
    int fixedTime;
    Queue customerInCassa;
    pthread_mutex_t mutexCassa;
    pthread_cond_t condCodaVuota;
} Cassa;


Queue customerInStore;
Queue customerInQueue;
Cassa cassa[NUM_CASSE];
pthread_mutex_t mutexStore = PTHREAD_MUTEX_INITIALIZER;
int currentCustomers = 0;

void * cassiere(void * arg) {
    const int numCassa = *(int *) arg;
    // Ciclo infinito per servire i clienti
    printf("Cassa %d aperta.\n", numCassa);
    while (1) {
        // Attende che ci siano clienti in coda
        pthread_mutex_lock(&cassa[numCassa].mutexCassa);
        while (isEmpty(&cassa[numCassa].customerInCassa)) {
            pthread_cond_wait(&cassa[numCassa].condCodaVuota, &cassa[numCassa].mutexCassa);
        }
        Customer *client = dequeue(&cassa[numCassa].customerInCassa);
        pthread_mutex_unlock(&cassa[numCassa].mutexCassa);
        // Simula il pagamento
        if (client) {
            printf(COLOR_MAGENTA "Il cliente %d è in fase di pagamento alla cassa %d\n" COLOR_RESET, client->id, numCassa);
            sleep(cassa[numCassa].fixedTime + client->nProducts);
            printf(COLOR_GREEN "Il cliente %d ha terminato il pagamento ed esce dal supermercato.\n" COLOR_RESET, client->id);
            // Libera la memoria e aggiorna il numero di clienti presenti nel supermercato
            free(client);
            // Aggiorna il numero di clienti presenti nel supermercato
            pthread_mutex_lock(&mutexStore);
            currentCustomers--;
            pthread_mutex_unlock(&mutexStore);
        }
    }
}

void * spesa(void * arg) {
    Customer *client = (Customer *) arg;
    printf(COLOR_MAGENTA "Cliente %d fa acquisti per %d secondi.\n" COLOR_RESET, client->id, client->time);
    sleep(client->time);
    if (client->nProducts > 0) {
        const int chosenCassa = rand() % NUM_CASSE;
        pthread_mutex_lock(&cassa[chosenCassa].mutexCassa);
        enqueue(&cassa[chosenCassa].customerInCassa, client);
        pthread_cond_signal(&cassa[chosenCassa].condCodaVuota);;
        pthread_mutex_unlock(&cassa[chosenCassa].mutexCassa);
        printf(COLOR_CYAN "Cliente %d si mette in fila alla cassa %d.\n" COLOR_RESET, client->id, chosenCassa);
    } else {
        printf("Cliente %d non ha acquistato nulla ed esce dal supermercato.\n", client->id);
        free(client->products);
        free(client);
        pthread_mutex_lock(&mutexStore);
        currentCustomers--;
        pthread_mutex_unlock(&mutexStore);
    }
    pthread_exit(0);
}

void * client(void * arg) {
    // Riceve il cliente e lo mette in coda nel supermercato
    const int clientSocket = *(int *) arg;
    Customer *customer = malloc(sizeof(Customer));
    recv(clientSocket, customer, sizeof(Customer), 0);

    pthread_mutex_lock(&mutexStore);
    if (currentCustomers < MAX_CUSTOMERS) {
        enqueue(&customerInStore, customer);
        currentCustomers++;
        printf(COLOR_BLUE "Il cliente %d è entrato nel supermercato.\n" COLOR_RESET, customer->id);
        pthread_t spesaThread;
        pthread_create(&spesaThread, NULL, spesa, (void *) customer);
        pthread_detach(spesaThread);
    } else {
        enqueue(&customerInQueue, customer);
        printf(COLOR_RED"Il supermercato è pieno, il cliente %d è in attesa.\n" COLOR_RESET, customer->id);
    }
    pthread_mutex_unlock(&mutexStore);
    pthread_exit(0);
}

void *direttore(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutexStore);
        // Se il numero di clienti scende sotto la soglia, ne fa entrare altri E
        if (currentCustomers <= MAX_CUSTOMERS - E && !isEmpty(&customerInQueue)) {
            int clientiDaFarEntrare = E;
            while (clientiDaFarEntrare > 0 && !isEmpty(&customerInQueue)) {
                Customer *client = dequeue(&customerInQueue);
                if (client->nProducts == 0) {
                    printf("Il cliente %d non ha acquistato nulla ed esce immediatamente.\n", client->id);
                    free(client);
                } else {
                    enqueue(&customerInStore, client);
                    currentCustomers++;
                    printf(COLOR_BLUE"Il cliente %d è entrato nel supermercato.\n"COLOR_RESET, client->id);
                    pthread_t clientThread;
                    pthread_create(&clientThread, NULL, spesa, client);
                    pthread_detach(clientThread);
                }
                clientiDaFarEntrare--;
            }
        }
        pthread_mutex_unlock(&mutexStore);
        sleep(1); // Controlla periodicamente
    }
}

void * connection(void * arg) {
    // Crea un socket , si mette in ascolto e crea un nuovo thread per ogni richiesta
    const char *ip = (char *) arg;
    //int clientSocket; // Descrittori dei socket
    struct sockaddr_in serverAddr, clientAddr; // Indirizzi del server e del client
    socklen_t addrSize = sizeof(struct sockaddr_in); // Dimensione dell'indirizzo
    const int serverSocket = socket(AF_INET, SOCK_STREAM, 0); // Creazione del socket
    if (serverSocket < 0) {
        perror("Errore nella creazione del socket");
        exit(1);
    }
    serverAddr.sin_family = AF_INET; // Dominio del socket
    serverAddr.sin_port = htons(PORT); // Porta del socket
    serverAddr.sin_addr.s_addr = inet_addr(ip); // Indirizzo del server
    if (bind(serverSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr)) < 0) {
        perror("Errore nel binding del socket");
        exit(1);
    }
    if (listen(serverSocket, MAX_CUSTOMERS) < 0) {
        perror("Errore nell'ascolto del socket");
        exit(1);
    }
    printf("Server in ascolto sulla porta %d...\n", PORT);
    while (1) {
        int clientSocket = accept(serverSocket, (struct sockaddr *) &clientAddr, &addrSize);
        printf("Nuova connessione accettata\n");
        if (clientSocket < 0) {
            perror("Errore nell'accettazione del client");
            exit(1);
        }
        pthread_t clientThread;
        pthread_create(&clientThread, NULL, client, (void *) &clientSocket);
        pthread_detach(clientThread);
        usleep(500);
    }
}


int main(int argc, char* argv[]) {

    if (argc < 2) {
        printf("Usage : ./server <ip>\n");
        exit(1);
    }
    const char *ip = argv[1];
    pthread_t casse[NUM_CASSE];
    pthread_t connectionThread, direttoreThread;
    int i;
    srand(time(NULL)); // Initialize random number generator once
    for (i = 0; i < NUM_CASSE; i++) {
        createQueue(&cassa[i].customerInCassa, sizeof(Customer)); // Inizializzazione delle code delle casse
        int *cassaIndex = malloc(sizeof(int));
        *cassaIndex = i;
        cassa[i].fixedTime = rand() % 5 + 1;
        pthread_create(&casse[i], NULL, cassiere, (void *) cassaIndex);// Creazione dei thread delle casse
        pthread_mutex_init(&cassa[i].mutexCassa, NULL); // Inizializzazione dei mutex delle casse
        pthread_cond_init(&cassa[i].condCodaVuota, NULL); // Inizializzazione delle variabile condizione delle casse
        pthread_detach(casse[i]); // Detach dei thread delle casse
    }
    pthread_create(&connectionThread, NULL, connection, (void *) ip);// Creazione del thread di connessione
    pthread_create(&direttoreThread, NULL, direttore, NULL); // Creazione del thread del direttore
    createQueue(&customerInStore, sizeof(Customer)); // Inizializzazione della coda del supermercato
    createQueue(&customerInQueue, sizeof(Customer)); // Inizializzazione della coda dei clienti in attesa
    pthread_join(connectionThread, NULL); // Attende la terminazione del thread di connessione
    // Distruzione dei mutex prima di terminare
    for (i = 0; i < NUM_CASSE; i++) {
        pthread_mutex_destroy(&cassa[i].mutexCassa);
    }
    return 0;
}
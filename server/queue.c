#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "queue.h"

// Crea una nuova coda per dati di una data dimensione
void createQueue(Queue *q, size_t dataSize) {
	q->front = q->rear = 0;
	q->dataSize = dataSize;
}

// Controlla se la coda è vuota
int isEmpty(Queue *q) {
	return q->front == q->rear;
}

// Controlla se la coda è piena
int isFull(Queue *q) {
	return (q->rear + 1) % MAX == q->front;
}

// Inserisce un elemento nella coda
void enqueue(Queue *q, void *item) {
	if (isFull(q)) {
		printf("Errore: Coda piena!\n");
		return;
	}

	// Alloca memoria per il nuovo elemento
	q->data[q->rear] = malloc(q->dataSize);
	if (!q->data[q->rear]) {
		printf("Errore: Allocazione di memoria fallita!\n");
		return;
	}

	// Copia i dati nel nuovo elemento
	memcpy(q->data[q->rear], item, q->dataSize);
	q->rear = (q->rear + 1) % MAX;
}

// Estrae un elemento dalla coda
void *dequeue(Queue *q) {
	if (isEmpty(q)) {
		printf("Errore: Coda vuota!\n");
		return NULL;
	}

	void *item = q->data[q->front];
	q->front = (q->front + 1) % MAX;

	return item;
}

// Stampa una coda di interi
void printQueueInt(Queue *q) {
	printf("Queue: ");
	for (int i = q->front; i != q->rear; i = (i + 1) % MAX) {
		printf("%d ", *(int *)q->data[i]);
	}
	printf("\n");
}

// Pulisce la memoria allocata
void clearQueue(Queue *q) {
	while (!isEmpty(q)) {
		free(dequeue(q));
	}
}

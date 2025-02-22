#ifndef QUEUE_H
#define QUEUE_H

#define MAX 20

typedef struct {
    void *data[MAX]; // Array di puntatori generici
    int front, rear;
    size_t dataSize; // Dimensione di ogni elemento
} Queue;

void createQueue(Queue *q, size_t dataSize);
void enqueue(Queue *q, void *item);
void *dequeue(Queue *q);
int isEmpty(Queue *q) ;
int isFull(Queue *q);
void clearQueue(Queue *q);

#endif

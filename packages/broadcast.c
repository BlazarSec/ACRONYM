#include <errno.h>
#include <fcntl.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <sys/stat.h>

#include "broadcast.h"

typedef struct {
    broadcast_msg_t buffer[BROADCAST_QUEUE_SIZE];
    int head;
    int tail;
} broadcast_msg_queue_t;

//file globals
broadcast_msg_queue_t queue;
sem_t queue_sem;
pthread_mutex_t queue_mut     = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t broadcast_mut = PTHREAD_MUTEX_INITIALIZER;

void* broadcast_handler(void* param) {
    while (1) {
        //wait for a message to be queued
        sem_wait(&queue_sem);
        //dont let further circ buff modifications happen yet
        pthread_mutex_lock(&queue_mut);
        //update the circ buff and consume the tail
        if (queue.tail != queue.head) {
            broadcast_msg(queue.buffer[queue.tail]);
            int next = queue.tail + 1;
            if (next == BROADCAST_QUEUE_SIZE) {
                next = 0;
            }
            queue.tail = next;
        }
        pthread_mutex_unlock(&queue_mut);
    }
    return 0;
}

void broadcast_init() {
    queue.head = 0;
    queue.tail = 0;
    if (!sem_init(&queue_sem, 0, 0)) {
        perror("sem_init");
    }
    //spin up the broadcast msg consuming thread
    pthread_t th_id;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_create(&th_id, &attr, broadcast_handler, 0);
    pthread_detach(th_id);
}

void broadcast_close() {
    sem_close(&queue_sem);
    pthread_mutex_destroy(&queue_mut);
    pthread_mutex_destroy(&broadcast_mut);
}

void broadcast_msg(const broadcast_msg_t msg) {
    //only broadcast one at a time
    pthread_mutex_lock(&broadcast_mut);
    for (int j = 0; j < broadcast_type_totals[msg.type]; ++j) {
        broadcast_callbacks[msg.type][j](&msg);
    }
    pthread_mutex_unlock(&broadcast_mut);
}

int broadcast_queue_msg(const broadcast_msg_t msg) {
    pthread_mutex_lock(&queue_mut);
    int next;
    next = queue.head + 1;
    if (next == BROADCAST_QUEUE_SIZE) {
        next = 0;
    }

    if (next == queue.tail) {
        pthread_mutex_unlock(&queue_mut);
        return -1; //queue full
    }
    queue.buffer[next] = msg;
    queue.head         = next;

    pthread_mutex_unlock(&queue_mut);
    sem_post(&queue_sem);
    return 0; //data pushed
}

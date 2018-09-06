#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <time.h>

#include "../broadcast.h"
#include "timer.h"

void* tick(void* param(void)) {
    struct timespec tim, tim2;
    tim.tv_sec  = 1;
    tim.tv_nsec = 0;
    while (1) {
        if (nanosleep(&tim, &tim2)) {
            perror("nanosleep failed!");
            break;
        }
        //TODO broadcast the timer message
    }
    return 0;
}

void timer_init() {
    void* ret;
    pthread_t th_id;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_create(th_id, &attr, tick, 0);
    pthread_detach(th_id);
}

#pragma once

#ifndef BROADCAST_QUEUE_SIZE
#define BROADCAST_QUEUE_SIZE 10
#endif


typedef struct {
    //TODO generate all types based on the number of unique event strings
    int type;
    union {
        int flag;
        void* data;
    } extra;
} broadcast_msg_t;

//TODO write the init that waits on CV signals to consume the queue and broadcast the async signals, probably a seperate thread

//blocking call avoid use
//  ie for critical messages
void broadcast_msg(const broadcast_msg_t msg);
//non blocking
//
int broadcast_queue_msg(const broadcast_msg_t msg);

extern int broadcast_total_types;
extern int *broadcast_type_totals;
extern void (***broadcast_callbacks)(const broadcast_msg_t* msg);

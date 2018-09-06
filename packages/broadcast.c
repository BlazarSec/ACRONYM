#include "broadcast.h"

typedef struct {
    broadcast_msg_t[BROADCAST_QUEUE_SIZE] buffer;
    int head;
    int tail;
} broadcast_msg_queue_t;

broadcast_msg_queue_t queue;

void broadcast_msg(const broadcast_msg_t msg) {
    //TODO aquire lock
    for (int j = 0; j < broadcast_type_totals[msg.type]; ++j) {
        broadcast_callbacks[msg.type][j](&msg);
    }
    //TODO release lock
}

int broadcast_queue_msg(const broadcast_msg_t msg) {
    //TODO aquire lock
    int next;
    next = queue.head + 1;
    if (next > BROADCAST_QUEUE_SIZE) {
        next = 0;
    }

    if (next == queue.tail) {
        //TODO release lock
        return -1; //queue full
    }
    queue.buffer[next] = msg;
    queue.head = next;

    //TODO release lock
    //signal CV of pending data
    return 0; //data pushed
}

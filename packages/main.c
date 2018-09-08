#include "broadcast.h"
#include "stdio.h"
#include "stdlib.h"
void test(const broadcast_msg_t* msg) {
    puts("test");
}

void (***broadcast_callbacks)(const broadcast_msg_t*);
int broadcast_total_types = 1;
int* broadcast_type_totals;

int main(int argc, char** argv) {
    //TODO generate mallocs and frees from selected packages
    broadcast_init();

    broadcast_callbacks = malloc(sizeof(void (**)(const broadcast_msg_t*))*broadcast_total_types);

    broadcast_type_totals = malloc(sizeof(int)*broadcast_total_types);
    //TODO generate out totals for subscribers

    for (int i = 0; i < broadcast_total_types; ++i) {
        broadcast_callbacks[i] = malloc(sizeof(void (*)(const broadcast_msg_t*))*broadcast_type_totals[i]);
        //TODO insert handler assertions to types in the callback
        //broadcast_callbacks[i][0] = &handler
    }


    broadcast_msg_t msg;
    msg.type = 0;

    broadcast_msg(msg);

    broadcast_close();

    while (1)
        usleep(1000);

    for (int i = 0; i < broadcast_total_types; ++i) {
        free(broadcast_callbacks[i]);
    }
    free(broadcast_callbacks);
}

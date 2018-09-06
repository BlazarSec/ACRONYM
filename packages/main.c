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
    broadcast_callbacks = malloc(sizeof(void (**)(const broadcast_msg_t*)));
    broadcast_callbacks[0] = malloc(sizeof(void (*)(const broadcast_msg_t*)));
    broadcast_callbacks[0][0] = &test;

    broadcast_type_totals = malloc(sizeof(int));
    broadcast_type_totals[0] = 1;

    broadcast_msg_t msg;
    msg.type = 0;

    broadcast_msg(msg);
}

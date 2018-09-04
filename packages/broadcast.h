#pragma once

typedef struct broadcast_msg_t {
    int type;
    union {
        int flag;
        void* data;
    } extra;
} broadcast_msg_t;

void broadcast_msg(const broadcast_msg_t msg);

extern int broadcast_total_types;
extern int *broadcast_type_totals;
extern void (***broadcast_callbacks)(const broadcast_msg_t* msg);

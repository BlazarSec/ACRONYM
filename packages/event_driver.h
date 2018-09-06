#pragma once

typedef struct event_message {
    int type;
    void * extra;
} event_message;

void broadcast_event_message(event_message message);


//void (type_callback)(const event_message *)[];

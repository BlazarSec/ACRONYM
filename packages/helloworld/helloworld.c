#include "helloworld.h"
#include <stdio.h>

void helloworld_init() {
    puts("hello world");
}

void helloworld_handler(const broadcast_msg_t * msg) {
    puts("hi!");
}

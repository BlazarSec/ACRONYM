#include "broadcast.h"

void broadcast_msg(const broadcast_msg_t msg) {
    for (int j = 0; j < broadcast_type_totals[msg.type]; ++j) {
        broadcast_callbacks[msg.type][j](&msg);
    }
}

#include "stdio.h"

int countdown_break() {
    static int i = 10;
    printf("%d...\n", i);
    return --i;
}

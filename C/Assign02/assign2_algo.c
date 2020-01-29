#include "assign2_algo.h"


int str2bin(char *str) {

    char *ptr = str;
    int i;

    for(; *ptr != 0; ++ptr)
    {

        /* perform bitwise AND for every bit of the character */
        for(i = 7; i >= 0; --i) {
            if (*ptr & 1 << i){
                 putchar('1');
             } else{
                 putchar('0');
             }
        }

        putchar(' ');
    }

    putchar('\n');




    return 0;
}

int main(int argc, char *argv[])
{
    if(argc < 2){
         return 0; /* no input string */
    }

    str2bin(argv[1]);
    
    return 0;
}

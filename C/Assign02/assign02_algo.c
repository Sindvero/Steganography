#include "assign02_algo.h"


int str2bin(char *str) {

    char *ptr = str;
    int i;
    char str1[] = "1";
    char str0[] = "0";
    FILE *fp = fopen("output_file.txt", "a");

    for(; *ptr != 0; ++ptr)
    {

        /* perform bitwise AND for every bit of the character */
        for(i = 7; i >= 0; --i) {
            if (*ptr & 1 << i){
                 putchar('1');
                 fwrite(str1, 1, sizeof(str1), fp);
             } else{
                 putchar('0');
                 fwrite(str0, 1, sizeof(str0), fp);
             }
        }
        fwrite(" ", 1, sizeof(" "), fp);
        putchar(' ');
    }

    fclose(fp);
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

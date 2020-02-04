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

    FILE *fp = fopen(argv[1], "r");
    fseek(fp, 0, SEEK_END);
    long fsize = ftell(fp);
    fseek(fp, 0, SEEK_SET); 
    char *buffer = malloc(fsize + 1);

    fread(buffer, 1, fsize, fp);

    fclose(fp);

    str2bin(buffer);
    
    return 0;
}

#include "assign02_algo.h"


int str2bin(char *str) {

    char *ptr = str;
    int i;
    char str1 = '1';
    char str0 = '0';
    FILE *fp = fopen("output_file.txt", "a");

    for(; *ptr != 0; ++ptr)
    {

        /* perform bitwise AND for every bit of the character */
        for(i = 7; i >= 0; i--) {
            if (*ptr & 1 << i){
                 putchar('1');
                 fwrite(&str1, 1, sizeof(char), fp);
             } else{
                 putchar('0');
                 fwrite(&str0, 1, sizeof(char), fp);
             }
        }
        // putchar(' ');
    }

    fclose(fp);
    putchar('\n');
    return 0;
}
void binaryToString(char* input, char* output){

    char binary[9] = {0}; // initialize string to 0's

    // copy 8 bits from input string
    for (int i = 0; i < 8; i ++){
        binary[i] = input[i];    
    }

    *output  = strtol(binary,NULL,2); // convert the byte to a long, using base 2 
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
    // printf("%s\n", buffer);
    str2bin(buffer);

    FILE *fp1 = fopen("output_file.txt", "r");
    fseek(fp1, 0, SEEK_END);
    long fsize1 = ftell(fp1);
    fseek(fp1, 0, SEEK_SET); 
    char buffer1[fsize1];
    fread(&buffer1, 1, fsize1, fp1);
    fclose(fp1);
    printf("%s\n", buffer1);


    FILE *fp2 = fopen("test_return.txt", "a");

    char outputStr[fsize1]; // initialize string to 0's

    int iterations = strlen(buffer1) / 8; // get the # of bytes

    // convert each byte into an ascii value
    for (int i = 0; i < iterations; i++){
        binaryToString(&buffer1[i*8], &outputStr[i]);
    }

    printf("%s\n", outputStr); // print the resulting string
    fwrite(outputStr, 1, fsize, fp2);
    fclose(fp2);
    
    return 0;
}

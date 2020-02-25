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
                 fwrite(&str1, 1, sizeof(char), fp);
             } else{
                 fwrite(&str0, 1, sizeof(char), fp);
             }
        }
        
        // putchar(' ');
    }

    fclose(fp);
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

    // Transform ASCII to binary
    FILE *fpInput = fopen(argv[1], "r");
    fseek(fpInput, 0, SEEK_END);
    long fsize = ftell(fpInput);
    fseek(fpInput, 0, SEEK_SET); 
    char *bufferInput = malloc(fsize + 1);

    fread(bufferInput, 1, fsize, fpInput);

    fclose(fpInput);

    str2bin(bufferInput);

    // Transform back to ASCII
    FILE *fpBin = fopen("output_file.txt", "r");
    fseek(fpBin, 0, SEEK_END);
    long fsize1 = ftell(fpBin);
    fseek(fpBin, 0, SEEK_SET); 
    char buffer1[fsize1];
    fread(&buffer1, 1, fsize1, fpBin);
    fclose(fpBin);


    FILE *fpOutput = fopen("output_return.txt", "a");

    char outputStr[fsize1]; // initialize string to 0's

    int iterations = strlen(buffer1) / 8; // get the # of bytes

    // convert each byte into an ascii value
    for (int i = 0; i < iterations; i++){
        binaryToString(&buffer1[i*8], &outputStr[i]);
    }

    fwrite(outputStr, 1, fsize, fpOutput);
    fclose(fpOutput);
    
    return 0;
}

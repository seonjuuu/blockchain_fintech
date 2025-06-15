#include <stdio.h>
#include <inttypes.h>
#include <string.h>

uint8_t Rkey[11][16];  

#define AES128

#ifdef AES128
int Nr = 10; //number round
int Nb = 16; //number byte
int Nw = 4; //number words
#endif
#include <stdio.h>
#include <inttypes.h>
#include <string.h>


uint8_t Rkey[11][16];  

#define AES128'

//CTR 변화
#ifdef AES128
#define Nr 10  
#define Nb 16  
#define Nw 4   
#endif
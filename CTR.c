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

//CTR 구조체
typedef struct _AES_ALG_INFO {
	uint8_t Buffer[Nb];
	uint32_t BufLen;
	uint8_t ChainVar[Nb];
}_AES_ALG_INFO;
typedef _AES_ALG_INFO AES_ALG_INFO[1];

#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#define SHA256_BLOCKLEN 64
#define SHA256_DIGESTLEN 32

//C구조체
typedef struct _SHA256_CTX {
	uint8_t data[SHA256_BLOCKLEN]; //8bit*64개 = 512bit (one block)
	uint32_t datalen; //bytelen
	uint64_t bitlen; //data bitlen
	uint32_t ChainVar[8];
}_SHA256_CTX;
typedef _SHA256_CTX SHA256_CTX[1];
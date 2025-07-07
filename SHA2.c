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

#define ROTR_ULONG(x, n) ((uint32_t)((x) >> (n)) | (uint32_t)((x) << (32 - (n))))
#define ROTL_ULONG(x, n) ((uint32_t)((x) << (n)) | (uint32_t)((x) >> (32 - (n))))

//SHA-2 Functions
#define CH(x,y,z) ((x&y)^((~x)&z))
#define Maj(x,y,z) ((x&y)^(x&z)^(y&z))

#define S0(x)  (ROTR_ULONG(x,2)^ROTR_ULONG(x,13)^ROTR_ULONG(x,22))
#define S1(x)  (ROTR_ULONG(x,6)^ROTR_ULONG(x,11)^ROTR_ULONG(x,25))

#define sig0(x) (ROTR_ULONG(x,7)^ROTR_ULONG(x,18)^((x)>>3)) 
#define sig1(x) (ROTR_ULONG(x,17)^ROTR_ULONG(x,19)^((x)>>10))

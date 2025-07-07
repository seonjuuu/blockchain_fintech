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

const uint32_t SHA256_K[64] = { 0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
	0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
	0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
	0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
	0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
	0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
	0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
	0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
	0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
	0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
	0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2 };


uint32_t ChainVar[8] = { 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19 };  //초기값

//초기화
void sha256_init(SHA256_CTX ctx)
{
	ctx->datalen = 0;
	ctx->bitlen = 0;
	ctx->ChainVar[0] = 0x6a09e667;
	ctx->ChainVar[1] = 0xbb67ae85;
	ctx->ChainVar[2] = 0x3c6ef372;
	ctx->ChainVar[3] = 0xa54ff53a;
	ctx->ChainVar[4] = 0x510e527f;
	ctx->ChainVar[5] = 0x9b05688c;
	ctx->ChainVar[6] = 0x1f83d9ab;
	ctx->ChainVar[7] = 0x5be0cd19;

}
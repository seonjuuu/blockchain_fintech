#include <stdio.h>
#include <inttypes.h>

#define SHA256_BLOCKLEN 64
#define SHA256_DIGESTLEN 32

#define ROTR_ULONG(x, n) ((uint32_t)((x) >> (n)) | (uint32_t)((x) << (32 - (n))))
#define ROTL_ULONG(x, n) ((uint32_t)((x) << (n)) | (uint32_t)((x) >> (32 - (n))))

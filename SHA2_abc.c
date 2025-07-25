#include <stdio.h>
#include <inttypes.h>

#define SHA256_BLOCKLEN 64
#define SHA256_DIGESTLEN 32

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

void main() 
{
	uint8_t msg1[] = {"abc"};
	uint8_t hash1[SHA256_DIGESTLEN] = { 0xba,0x78,0x16,0xbf,0x8f,0x01,0xcf,0xea,0x41,0x41,0x40,0xde,0x5d,0xae,0x22,0x23,0xb0,0x03,0x61,0xa3,0x96,0x17,0x7a,0x9c,0xb4,0x10,0xff,0x61,0xf2,0x00,0x15,0xad };  //해시 결과값
    uint8_t msglen = 24; //24는 16bit가 아닌 8bit

    // 전처리(preprocessing)
	uint8_t mpad[SHA256_BLOCKLEN] = { 0, }; //8bit가 64개
    uint32_t W[SHA256_BLOCKLEN] = { 0, }; //32bit 16개(t가 0~15)와 연산(16~63) => 총 64개(SHA256_BLOCKLEN)
    uint32_t a, b, c, d, e, f, g, h, T1, T2;

	mpad[0] = msg1[0];
    mpad[1] = msg1[1];
    mpad[2] = msg1[2];
    mpad[3] = 0x80; //1붙이고 뒤는 0으로 패딩 즉, 10000000..
    mpad[63] = msglen; //길이 정보

	//기본 블록 해시
	for (int i = 0; i < 16; i++)
	{
		W[i] = (mpad[4 * i] << 24) ^ (mpad[4 * i + 1] << 16) ^ (mpad[4 * i + 2] << 8) ^ (mpad[4 * i + 3]);
	}
	for (int i = 16; i < 64; i++)
	{
		W[i] = sig1(W[i - 2]) + W[i - 7] + sig0(W[i - 15]) + W[i - 16];
	}

	a = ChainVar[0];
	b = ChainVar[1];
	c = ChainVar[2];
	d = ChainVar[3];
	e = ChainVar[4];
	f = ChainVar[5];
	g = ChainVar[6];
	h = ChainVar[7];

	// SHA256-one block
	for (int t = 0; t < 64; t++)
	{
		T1 = h + S1(e) + CH(e, f, g) + SHA256_K[t] + W[t];
		T2 = S0(a) + Maj(a, b, c);
		h = g;
		g = f;
		f = e;
		e = d + T1;
		d = c;
		c = b;
		b = a;
		a = T1 + T2;

	}

	ChainVar[0] = a + ChainVar[0];
	ChainVar[1] = b + ChainVar[1];
	ChainVar[2] = c + ChainVar[2];
	ChainVar[3] = d + ChainVar[3];
	ChainVar[4] = e + ChainVar[4];
	ChainVar[5] = f + ChainVar[5];
	ChainVar[6] = g + ChainVar[6];
	ChainVar[7] = h + ChainVar[7];

	//Hash value
	for (int i = 0; i < 8; i++)
	{
		printf("Ch[%d] : %x \n", i,ChainVar[i]);
	}

}
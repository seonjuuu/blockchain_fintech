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

// 전처리과정 함수
void sha256_transform(SHA256_CTX ctx, const uint8_t* mgs)
{
	uint32_t W[SHA256_BLOCKLEN] = { 0, }; //32bit 16개(t가 0~15)와 연산(16~63) => 총 64개(SHA256_BLOCKLEN)
    uint32_t a, b, c, d, e, f, g, h, T1, T2;

    //기본 블록 해시
	for (int i = 0; i < 16; i++)
	{
		W[i] = (mgs[4 * i] << 24) ^ (mgs[4 * i + 1] << 16) ^ (mgs[4 * i + 2] << 8) ^ (mgs[4 * i + 3]);
	}
	for (int i = 16; i < 64; i++)
	{
		W[i] = sig1(W[i - 2]) + W[i - 7] + sig0(W[i - 15]) + W[i - 16];
	}

	a = ctx->ChainVar[0];
	b = ctx->ChainVar[1];
	c = ctx->ChainVar[2];
	d = ctx->ChainVar[3];
	e = ctx->ChainVar[4];
	f = ctx->ChainVar[5];
	g = ctx->ChainVar[6];
	h = ctx->ChainVar[7];

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

	ctx->ChainVar[0] = a + ctx->ChainVar[0];
	ctx->ChainVar[1] = b + ctx->ChainVar[1];
	ctx->ChainVar[2] = c + ctx->ChainVar[2];
	ctx->ChainVar[3] = d + ctx->ChainVar[3];
	ctx->ChainVar[4] = e + ctx->ChainVar[4];
	ctx->ChainVar[5] = f + ctx->ChainVar[5];
	ctx->ChainVar[6] = g + ctx->ChainVar[6];
	ctx->ChainVar[7] = h + ctx->ChainVar[7];

	//Hash value
	for (int i = 0; i < 8; i++)
	{
		printf("transform_Ch[%d] : %x \n", i,ChainVar[i]);
	}
}
// memcpy 사용법
// memcpy (결과, 복사하고 싶은것, 길이)
// Message를 ctx->data에 복사  => memcy(ctc->data, Message, 64) = memcy(ctx->data, Message, SHA256_BLOCKLEN)

// MegLen => byte 단위 >= 64
void sha256_update(SHA256_CTX ctx, uint8_t* Message, uint32_t MsgLen)
{
	ctx->datalen = MsgLen;
	while (ctx->datalen >= SHA256_BLOCKLEN)
	{
		//ctx->data에 meg 복사
		memcpy(ctx->data, Message, SHA256_BLOCKLEN);        //ctc->data에 Message를 64byte만큼 복사, 512bit를 끊는것
		//sha256 tranform 
		sha256_transform(ctx, ctx->data);

		Message += SHA256_BLOCKLEN;                       //while문을 새롭게 한번 더 돌때 복사하는 Message의 시작부분 증가해야함, 시작포인터 증가(64byte 증가시킨부분부터 복사해서 transform)
		ctx->datalen -= SHA256_BLOCKLEN;                  //ctx->datalen에 남은 메시지가 저장됨
		ctx->bitlen += 512;

	}
	// 남은 메시지 블록 복사 => final에서 패딩 
	memcpy(ctx->data, Message, ctx->datalen);

}

void sha256_final(uint8_t* hash, SHA256_CTX ctx)
{
	int i = ctx->datalen;
	if (ctx->datalen <56) 
	{
		ctx->data[i++] = 0x80;     //1byte는 0x80
		while(i<56)
			ctx->data[i++] = 0x00;
	}
	else
	{
		ctx->data[i++] = 0x80;    //길이가 56byte가 넘어도 0x80는 무조건 붙여줘야함 !!
		while (i < 64)
			ctx->data[i++] = 0x00;
		sha256_transform(ctx, ctx->data);
		memset(ctx->data, 0, 56);                         //'ctx->data'배열의 처음 56byte를 0으로 설정(초기화)

	}
	//길이정보(64bit=8byte)//hash
	ctx->bitlen += ctx->datalen * 8;                     //bitlen의 길이정보에 나머지 블록 길이의 정보도 저장
	// 64bit 변수 -> 8bit 8개
	ctx->data[63] = (ctx->bitlen) & 0xff;                 //0xff=마지막 8bit를 끊어낸다(최하위 8bit는 [63]에 저장)
	ctx->data[62] = (ctx->bitlen >> 8) & 0xff;
	ctx->data[61] = (ctx->bitlen >> 16) & 0xff;
	ctx->data[60] = (ctx->bitlen >> 24) & 0xff;
	ctx->data[59] = (ctx->bitlen >> 32) & 0xff;
	ctx->data[58] = (ctx->bitlen >> 40) & 0xff;
	ctx->data[57] = (ctx->bitlen >> 48) & 0xff;
	ctx->data[56] = (ctx->bitlen >> 56) & 0xff;

	sha256_transform(ctx, ctx->data);                    //나머지블록의 transform

	//최종 해시값 hash[]//ChainVar[0] = hash[0] hash[1] hash[2] hash[3]
	for (int i = 0; i < 8; i++)  //hash[0](8bit)~hash[31] : 각각의 hash가 32개 모여서 총 256bit(해시값) 
	{
		hash[4 * i] = (ctx->ChainVar[i] >> 24) & 0xff;  
		hash[4 * i+1] = (ctx->ChainVar[i] >> 16) & 0xff;
		hash[4 * i+2] = (ctx->ChainVar[i] >> 8) & 0xff;
		hash[4 * i+3] = (ctx->ChainVar[i]) & 0xff;	
	}
}

void SHA256(uint8_t* Digest, uint8_t* Message, uint32_t MsgLen)
{
	SHA256_CTX ctx;
	sha256_init(ctx);
	sha256_update(ctx, Message, MsgLen);
	sha256_final(Digest, ctx);
}
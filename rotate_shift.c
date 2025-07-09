#include <stdio.h>
#define DEBUG

// rotate shift - 왼쪽
void main()
{
	unsigned char a = 0x23;                      // unsigned 사용하기
	unsigned char b = 0;

#ifdef DEBUG
	b = (a & 0xe0) >> 5;                        // 0xe0 : e0 = 1110 0000 -> 앞에 있는 3비트만 남기기 위해서 1110 0000과 a를 &(and) -> and(&)는 1과 더해야 자기자신이 나오므로
	a = (a << 3) ^ b;                           // ^ = XOR 연산자 부호 -> XOR는 0이랑 더하면 자기 자신이 나옴
	printf("rotate shift : %02x \n",a);
#endif
}

// rotate shift - 오른쪽

void main()
{
	unsigned char a = 0xb3, out = 0;
	unsigned char t0 = 0, t1 = 0;

	t0 = a & 0x07;   //_ _ _ _ _ * * *
	t0 = t0 << 5;   //* * * _ _ _ _ _
	t1 = a >> 3; // _ _ _ * * * * *

	out = t0 ^ t1;

	printf("out : %02x \n", out);
}
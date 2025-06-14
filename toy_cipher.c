#include <stdio.h>
#include <inttypes.h>
#include <string.h>

uint8_t F(uint8_t finput)
{
    uint8_t finput1 = finput<<2;
    finput1 = (finput1 + finput)%(1<<8);
    uint8_t finput2 = finput<<4;
    finput2 = (finput1+finput2)%(1<<8);

    return finput2;
}

uint16_t toy_cipher(uint16_t pt , uint16_t key)
{
    pt = pt^key;

    uint8_t R1 = (pt&0xff);
    uint8_t L1 = (pt>>8)&0xff;
    //printf("%02x %02x\n",L1,R1);

    uint8_t R2 = L1^F(R1);
    uint8_t L2 = R1;

    uint8_t L3 = L2^F(R2);
    uint8_t R3 = R2;
    //printf("%02x %02x\n",L3,R3);


    uint16_t ct = (L3 << 8) ^ R3;

    return ct;

}

int main() {
    uint16_t plaintext = 0x5A3C;
    uint16_t key = 0x7B28;

    printf("%x",toy_cipher(plaintext, key));

}
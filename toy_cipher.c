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
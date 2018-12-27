// c++ -O2 solve.cpp -o solve
// Generated with Tardis https://github.com/paiv/aoc2018
#include <stdint.h>
#include <stdio.h>

typedef uint8_t u8;
typedef uint32_t u32;


int main(int argc, char const *argv[]) {
    u32 r0 = 0, r1 = 0, r2 = 0, r3 = 0, r4 = 0, r5 = 0;
    r5 = 123;
    do {
        r5 &= 456;
    } while (r5 != 72);
    r5 = 0;
    do {
        r3 = r5 | 65536;
        r5 = 7586220;
    ln8:
        r1 = r3 & 255;
        r5 += r1;
        r5 &= 16777215;
        r5 *= 65899;
        r5 &= 16777215;
        if (256 <= r3) {
            r1 = 0;
    ln18:
            r4 = r1 + 1;
            r4 *= 256;
            if (r4 <= r3) {
                r1 += 1;
                goto ln18;
            }
            r3 = r1;
            goto ln8;
        }
    // } while (r5 != r0);
    } while (false);

    printf("part1: %d\n", r5);

    return 0;
}

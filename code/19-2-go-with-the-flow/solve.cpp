// c++ -O2 solve.cpp -o solve
// Generated with Tardis https://github.com/paiv/aoc2018
#include <stdint.h>
#include <stdio.h>

typedef uint8_t u8;
typedef uint32_t u32;


int main(int argc, char const *argv[]) {
    u32 r0 = 1, r1 = 0, r2 = 0, r3 = 0, r4 = 0, r5 = 0;

    r2 += 2;
    r2 *= r2;
    r2 *= 19;
    r2 *= 11;
    r5 += 4;
    r5 *= 22;
    r5 += 16;
    r2 += r5;
    if (r0) {
        r5 = 27;
        r5 *= 28;
        r5 += 29;
        r5 *= 30;
        r5 *= 14;
        r5 *= 32;
        r2 += r5;
        r0 = 0;
    }

    r4 = 1;
    do {
        // r1 = 1;
        r1 = r2 / r4;
        do {
            r5 = r4 * r1;
            if (r5 == r2) {
                r0 += r4;
            }
        //     r1 += 1;
        // } while (r1 <= r2);
        } while (false);
        r4 += 1;
    } while (r4 <= r2);

    printf("%d\n", r0);

    return 0;
}

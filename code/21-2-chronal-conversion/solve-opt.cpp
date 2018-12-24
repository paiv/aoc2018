// c++ -O2 solve.cpp -o solve
#include <stdint.h>
#include <stdio.h>
#include <unordered_set>

using namespace std;

typedef uint8_t u8;
typedef uint32_t u32;


int main(int argc, char const *argv[]) {
    unordered_set<u32> visited;
    u32 last_seen = 0;

    u32 r0 = 0, r1 = 0, r2 = 0, r3 = 0, r4 = 0, r5 = 0;
    //   0: seti 123 0 5
    src0: r5 = 123;
    //   1: bani 5 456 5
    src1: r5 = r5 & 456;
    //   2: eqri 5 72 5
    src2: r5 = r5 == 72 ? 1 : 0;
    //   3: addr 5 2 2
    src3: if (!r5)
    //   4: seti 0 0 2
    src4: goto src1;
    //   5: seti 0 9 5
    src5: r5 = 0;
    //   6: bori 5 65536 3
    src6: r3 = r5 | 65536;
    //   7: seti 7586220 4 5
    src7: r5 = 7586220;
    //   8: bani 3 255 1
    src8: r1 = r3 & 255;
    //   9: addr 5 1 5
    src9: r5 = r5 + r1;
    //  10: bani 5 16777215 5
    src10: r5 = r5 & 16777215;
    //  11: muli 5 65899 5
    src11: r5 = r5 * 65899;
    //  12: bani 5 16777215 5
    src12: r5 = r5 & 16777215;
    //  13: gtir 256 3 1
    src13: r1 = 256 > r3 ? 1 : 0;
    //  14: addr 1 2 2
    src14: if (!r1)
    //  15: addi 2 1 2
    src15: goto src17;
    //  16: seti 27 9 2
    src16: goto src28;
    //  17: seti 0 9 1
    src17: r1 = 0;
    //  18: addi 1 1 4
    src18: r4 = r1 + 1;
    //  19: muli 4 256 4
    src19: r4 = r4 * 256;
    //  20: gtrr 4 3 4
    src20: r4 = r4 > r3 ? 1 : 0;
    //  21: addr 4 2 2
    src21: if (!r4)
    //  22: addi 2 1 2
    src22: goto src24;
    //  23: seti 25 4 2
    src23: goto src26;
    //  24: addi 1 1 1
    src24: r1 = r1 + 1;
    //  25: seti 17 2 2
    src25: goto src18;
    //  26: setr 1 6 3
    src26: r3 = r1;
    //  27: seti 7 8 2
    src27: goto src8;
    //  28: eqrr 5 0 1
    src28: r1 = r5 == r0 ? 1 : 0;

    if (visited.find(r5) != visited.end()) {
        goto srcexit;
    }
    last_seen = r5;
    visited.insert(last_seen);

    //  29: addr 1 2 2
    src29: if (!r1)
    //  30: seti 5 0 2
    src30: goto src6;
    srcexit:

    printf("part2: %d\n", last_seen);

    return 0;
}

// c++ -O2 solve.cpp -o solve
#include <stdint.h>
#include <stdio.h>
#include <unordered_set>


using namespace std;


typedef enum opcodes {
    addi,
    addr,
    bani,
    bori,
    eqri,
    eqrr,
    gtir,
    gtrr,
    muli,
    seti,
    setr,
} opcodes;


typedef uint8_t u8;
typedef uint32_t u32;


static const u8 rip = 2;

static const u32
prog[][4] = {
    {seti, 123, 0, 5},
    {bani, 5, 456, 5},
    {eqri, 5, 72, 5},
    {addr, 5, 2, 2},
    {seti, 0, 0, 2},
    {seti, 0, 9, 5},
    {bori, 5, 65536, 3},
    {seti, 7586220, 4, 5},
    {bani, 3, 255, 1},
    {addr, 5, 1, 5},
    {bani, 5, 16777215, 5},
    {muli, 5, 65899, 5},
    {bani, 5, 16777215, 5},
    {gtir, 256, 3, 1},
    {addr, 1, 2, 2},
    {addi, 2, 1, 2},
    {seti, 27, 9, 2},
    {seti, 0, 9, 1},
    {addi, 1, 1, 4},
    {muli, 4, 256, 4},
    {gtrr, 4, 3, 4},
    {addr, 4, 2, 2},
    {addi, 2, 1, 2},
    {seti, 25, 4, 2},
    {addi, 1, 1, 1},
    {seti, 17, 2, 2},
    {setr, 1, 6, 3},
    {seti, 7, 8, 2},
    {eqrr, 5, 0, 1},
    {addr, 1, 2, 2},
    {seti, 5, 0, 2},
};


static inline void
dispatch(const u32* instr, u32* mem) {
    switch (instr[0]) {
        case addi:
            mem[instr[3]] = mem[instr[1]] + instr[2];
            break;
        case addr:
            mem[instr[3]] = mem[instr[1]] + mem[instr[2]];
            break;
        case bani:
            mem[instr[3]] = mem[instr[1]] & instr[2];
            break;
        case bori:
            mem[instr[3]] = mem[instr[1]] | instr[2];
            break;
        case eqri:
            mem[instr[3]] = mem[instr[1]] == instr[2];
            break;
        case eqrr:
            mem[instr[3]] = mem[instr[1]] == mem[instr[2]];
            break;
        case gtir:
            mem[instr[3]] = instr[1] > mem[instr[2]];
            break;
        case gtrr:
            mem[instr[3]] = mem[instr[1]] > mem[instr[2]];
            break;
        case muli:
            mem[instr[3]] = mem[instr[1]] * instr[2];
            break;
        case seti:
            mem[instr[3]] = instr[1];
            break;
        case setr:
            mem[instr[3]] = mem[instr[1]];
            break;
    }
}


int main(int argc, char const *argv[]) {
    const int progn = sizeof(prog) / sizeof(prog[0]);
    u32 mem[6] = {};
    unordered_set<u32> visited;
    u32 res = 0;

    for (int ip = 0; ip >= 0 && ip < progn; ip++) {
        if (ip == 29) {
            if (visited.find(mem[5]) != visited.end()) {
                break;
            }
            res = mem[5];
            visited.insert(res);
        }

        mem[rip] = ip;
        dispatch(prog[ip], mem);
        ip = mem[rip];
    }

    printf("%d\n", res);

    return 0;
}

// c++ -O2 solve.cpp -o solve
#include <stdint.h>
#include <stdio.h>


typedef enum opcodes {
    addi,
    addr,
    eqrr,
    gtrr,
    muli,
    mulr,
    seti,
    setr,
} opcodes;


typedef uint8_t u8;

static u8
prog[][4] = {
    {addi, 3, 16, 3},
    {seti, 1, 0, 4},
    {seti, 1, 0, 1},
    {mulr, 4, 1, 5},
    {eqrr, 5, 2, 5},
    {addr, 5, 3, 3},
    {addi, 3, 1, 3},
    {addr, 4, 0, 0},
    {addi, 1, 1, 1},
    {gtrr, 1, 2, 5},
    {addr, 3, 5, 3},
    {seti, 2, 9, 3},
    {addi, 4, 1, 4},
    {gtrr, 4, 2, 5},
    {addr, 5, 3, 3},
    {seti, 1, 2, 3},
    {mulr, 3, 3, 3},
    {addi, 2, 2, 2},
    {mulr, 2, 2, 2},
    {mulr, 3, 2, 2},
    {muli, 2, 11, 2},
    {addi, 5, 4, 5},
    {mulr, 5, 3, 5},
    {addi, 5, 16, 5},
    {addr, 2, 5, 2},
    {addr, 3, 0, 3},
    {seti, 0, 8, 3},
    {setr, 3, 2, 5},
    {mulr, 5, 3, 5},
    {addr, 3, 5, 5},
    {mulr, 3, 5, 5},
    {muli, 5, 14, 5},
    {mulr, 5, 3, 5},
    {addr, 2, 5, 2},
    {seti, 0, 0, 0},
    {seti, 0, 0, 3},
};


static inline void
dispatch(u8* instr, int* mem) {
    switch (instr[0]) {
        case addi:
            mem[instr[3]] = mem[instr[1]] + instr[2];
            break;
        case addr:
            mem[instr[3]] = mem[instr[1]] + mem[instr[2]];
            break;
        case eqrr:
            mem[instr[3]] = mem[instr[1]] == mem[instr[2]];
            break;
        case gtrr:
            mem[instr[3]] = mem[instr[1]] > mem[instr[2]];
            break;
        case muli:
            mem[instr[3]] = mem[instr[1]] * instr[2];
            break;
        case mulr:
            mem[instr[3]] = mem[instr[1]] * mem[instr[2]];
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
    int progn = sizeof(prog) / sizeof(prog[0]);
    int mem[6] = {};
    mem[0] = 1;
    const int rip = 3;

    for (int ip = 0; ip >= 0 && ip < progn; ip++) {
        mem[rip] = ip;

        dispatch(prog[ip], mem);

        if (ip == 2) {
            mem[1] = mem[2] / mem[4];
            // printf("%d: %d %d %d %d %d %d\n", ip, mem[0], mem[1], mem[2], mem[3], mem[4], mem[5]);
        }
        else if (ip == 3) {
            if (mem[5] > mem[2]) {
                mem[1] = mem[2];
            }
        }
        else if (ip == 7) {
            mem[1] = mem[2];
        }

        ip = mem[rip];
    }

    printf("%d\n", mem[0]);

    return 0;
}

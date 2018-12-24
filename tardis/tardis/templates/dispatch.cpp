// c++ -O2 solve.cpp -o solve
#include <stdint.h>
#include <stdio.h>


using namespace std;


typedef uint8_t u8;
typedef uint32_t u32;


typedef enum opcodes {
    {%- for name in instructions %}
    {{name}},
    {%- endfor %}
} opcodes;


static inline void
dispatch(const u32* instr, u32* regs) {
    switch (instr[0]) {
        {%- if 'addi' in instructions %}
        case addi:
            regs[instr[3]] = regs[instr[1]] + instr[2];
            break;
        {%- endif %}
        {%- if 'addr' in instructions %}
        case addr:
            regs[instr[3]] = regs[instr[1]] + regs[instr[2]];
            break;
        {%- endif %}
        {%- if 'bani' in instructions %}
        case bani:
            regs[instr[3]] = regs[instr[1]] & instr[2];
            break;
        {%- endif %}
        {%- if 'banr' in instructions %}
        case banr:
            regs[instr[3]] = regs[instr[1]] & regs[instr[2]];
            break;
        {%- endif %}
        {%- if 'bori' in instructions %}
        case bori:
            regs[instr[3]] = regs[instr[1]] | instr[2];
            break;
        {%- endif %}
        {%- if 'borr' in instructions %}
        case borr:
            regs[instr[3]] = regs[instr[1]] | regs[instr[2]];
            break;
        {%- endif %}
        {%- if 'eqri' in instructions %}
        case eqri:
            regs[instr[3]] = regs[instr[1]] == instr[2];
            break;
        {%- endif %}
        {%- if 'eqrr' in instructions %}
        case eqrr:
            regs[instr[3]] = regs[instr[1]] == regs[instr[2]];
            break;
        {%- endif %}
        {%- if 'gtir' in instructions %}
        case gtir:
            regs[instr[3]] = instr[1] > regs[instr[2]];
            break;
        {%- endif %}
        {%- if 'gtri' in instructions %}
        case gtri:
            regs[instr[3]] = regs[instr[1]] > instr[2];
            break;
        {%- endif %}
        {%- if 'gtrr' in instructions %}
        case gtrr:
            regs[instr[3]] = regs[instr[1]] > regs[instr[2]];
            break;
        {%- endif %}
        {%- if 'muli' in instructions %}
        case muli:
            regs[instr[3]] = regs[instr[1]] * instr[2];
            break;
        {%- endif %}
        {%- if 'mulr' in instructions %}
        case mulr:
            regs[instr[3]] = regs[instr[1]] * regs[instr[2]];
            break;
        {%- endif %}
        {%- if 'seti' in instructions %}
        case seti:
            regs[instr[3]] = instr[1];
            break;
        {%- endif %}
        {%- if 'setr' in instructions %}
        case setr:
            regs[instr[3]] = regs[instr[1]];
            break;
        {%- endif %}
    }
}


static const u32
program[][4] = {
    {%- for line in program %}
    { {{- instructions[line[0]] }}, {% for x in line[1:] %}{{x}}{% if not loop.last %}, {% endif %}{% endfor -%} },
    {%- endfor %}
};


int main(int argc, char const *argv[]) {
    const u32 progn = sizeof(program) / sizeof(program[0]);
    const u8 rip = {{rip}};
    u32 regs[6] = { {%- for x in registers %}{{x}}{% if not loop.last %}, {% endif %}{% endfor -%} };

    for (u32 ip = {{ip}}; ip >= 0 && ip < progn; ip++) {
        regs[rip] = ip;
        dispatch(program[ip], regs);
        ip = regs[rip];
    }

    printf("%d\n", regs[0]);

    return 0;
}

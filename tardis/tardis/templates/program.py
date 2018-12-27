#!/usr/bin/env pypy3
# Generated with Tardis https://github.com/paiv/aoc2018

{% if 'addi' in instructions %}
def addi(a, b, c, regs):
    regs[c] = regs[a] + b
{%- endif %}

{%- if 'addr' in instructions %}
def addr(a, b, c, regs):
    regs[c] = regs[a] + regs[b]
{%- endif %}

{%- if 'bani' in instructions %}
def bani(a, b, c, regs):
    regs[c] = regs[a] & b
{%- endif %}

{%- if 'banr' in instructions %}
def banr(a, b, c, regs):
    regs[c] = regs[a] & regs[b]
{%- endif %}

{%- if 'bori' in instructions %}
def bori(a, b, c, regs):
    regs[c] = regs[a] | b
{%- endif %}

{%- if 'borr' in instructions %}
def borr(a, b, c, regs):
    regs[c] = regs[a] | regs[b]
{%- endif %}

{%- if 'eqir' in instructions %}
def eqir(a, b, c, regs):
    regs[c] = 1 if a == regs[b] else 0
{%- endif %}

{%- if 'eqri' in instructions %}
def eqri(a, b, c, regs):
    regs[c] = 1 if regs[a] == b else 0
{%- endif %}

{%- if 'eqrr' in instructions %}
def eqrr(a, b, c, regs):
    regs[c] = 1 if regs[a] == regs[b] else 0
{%- endif %}

{%- if 'gtir' in instructions %}
def gtir(a, b, c, regs):
    regs[c] = 1 if a > regs[b] else 0
{%- endif %}

{%- if 'gtri' in instructions %}
def gtri(a, b, c, regs):
    regs[c] = 1 if regs[a] > b else 0
{%- endif %}

{%- if 'gtrr' in instructions %}
def gtrr(a, b, c, regs):
    regs[c] = 1 if regs[a] > regs[b] else 0
{%- endif %}

{%- if 'muli' in instructions %}
def muli(a, b, c, regs):
    regs[c] = regs[a] * b
{%- endif %}

{%- if 'mulr' in instructions %}
def mulr(a, b, c, regs):
    regs[c] = regs[a] * regs[b]
{%- endif %}

{%- if 'seti' in instructions %}
def seti(a, b, c, regs):
    regs[c] = a
{%- endif %}

{%- if 'setr' in instructions %}
def setr(a, b, c, regs):
    regs[c] = regs[a]
{%- endif %}


instr = ({% for name in instructions %}{{name}}{% if not loop.last %}, {% endif %}{% endfor %})


program = (
    {%- for line in program %}
    {{line}},
    {%- endfor %}
    )


def main():
    regs = {{registers}}
    rip = {{rip}}
    ip = {{ip}}

    while 0 <= ip < len(program):
        regs[rip] = ip
        op, a, b, c = program[ip]
        instr[op](a, b, c, regs)
        ip = regs[rip] + 1

    return regs[0]


if __name__ == '__main__':
    print(main())

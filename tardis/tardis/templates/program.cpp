// c++ -O2 solve.cpp -o solve
#include <stdint.h>
#include <stdio.h>

typedef uint8_t u8;
typedef uint32_t u32;


int main(int argc, char const *argv[]) {
    u32 {% for name, value in registers.items() %}{{name}} = {{value}}{% if not loop.last %}, {% endif %}{% endfor %};

    {%- for line in program %}
    {{line}}
    {%- endfor %}

    printf("%d\n", r0);

    return 0;
}

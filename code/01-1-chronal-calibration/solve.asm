; synacor vm

read_int:
  set d 0
  set c 1
  in b
  eq f b '+'
  jt f :input
  eq f b '-'
  jf f :input
  add c c -2
input:
  in b
  eq f b 10
  jt f :process
  mult d d 10
  add b b -'0'
  add d d b
  jmp :input

process:
  mult d d c

print_int: ; d
  push 0

print10:
  mod a d 10
  add a a '0'
  push a

div10:
  set b 0
  jmp :remainder10

sub10:
  add d d -10
  add b b 1

remainder10:
  gt c 10 d
  jf c :sub10

  set d b
  jt d :print10

output:
  pop a
  out a
  jt a :output

memory:

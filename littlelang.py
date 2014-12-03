"""
Basic languague by finkcl

"""

import os
import sys
from rpython.rlib.jit import JitDriver
jitdriver = JitDriver(greens=['pc', 'code', 'program'],
        reds=['stack'])

def mainloop(program):
    pc = 0
    stack = []

    while pc < len(program):
        code = program[pc]
        jitdriver.jit_merge_point(pc=pc, code=code, program=program, stack=stack)
        # PRINT
        if code == 1:
            if len(stack) > 0:
                var = stack.pop()
                os.write(1, str(var) + "\n")
            else: os.write(1, "Error: nothing on stack to print\n")
            pc = pc + 2

        # ADD
        elif code == 2:
            if len(stack) > 0:
                a = stack.pop()
                stack.append(a + program[pc+1])
            else: os.write(1, "Error: not enough variables to add\n")
            pc = pc + 2

        # SUB
        elif code == 3:
            if len(stack) > 0:
                a = stack.pop()
                stack.append(a - program[pc+1])
            else: os.write(1, "Error: not enough variables to subtract\n")
            pc = pc + 2

        # INT
        elif code == 4:
            var = program[pc+1]
            stack.append(var)
            pc = pc + 2

        # JUMP
        elif code == 5:
            var = program[pc+1]
            if var < len(program)/2:
                pc = var*2
            else: os.write(1, "Error: wrong syntax for JUMP\n")

        # JNZERO
        elif code == 6:
            jumpTo = program[pc+1]
            if jumpTo < len(program):
                topOfStack = stack[len(stack)-1]
                if topOfStack != 0:
                	pc = jumpTo * 2
                else: pc = pc + 2
            else: os.write(1, "Error: wrong syntax for JNZERO\n")


def parse(program):
    instructions = program.split("\n")
    os.write(1, "Instructions: \n")
    for n in instructions:
        os.write(1, n + "\n")
    tokens = []
    for n in instructions:
        if " " in n:
            tokens.extend(n.split(" "))
        elif n == "":
            continue
        else:
            tokens.append(n)
            # Dummy value for instructions with no operand
            tokens.append("0")
    os.write(1, "Tokens as text: \n")
    for n in tokens:
        os.write(1, str(n) + "\n")
    int_tokens = []
    for n in tokens:
        if n == "PRINT":
            int_tokens.append(1)
        elif n == "ADD":
            int_tokens.append(2)
        elif n == "SUB":
            int_tokens.append(3)
        elif n == "INT":
            int_tokens.append(4)
        elif n == "JUMP":
            int_tokens.append(5)
        elif n == "JNZERO":
            int_tokens.append(6)
        else: int_tokens.append(int(n))

    os.write(1, "Tokens as ints: \n")
    for n in int_tokens:
        os.write(1, str(n) + "\n")
    return int_tokens

def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    program = parse(program_contents)
    mainloop(program)

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1

    run(os.open(filename, os.O_RDONLY, 0777))
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)

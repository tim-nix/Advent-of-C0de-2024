# This program is an interpreter for a 3-bit computer:
# its program is a list of 3-bit numbers (0 through 7).
# The computer also has three registers named A, B, and
# C, but these registers aren't limited to 3 bits and
# can instead hold any integer.

# The computer knows eight instructions, each
# identified by a 3-bit number (called the
# instruction's opcode). Each instruction also reads
# the 3-bit number after it as an input; this is
# called its operand.

# A number called the instruction pointer identifies
# the position in the program from which the next
# opcode will be read; it starts at 0, pointing at the
# first 3-bit number in the program. Except for jump
# instructions, the instruction pointer increases by 2
# after each instruction is processed (to move past
# the instruction's opcode and its operand). If the
# computer tries to read an opcode past the end of the
# program, it instead halts.

# Constant and global variable
BIT_SIZE = 8
OUT_FIRST = True # For comma usage in output


# Read in the data file and convert it to a list
# of strings.
def readFile(filename):
   lines = []
   try:
      with open(filename, "r") as file:
         line = file.readline()
         while line:
            lines.append(line.replace('\n', ''))
            line = file.readline()

         file.close()
            
   except FileNotFoundError:
      print("Error: File not found!")
   except:
      print("Error: Can't read from file!")
   
   return lines


# The file input is organized into three registers
# (A, B, and C) and a program (a series of integer
# values). Parse the input so that the three register
# values are in a list (as integers) and the program
# is a list (as integers).
def parseInput(values):
   registers = []
   program = []

   # Parse the three register values.
   for r in values[:3]:
      vals = r.split()
      registers.append(int(vals[-1]))

   # Parse the program values.
   vals = values[-1].split(',')
   vals[0] = vals[0].split(':')[1]
   program = [ int(v) for v in vals ] 

   # Return the results.
   return [ registers, program ]


# Convert the combo operand value
def convertCombo(registers, combo):
   if combo <= 3:
      return combo
   elif combo == 4:
      return registers[0]
   elif combo == 5:
      return registers[1]
   elif combo == 6:
      return registers[2]
   elif combo >= 7:
      raise Exception("Invalid combo operand value!")


# The adv instruction (opcode 0) performs division.
# The numerator is the value in the A register. The
# denominator is found by raising 2 to the power of
# the instruction's combo operand. The result of the
# division operation is truncated to an integer and
# then written to the A register.
def adv(registers, combo):
   numerator = registers[0]
   denominator = 2 ** convertCombo(registers, combo)
   registers[0] = numerator // denominator


# The bxl instruction (opcode 1) calculates the bit-
# wise XOR of register B and the instruction's literal
# operand, then stores the result in register B.
def bxl(registers, literal):
   value = registers[1] ^ literal
   registers[1] = value

# The bst instruction (opcode 2) calculates the value
# of its combo operand modulo 8 (thereby keeping only
# its lowest 3 bits), then writes that value to the B
# register.
def bst(registers, combo):
   value = convertCombo(registers, combo) % BIT_SIZE
   registers[1] = value


# The jnz instruction (opcode 3) does nothing if the
# A register is 0. However, if the A register is not
# zero, it jumps by setting the instruction pointer
# to the value of its literal operand; if this
# instruction jumps, the instruction pointer is not
# increased by 2 after this instruction.
def jnz(registers, literal, ip):
   if registers[0] == 0:
      return ip + 2
   else:
      return literal


# The bxc instruction (opcode 4) calculates the
# bitwise XOR of register B and register C, then
# stores the result in register B. (For legacy
# reasons, this instruction reads an operand but
# ignores it.)
def bxc(registers):
   registers[1] = registers[1] ^ registers[2]


# The out instruction (opcode 5) calculates the value
# of its combo operand modulo 8, then outputs that
# value. (If a program outputs multiple values, they
# are separated by commas.)
def out(registers, combo):
   value = convertCombo(registers, combo) % BIT_SIZE
   global OUT_FIRST
   if OUT_FIRST:
      print(value % BIT_SIZE, end = '')
      OUT_FIRST = False
   else:
      print(',' + str(value), end='')


# The bdv instruction (opcode 6) works exactly like
# the adv instruction except that the result is stored
# in the B register. (The numerator is still read from
# the A register.)
def bdv(registers, combo):
   numerator = registers[0]
   denominator = 2 ** convertCombo(registers, combo)
   registers[1] = numerator // denominator


# The cdv instruction (opcode 7) works exactly like
# the adv instruction except that the result is stored
# in the C register. (The numerator is still read from
# the A register.)
def cdv(registers, combo):
   numerator = registers[0]
   denominator = 2 ** convertCombo(registers, combo)
   registers[2] = numerator // denominator

   
if __name__ == '__main__':
   # Read and parse input to a list containing the
   # register values and a list containing the program.
   values = readFile("input17b.txt")
   registers, program = parseInput(values)

   # Run the program until the instruction pointer (ip)
   # exceeds the program instructions.
   ip = 0
   while ip < len(program):
      # Extract opcode and operand.
      opcode = program[ip]
      operand = program[ip + 1]

      modifiedIP = False # Controls changes to ip

      # Run the operation associated with the opcode.
      match opcode:
         case 0: # adv
            adv(registers, operand)
         case 1: # bxl
            bxl(registers, operand)
         case 2: # bst
            bst(registers, operand)
         case 3: # jnz
            ip = jnz(registers, operand, ip)
            # ip is modified so do not increment.
            modifiedIP = True
         case 4: # bxc
            bxc(registers)
         case 5: # out
            out(registers, operand)
         case 6: # bdv
            bdv(registers, operand)
         case 7: # cdv
            cdv(registers, operand)
         case _:
            print('Error: unknown opcode!')

      # If the ip was not modified, then increment
      # it by two (to the next opcode).
      if not modifiedIP:
         ip += 2

   # Add a newline to the end of the output.
   print()
      

   
   

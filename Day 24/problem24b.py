# The program input consists of a series of boolean
# gates and their associated input and output wires
# that, when performed, is an adder that adds the
# initial input values (denoted by labels that start
# with 'x' and 'y'). There are, unfortunately, four
# crossed wires in the circuit. This program analyzes
# the gates and identifies the crossed wires.


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


# Parse the input data splitting it into the initial
# wire values (a dictionary) and all of the gates and
# the wires connected to them. Each gate is broken 
# down into a tuple (GATE, input1, input2, output).
# The inputs and output are labels for wires.
def parseInput(values):
   # Parse the initial wire values.
   wires = dict()
   i = 0
   while values[i] != '':
      name, value = values[i].split(' ')
      wires[name[:-1]] = int(value)
      i += 1

   # Parse the gates.
   gates = []
   i += 1
   while i < len(values):
      gate = values[i].split()
      gates.append((gate[1], gate[0], gate[2], gate[4]))
      i += 1

   # Return the results.
   return (wires, gates)


# Three boolean operations are available: AND, OR, and
# XOR. Perform the gate operation, given the inputs,
# and return the results.
def performGate(gate, input1, input2):
   if gate == 'AND':
      return input1 & input2

   if gate == 'OR':
      return input1 | input2

   if gate == 'XOR':
      return input1 ^ input2


if __name__ == '__main__':
   # Read the input from the file and parse it into
   # the initial wire values and the set of gates to
   # be performed.
   values = readFile("input24b.txt")
   wires, gates = parseInput(values)

   # All initial input wires start with 'x' or 'y' and
   # all final output wires start with 'z'.
   io_gates = [ 'x', 'y', 'z' ]

   # Find the most significant bit; that is, the 'z'
   # wire with the highest number value.
   highest_z = 'z00'
   for gate in gates:
      if gate[3][0] == 'z' and int(gate[3][1:]) > int(highest_z[1:]):
         highest_z = gate[3]

   # Generate the set of crossed wires by iterating
   # through the gate operations and look for wrong
   # adder setup.
   crossed = set()
   for gate, input1, input2, output in gates:
      # All output values (except the most significant
      # bit) will result from XOR. If something else
      # is found, then add it to the 'wrong' set.
      if (output[0] == 'z') and (gate != 'XOR') and (output != highest_z):
         crossed.add(output)

      # Any XOR gate should producing output for
      # either the initial input wires ('x' or 'y') or
      # the final output wires ('z').
      if (gate == 'XOR') and (output[0] not in io_gates):
         if (input1[0] not in io_gates) and (input2[0] not in io_gates):
            crossed.add(output)

      # Ignore the AND gate in the half-adder for the
      # LSB of input. Any other AND gate should feed
      # into an OR gate. Thus, if not so, add it to
      # crossed wires.
      if (gate == 'AND') and ('x00' not in [input1, input2]):
         for gate2, input2_1, input2_2, output2 in gates:
            if ((output == input2_1) or (output == input2_2)) and (gate2 != 'OR'):
               crossed.add(output)

      # Any XOR gate should feed into either another
      # XOR or an AND gate; not an OR gate. Thus, if
      # it feeds into an OR gate, add it.
      if gate == 'XOR':
         for gate2, input2_1, input2_2, output2 in gates:
            if ((output == input2_1) or (output == input2_2)) and (gate2 == 'OR'):
               crossed.add(output)

   # Sort and display the crossed wires.
   print('crossed wires = ', end = '')
   x_wires = sorted(crossed)
   for x in x_wires[:-1]:
      print(x + ',', end = '')
   print(x_wires[-1])

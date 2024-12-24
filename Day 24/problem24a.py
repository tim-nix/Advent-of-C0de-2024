# This program solves a series of boolean gates in
# order to generate a binary output which is then
# converted to a decimal value.


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

            
if __name__ == '__main__':
   # Read the input from the file and parse it into
   # the initial wire values and the set of gates to
   # be performed.
   values = readFile("input24b.txt")
   wires, gates = parseInput(values)

   # Keep looping until all gates are performed.
   while len(gates) > 0:
      # Any gate that does not have values for the two
      # inputs is added to the next_round list for
      # processing on the next round.
      next_round = []

      # Iterate through the list of gate operations
      # and perform any in which both inputs are
      # available.
      for gate in gates:
         # Three boolean operations are available:
         # AND, OR, and XOR.
         match gate[0]:
            case 'AND':
               if (gate[1] not in wires) or (gate[2] not in wires):
                  next_round.append(gate)
               else:
                  wires[gate[3]] = wires[gate[1]] & wires[gate[2]]
            case 'OR':
               if (gate[1] not in wires) or (gate[2] not in wires):
                  next_round.append(gate)
               else:
                  wires[gate[3]] = wires[gate[1]] | wires[gate[2]]
            case 'XOR':
               if (gate[1] not in wires) or (gate[2] not in wires):
                  next_round.append(gate)
               else:
                  wires[gate[3]] = wires[gate[1]] ^ wires[gate[2]]

         # Set up for the next round.
         gates = next_round

   # Extract all of the output wires (those that start
   # with 'z'.
   bits = []
   for key in wires:
      if key[0] == 'z':
         bits.append(key)

   # Sort the output wires and then iterate through
   # them to create the output result in binary; z00
   # is the least significant bit, z01 is next, etc.
   bits.sort()
   result = ''
   for b in bits:
      result = str(wires[b]) + result

   # Convert the binary result into decimal and
   # display the result.
   print('output = ' + str(int(result, 2)))
   

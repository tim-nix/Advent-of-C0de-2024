# This program reads in a a list of every connection
# between two computers; that is, each line of text in
# the network map represents a single connection. From
# this input, sets of three computers are found where
# each computer in the set is connected to the other
# two computers. Among these sets of three computers,
# the number of sets containing at least one computer
# that starts with 't' are found.


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


# Convert the list of strings into a dictionary in
# which each key is a computer and each value is a
# computer to which the key computer is connected.
def parseInput(values):
   connections = dict()
   for v in values:
      # Split text into the two connected computers.
      pair = tuple(v.split('-'))

      # Add the undirected connection to the lists of
      # both computers.
      if pair[0] not in connections:
         connections[pair[0]] = [ pair[1] ]
      else:
         connections[pair[0]].append(pair[1])
                     
      if pair[1] not in connections:
         connections[pair[1]] = [ pair[0] ]
      else:
         connections[pair[1]].append(pair[0])

   # Return the dictionary of connections.
   return connections

            
if __name__ == '__main__':
   # Read and parse input to dictionary of connections
   # for each computer.
   values = readFile("input23b.txt")
   connections = parseInput(values)

   # For each computer, find the other two computers
   # that form the set of three that are connected.
   triplets = set()
   for key in connections:
      # Pick two computers to which the first (key) is
      # connected.
      for i in range(len(connections[key]) - 1):
         for j in range(i + 1, len(connections[key])):
            # If the other two computers are also
            # connected, then add the triplet.
            if connections[key][j] in connections[connections[key][i]]:
               t = sorted([ key, connections[key][i], connections[key][j] ])
               triplets.add(tuple(t))

   # Iterate through each triplet and, if at least one
   # computer within the triplet has a name which
   # starts with 't', increment the count.
   count = 0
   for t in triplets:
      if (t[0][0] == 't') or (t[1][0] == 't') or (t[2][0] == 't'):
            count += 1

   # Display the results.
   print(str(count) + " sets contain a computer with a name that starts with 't'.")

   


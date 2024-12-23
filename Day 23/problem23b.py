# This program reads in a a list of every connection
# between two computers; that is, each line of text in
# the network map represents a single connection. From
# this input, a list of edges is generates (a list of
# tuples with each tuple containing a pair of
# connected computers). The largest set of computers,
# in which each computer is connected to all other
# computers within the set, is found (largest clique
# within the graph of connected computers).

# This clique is displayed as a the name of every
# computer, sorted alphabetically, then joined
# together with commas.


# library used to find cliques
import networkx


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


# Convert the list of strings into a list of tuples in
# which each tuple represents a connection between two
# computers.
def parseInput(values):
   connections = []
   for v in values:
      connections.append(tuple(v.split('-')))

   # Return the dictionary of connections.
   return connections

# This function uses the networkx library to generate
# a graph from the connected computers and then find
# the computers within the largest clique (subset of
# computers that are all connected to each other).
def findMaxClique(connections):
   # Create the graph.
   G = networkx.Graph()
   G.add_edges_from(connections)

   # Generate a list of cliques within the graph.
   cliques = list(networkx.find_cliques(G))

   # Find the largest clique.
   max_clique = None
   max_clique_size = 0
   for c in cliques:
      if len(c) > max_clique_size:
         max_clique_size = len(c)
         max_clique = c

   return max_clique


if __name__ == '__main__':
   # Read and parse input to list of connections
   # between computers.
   values = readFile("input23b.txt")
   connections = parseInput(values)

   # Find the largest clique among the connections.
   clique = findMaxClique(connections)

   # Display the output as a sequence of sorted,
   # comma-separated computer names within the clique
   # (the password to the LAN party).
   clique.sort()
   print('password = ' , end='')
   for c in clique[:-1]:
      print(c + ',', end='')
   print(clique[-1])
   


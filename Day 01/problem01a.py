# Calculate the total distance from the set of
# integer values contained in the file.  The
# file consists of two columns of numbers.
# Pair up the smallest number in the left list
# with the smallest number in the right list,
# then the second-smallest left number with the
# second-smallest right number, and so on. Sum
# the total distance.

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

# Convert the list of strings into two lists of
# integers.  For each string, split it into two
# stings (removing whitespace), convert each
# string to an integer, and add each integer to
# its corresponding list of integers.
def parseInput(values):
   list1 = []
   list2 = []
   for line in values:
      num1, num2 = line.split()
      list1.append(int(num1))
      list2.append(int(num2))

   return (list1, list2)

if __name__ == '__main__':
   values = readFile("input1b.txt")
   num1, num2 = parseInput(values)
   # Sort each list of numbers
   num1.sort()
   num2.sort()

   # Generate a list of differences from the sorted lists of numbers
   differences = [ abs(num1[x] - num2[x]) for x in range(len(num1)) ]

   # Sum the total differences and print out the result
   print('Total distance = ' + str(sum(differences)))
        
    
        

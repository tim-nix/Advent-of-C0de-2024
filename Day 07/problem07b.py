# Determine whether the numbers for each equation
# can be combined with addition, multiplication,
# and concatenation operators to produce the test
# value. Operators are always evaluated left-to-right.
#Calculate the sum of the test values from just the
# equations that could possibly be true.

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


# Convert each string into a tuple in which the
# first value is the result and the second value
# is the list of numbers used in the equation.
def parseInput(values):
   equations = []
   for line in values:
      r, nums = line.split(':')
      numbers = [ int(x) for x in nums.split() ]
      equations.append((int(r), numbers))

   return equations


# Recursively traverse the set of numbers. On
# one recursive call use addition, and on a
# different recursive call use multiplication.
# If all numbers have been computed, check to
# see if the results of the computation match
# the listed result.
def calcEquation(result, numbers, current, calcSoFar):
   if (current == len(numbers)):
      return result == calcSoFar
   elif calcSoFar > result:
      return False
   else:
      # Recurse on addition.
      calc1 = calcEquation(result, numbers, current+1, calcSoFar + numbers[current])
      # Recurse on multiplication.
      calc2 = calcEquation(result, numbers, current+1, calcSoFar * numbers[current])
      # Recurse on concatentation.
      calc3 = calcEquation(result, numbers, current+1, int(str(calcSoFar) + str(numbers[current])))

      # Return True if any of the three recursions
      # return True.
      return calc1 or calc2 or calc3
   

if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input7b.txt")
   equations = parseInput(values)

   # For each equation, calculate it and, if
   # it produces the correct result, add the
   # result to the sum.
   sum = 0
   for e in equations:
      if calcEquation(e[0], e[1], 0, 0):
         sum += e[0]

   print('calibration results = ' + str(sum))

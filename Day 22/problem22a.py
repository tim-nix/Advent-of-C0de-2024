# This program reads a file of initial secret numbers.
# For each number, it applies an algorithm to generate
# a pseudo-random sequence of 2000 numbers. It sums
# the 2000th pseudo-random number from each sequence.


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


# Convert the list of secret numbers, represented as
# strings, into a list of integers.
def parseInput(values):
   secrets = []
   for v in values:
      secrets.append(int(v))

   return secrets


# The mix operation if the bit-wise OR of the two
# input parameters.
def mix(secret, value):
   return secret ^ value

# The prune operation is the modulo of the input by
# the fixed constant, 16777216.
def prune(secret):
   return secret % 16777216

# This function generates the next pseudo-random
# number in the sequence by performing the following
# operations:
# -- Calculate the result of multiplying the secret
#    number by 64. Then, mix this result into the
#    secret number. Finally, prune the secret number.
# -- Calculate the result of dividing the secret number
#    by 32. Round the result down to the nearest
#    integer. Then, mix this result into the secret
#    number. Finally, prune the secret number.
# -- Calculate the result of multiplying the secret
#    number by 2048. Then, mix this result into the
#    secret number. Finally, prune the secret number.
def findNext(secret):
   secret2 = prune(mix(secret, secret * 64))
   secret2 = prune(mix(secret2, secret2 // 32))
   secret2 = prune(mix(secret2, secret2 * 2048))

   return secret2

            
if __name__ == '__main__':
   # Read and parse input to list of integers.
   values = readFile("input22b.txt")
   secrets = parseInput(values)

   # Find the 2000th secret number in the sequence.
   max_range = 2000

   # Iterate through each initial secret number,
   # generate the sequence, and sum the last number in
   # each sequence.
   sum_last = 0
   for s in secrets:
      next_num = s
      for i in range(max_range):
         next_num = findNext(next_num)
      #print('s: ' + str(next_num))
      sum_last += next_num

   # Display the resulting sum.
   print('sum of the last secret numbers is ' + str(sum_last))


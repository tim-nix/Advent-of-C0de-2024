# This program reads a file of initial secret numbers.
# For each number, it applies an algorithm to generate
# a pseudo-random sequence of 2000 numbers. The price
# of bananas fluxuate as the last digit of each number
# in the sequence. Monkeys will sell bananas after
# seeing a specific sequence of four consecutive
# changes in price.

# Determine the sequence of four consecutive changes
# in price that results in winning the most bananas.
# How many bananas are won?


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

   # The number of prices (pseudo-random numbers) to
   # generate for each starting value.
   max_range = 2000

   # For each specific sequence of four consecutive
   # changes in price, store the sum of the number of
   # bananas that would be bought.
   bananas = dict()

   # Calculate for each initial value stored.
   for s in secrets:
      previous = 0
      price = s % 10
      diff = 0
      sequence = []
      next_num = s
      # Looking for first occurrence of each sequence.
      found = set()

      # Generate the sequence of prices.
      for i in range(max_range):
         next_num = findNext(next_num)
         next_price = next_num % 10

         # Determine the change in price.
         diff = next_price - price
         sequence.append(diff)
         price = next_price

         # We only look at 4-value changes in price.
         if len(sequence) > 4:
            sequence.pop(0)
            index = tuple(sequence)

            # If the sequence if first encountered,
            # add it to the dictionary of price change
            # sequences.
            if index not in bananas:
               bananas[index] = price
               found.add(index)
            # If the sequence already exists, then add
            # the number of bananas purchased in this
            # sequence the first time the sequence is
            # encountered.
            elif index not in found:
               bananas[index] += price
               found.add(index)

   # Iterate through the dictionary to find the
   # sequence that generates the most bananas.
   max_key = 0
   max_bananas = 0
   for key in bananas:
      if bananas[key] > max_bananas:
         max_bananas = bananas[key]
         max_key = key

   # Display the results.
   print('max bananas = ' + str(max_bananas))
   print('best sequence = ' + str(max_key))

         




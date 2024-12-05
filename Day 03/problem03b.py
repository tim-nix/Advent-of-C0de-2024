# Parse through the file input to extract
# instructions in the form mul(X,Y), where
# X and Y are each 1-3 digit numbers. For
# instance, mul(44,46) multiplies 44 by 46
# to get a result of 2024.

# There are also two other instructions that
# need to be handled: the do() instruction
# enables future mul instructions; and the
# don't() instruction disables future mul
# instructions.

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


if __name__ == '__main__':
   # Read and parse input
   values = readFile("input3b.txt")
   sum_products = 0
   do = True
   # There could be line breaks in the input resulting
   # in different strings within the list.
   for line in values:
      # Start at the beginning of the string and iterate
      # through its contents
      i = 0
      while i < len(line):
         #print('i = ' + str(i))
         try:
            # Look for the string 'do()' starting at the
            # current position
            if line[i:i+4] == 'do()':
               #print("found do()")
               do = True

            elif line[i:i+7] == "don't()":
               #print("found don't()")
               do = False
   
            # Look for the string 'mul(' starting at the
            # current position
            elif line[i:i+4] == 'mul(':
               #print('found mul')
               inc = 4
               first = ''
               # Extract the first number
               while line[i+inc].isdigit():
                  first += line[i+inc]
                  inc += 1

               #print('first = ' + first)
               # Next should be a comma
               if (line[i+inc] == ','):
                  inc += 1
                  second = ''
                  # Extract the second number
                  while line[i+inc].isdigit():
                     second += line[i+inc]
                     inc += 1

                  #print('second = ' + second)
                  # Next should be a closing parenthesis
                  if (line[i+inc] == ')'):
                     # Form is correct, so convert numbers to
                     # integers, multiply together, and add to
                     # the running sum.
                     if do:
                        sum_products += int(first) * int(second)

            i += 1
            
         except IndexError:
            i = len(line)

      # Print the results for the string.
      print('sum = ' + str(sum_products))
   

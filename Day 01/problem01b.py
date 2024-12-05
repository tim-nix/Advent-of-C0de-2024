# Calculate a total similarity score by adding up
# each number in the left list after multiplying
# it by the number of times that number appears
# in the right list.

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


# Count the number of times that the number
# appears in the numList.
def countOccurences(number, numList):
   count = 0
   for x in numList:
      if (number == x):
         count += 1

   return count


if __name__ == '__main__':
   values = readFile("input1b.txt")
   num1, num2 = parseInput(values)

   # Calculate the similarity score.
   score = 0
   for num in num1:
      count = countOccurences(num, num2)
      score += num * count

   # Print the resulting score.
   print('Similarity score = ' + str(score))
        
    
        

# Determine the sum of middle elements for all
# CORRECTED orderings according to the rules.
# The rules and the orderings are contained
# within the input file. The first section of
# the input file specifies the page ordering
# rules, one per line. The second section
# specifies the page numbers of each update.

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


# Convert a list of strings into a list of
# orderings and a list of updates. The list
# of orderings will consist of tuples of
# integers. The list of updates will consist
# of a list of lists of integers.
def parseInput(values):
   # Split the input based on orderings and
   # updates
   split_index = values.index('')
   ordering = values[:split_index]
   # Convert orderings to tuples of integers
   order = []
   for o in ordering:
      lo, hi = o.split('|')
      order.append((int(lo), int(hi)))
   
   sequences = values[split_index+1:]
   # Convert updates to lists of integers
   updates = []
   for s in sequences:
      updates.append([ int(x) for x in s.split(',') ])

   return (order, updates)


# Check the update and if it needs correcting,
# flag it and correct it (sort).
def sort_update(update, order):
   corrected = False
   # Use 'while' loops because when a page
   # ordering is corrected, run the correction
   # through all order rules.
   u_i = 0
   while u_i < len(update):
      # Check page against all rules or until a
      # correction is made.
      o_i = 0
      good_pos = True
      while good_pos and (o_i < len(order)):
         # The page could be either the left or right part of the order rule.
         if (update[u_i] in order[o_i]) and (order[o_i][0] in update) and (order[o_i][1] in update):
            # Are the pages out of order?
            if update.index(order[o_i][0]) > update.index(order[o_i][1]):
               corrected = True
               good_pos = False
               # Swap the pages
               u_c1 = update.index(order[o_i][0])
               u_c2 = update.index(order[o_i][1])
               temp = update[u_c1]
               update[u_c1] = update[u_c2]
               update[u_c2] = temp

         o_i += 1

      # If the pass was made without any corrections, then
      # move to the next page in the update.
      if good_pos:
         u_i += 1

   return (corrected, update)


# Get the middle value within the update.
def getMiddle(update):
   middle_i = len(update) // 2
   return update[middle_i]


if __name__ == '__main__':
   # Read and parse input to a grid of characters.
   values = readFile("input5b.txt")
   order, updates = parseInput(values)

   sum = 0
   # Iterate through the updates
   for u in updates:
      # Check to see if the update is corrected
      corrected, new_update = sort_update(u, order)
      if corrected:
         # If corrected, add the middle element
         # to the sum
         sum += getMiddle(new_update)
      

   # Print the results
   print('sum of middle elements = ' + str(sum))
         

   

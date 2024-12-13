# The configuration for each claw machine consists
# in an change in the x, y claw position when the
# A button is pressed, a change in the x, y position
# when the B button is pressed, and the x, y position
# of the prize.

# Pressing the A button costs 3 tokens and pressing
# the B button costs 1 token. For each machine,
# determine the fewest tokens that will result in the
# claw moving to the position of the prize.

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


# Convert the list containing strings into a list of
# tuples. Each tuple contains the x and y step for
# pushing the A button, the x and y step for pushing
# the B button, and the x and y destination.
def parseInput(values):
   configs = []

   # Three strings determine a specific configuration.
   for i in range(0, len(values), 4):
      # Parse the x and y for the A button.
      buttonA = values[i].split()
      x_valueA = buttonA[2][:-1].split('+')
      y_valueA = buttonA[3].split('+')
      a_step = (int(x_valueA[1]), int(y_valueA[1]))

      # Pase the x and y for the B button.
      buttonB = values[i + 1].split()
      x_valueB = buttonB[2][:-1].split('+')
      y_valueB = buttonB[3].split('+')
      b_step = (int(x_valueB[1]), int(y_valueB[1]))

      # Parse the x and y for the destination.
      prize = values[i + 2].split()
      x_valueP = prize[1][:-1].split('=')
      y_valueP = prize[2].split('=')
      dest = (int(x_valueP[1]), int(y_valueP[1]))

      # Add the configuration data as a tuple.
      configs.append((a_step, b_step, dest))

   # Return the configuation data.
   return configs


# Determine the number of A button pushes and B
# button pushes needed to get the claw over the
# prize location. 
def calcGameCosts(gameConfig):
   # Split up game configuration.
   a_x, a_y = gameConfig[0]
   b_x, b_y = gameConfig[1]
   p_x, p_y = gameConfig[2]
   
   # Find max A buttons
   max_a = p_x // a_x

   # Iteration through pushing the buttons to
   # determine the cost.
   for a_press in range(max_a):
      # Calculate x and y position after pushing the
      # A button some number of times.
      x = a_press * a_x
      y = a_press * a_y

      # Calculate how far is needed to reach destination.
      r_x = p_x - x
      r_y = p_y - y

      # Determine how many presses of B button are
      # needed.
      b_press = r_x // b_x

      # If pressing the B button get the claw to the
      # correct position, then calculate the cost and
      # add the move and cost to the list of combos.
      if ((b_press * b_x) == r_x) and ((b_press * b_y) == r_y):
         return 3 * a_press + b_press

   return 0


if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input13b.txt")
   configs = parseInput(values)

   spent = 0
   games_won = 0
   # Iterate through the list of configurations for
   # each machine, find the list of winning
   # combinations of button presses, and get the
   # one that costs the fewest tokens.
   for line in configs:
      win_cost = calcGameCosts(line)
      if win_cost > 0:
         games_won += 1
         spent += win_cost

   # Print the total cost to win on as many machines
   # as possible.
   print('Games won = ' + str(games_won))
   print('Total spent = ' + str(spent))

   

# The configuration for each claw machine consists
# in an change in the x, y claw position when the
# A button is pressed, a change in the x, y position
# when the B button is pressed, and the x, y position
# of the prize.

# Pressing the A button costs 3 tokens and pressing
# the B button costs 1 token. For each machine,
# determine the fewest tokens that will result in the
# claw moving to the position of the prize.

# For this part, the prize x, y position is too large
# for iteration. Thus, the system of linear equations
# was solved to calculate the button presses.

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
   # Modify the prize x and y locations based on offset.
   offset = 10000000000000
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
      dest = (int(x_valueP[1]) + offset, int(y_valueP[1]) + offset)

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

   # The system of linear equations:
   #
   #    (a_press * a_x) + (b_press * b_x) = p_x
   #    (a_press * a_y) + (b_press * b_y) = p_y
   #
   # was solved for b_press and a_press.
   b_press = abs((p_x * a_y - p_y * a_x) // (b_x * a_y - a_x * b_y))
   a_press = (p_x - b_press * b_x) // a_x

   # Calculate the x, y position for the determined
   # button presses.
   r_x = a_press * a_x + b_press * b_x
   r_y = a_press * a_y + b_press * b_y

   # If the button presses result in the correct
   # location of the claw, then return the cost.
   if (p_x == r_x) and (p_y == r_y):
      return 3 * a_press + b_press
   else:
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

   

# Given the location and velocities of a group of
# robots, determine the fewest number of seconds that
# must elapse for the robots to display the Easter egg
# in which most of the robots arrange themselves into
# a picture of a Christmas tree.

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


# Convert the string representation of each robot's
# position and velocity into a tuple of two tuples;
# the first nested tuple is the x, y position of the
# robot and the second nested tuple is the dx, dy
# velocity of the robot (per second).
def parseInput(values):
   robots = []
   for line in values:
      loc, vel = line.split()
      x, y = loc[2:].split(',')
      dx, dy = vel[2:].split(',')
      robots.append(((int(x), int(y)), (int(dx), int(dy))))

   return robots


# Construct a new tuple of the location and velocity
# of the robot after a single move.
def moveRobot(robot, max_x, max_y):
   # Current location of the robot.
   x, y = robot[0]
   # Current velocity of the robot.
   dx, dy = robot[1]

   # Update the location of the robot.
   x = (x + dx) % max_x
   y = (y + dy) % max_y

   # Return new tuple.
   return ((x, y), (dx, dy))


if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input14b.txt")
   robots = parseInput(values)

   # Set the grid width and height
   max_x = 101 # 11
   max_y = 103 # 7

   # Robots continue to move until a each robot is
   # located on a unique tile; that is, no overlap
   # of robots.
   time = 0
   overlap = True
   while (overlap):
      new_locations = []
      locations = set()
      # Move each robot
      for r in robots:
         moved = moveRobot(r, max_x, max_y)
         new_locations.append(moved)
         locations.add(moved[0])

      robots = new_locations
      time += 1

      # Determine if robots do not overlap.
      if len(locations) == len(robots):
         # Set boolean to break loop
         overlap = False

         # Convert list of locations to picture.
         # Initialize a grid as a list of lists of
         # characters.
         grid = []
         for y in range(max_y):
            grid.append([ '.' for x in range(max_x) ])

         # Plot each robot on the grid
         for key in locations:
            x, y = key
            grid[y][x] = 'X'

         # Display the results
         print('time = ' + str(time))
         for line in grid:
            print(''.join(line))
               
      
      

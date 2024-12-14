# Given the location and velocities of a group of
# robots, determine the safety factor.  The safety
# factor is calculated by multiplying together the
# number of robots in each quadrant.

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

   # Set the number of seconds to move the robots.
   max_time = 100

   # Robots continue to move up to max_time
   for t in range(max_time):
      new_locations = []
      # Move each robot
      for r in robots:
         new_locations.append(moveRobot(r, max_x, max_y))

      robots = new_locations

   # Calculate the quadrant boundaries.
   center_x = max_x // 2
   center_y = max_y // 2

   # Count robots in each quadrant - robots that are
   # exactly in the middle (either horizontally or
   # vertically don't count as being in any quadrant.
   upper_left = 0
   upper_right = 0
   lower_left = 0
   lower_right = 0
   for r in robots:
      x, y = r[0]
      if (x < center_x) and (y < center_y):
         upper_left += 1
      if (x > center_x) and (y < center_y):
         upper_right += 1
      if (x < center_x) and (y > center_y):
         lower_left += 1
      if (x > center_x) and (y > center_y):
         lower_right += 1

   # Calculate the safety factor (the product of the
   # number of robots in each quadrant) and print it.
   safety = upper_left * upper_right * lower_left * lower_right
   print('safety factor = ' + str(safety))
         

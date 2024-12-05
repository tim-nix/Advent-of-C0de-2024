# Determine the number of reports that are safe.
# A report is safe if the levels are either all
# increasing or all decreasing AND if any two
# adjacent levels differ by at least one and at
# most three.

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

# Convert the list of strings into a list of
# lists of integers.
def parseInput(values):
   numList = []
   # For each string, split it into a list of
   # strings on the whitespace.
   for line in values:
      report = []
      nums = line.split()
      # Convert each text number to an integer
      for n in nums:
         report.append(int(n))
      
      numList.append(report)

   return numList


# Determine if a given report is safe (return
# True if safe and False if unsafe).  
def checkReport(report):
   # Determine if initially increasing or decreasing.
   if report[0] < report[1]:
      increasing = True
   else:
      increasing = False

   # Determine if initial increasing or decreasing
   # changes, if difference is 0, or if difference
   # is greater than 3.  If so, return False (unsafe).
   for i in range(1, len(report)):
      if (report[i - 1] < report[i]) and not increasing:
         return False
      elif (report[i - 1] > report[i]) and increasing:
         return False
      elif (report[i - 1] == report[i]):
         return False
      elif abs(report[i - 1] - report[i]) > 3:
         return False

   # Report is safe.
   return True


if __name__ == '__main__':
   # Read and parse input
   values = readFile("input2b.txt")
   reports = parseInput(values)

   # Count safe reports
   safe = 0
   for report in reports:
      if (checkReport(report)):
         safe += 1

   # Print results
   print('safe reports = ' + str(safe))
    
        

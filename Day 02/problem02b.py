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


# Determine if a given report is safe (return True
# if safe and False if unsafe).  If the report is
# unsafe, also return the index at which the unsafe
# condition was detected.
def checkReport(report):
   # Determine if initially increasing or decreasing.
   if report[0] < report[1]:
      increasing = True
   else:
      increasing = False

   # Determine if initial increasing or decreasing
   # changes, if difference is 0, or if difference
   # is greater than 3.
   for i in range(1, len(report)):
      if (report[i - 1] < report[i]) and not increasing:
         return (False, i - 1)
      elif (report[i - 1] > report[i]) and increasing:
         return (False, i - 1)
      elif (report[i - 1] == report[i]):
         return (False, i - 1)
      elif abs(report[i - 1] - report[i]) > 3:
         return (False, i - 1)

   # Report is safe.
   return (True, 0)


if __name__ == '__main__':
   # Read and parse input
   values = readFile("input2b.txt")
   reports = parseInput(values)

   # Count safe reports
   safe = 0
   for report in reports:
      results = checkReport(report)
      if results[0]:
         safe += 1
      else:
         # Unsafe report is detected.  Thus,
         # need to determine if removing a
         # single element fixes the unsafe
         # report.

         # Make two copies of the report.
         report2 = [ x for x in report ]
         report3 = [ x for x in report ]

         # Check to see if removing first
         # element fixes the problem.
         report.pop(0)
         if checkReport(report)[0]:
            safe += 1
         else:
            # Check to see if removing the
            # element at the problem index
            # (returned by the function call)
            # fixes the problem.
            report2.pop(results[1])
            if checkReport(report2)[0]:
               safe += 1
            else:
               # Check to see if removing the
               # element at the problem index
               # + 1 fixes the problem.
               report3.pop(results[1] + 1)
               if checkReport(report3)[0]:
                  safe += 1

   # Print results
   print('safe reports = ' + str(safe))
    
        

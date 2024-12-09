# Calculate the checksum on a compacted disk drive.
# The file input represents the layout of files and
# free space on the disk. The digits alternate
# between indicating the length of a file and the
# length of free space. Each file on disk also has
# an ID number based on the order of the files as
# they appear before they are rearranged, starting
# with ID 0. The disk is compressed; that is, file
# blocks are moved from the back of the disk to
# free space at the front of the disk (in this
# solution, the blocks are moved one at a time and
# can be split up over different sequences of free
# space). Then, the checksum is computed.


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


# Convert the string of digits into a list of
# integers; the even number digits (by list
# index) represent sequential file blocks and
# the odd number digits represent sequential free
# space.
def parseInput(values):
   drive = [ int(x) for x in list(values[0]) ]
   
   return drive
   

# Convert the drive formatting data into a list
# containing a sequence of fileIDs and character
# representations of free space. The index of the
# list corresponds to the block position.
def mapDrive(drive):
   driveMap = []
   fileID = 0
   freeSpace = False
   for x in drive:
      # Map out the sequence of free space.
      if freeSpace:
         for i in range(x):
            driveMap.append('.')
         freeSpace = False
      else:
         # Map out the sequence of file blocks.
         for i in range(x):
            driveMap.append(fileID)
         fileID += 1
         freeSpace = True

   # Return the mapped representation of the drive.
   return driveMap


# To calculate the checksum, add up the result of
# multiplying each of these blocks' position with
# the file ID number it contains. The leftmost block
# is in position 0. If a block contains free space,
# skip it instead.
def calcChecksum(driveMap):
   checkSum = 0
   for i in range(len(driveMap)):
      if driveMap[i] != '.':
         checkSum += driveMap[i] * i

   return checkSum


# Disk compression moves file blocks one at a time
# from the end of the disk to the leftmost free
# space block (until there are no gaps remaining
# between file blocks).
def compactDrive(driveMap):
   i = 0
   j = len(driveMap) - 1
   while i < j:
      # Find first free space
      while driveMap[i] != '.':
         i += 1
      
      # Find last block
      while driveMap[j] == '.':
         j -= 1

      # Make sure that the block is moved left
      # (closer to the front of the disk).
      if i < j:
         driveMap[i] = driveMap[j]
         driveMap[j] = '.'

   return driveMap 
   

if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input9b.txt")
   drive = parseInput(values)
   driveMap = mapDrive(drive)
   compacted = compactDrive(driveMap)
   checkSum = calcChecksum(compacted)
   print('checksum = ' + str(checkSum))

   

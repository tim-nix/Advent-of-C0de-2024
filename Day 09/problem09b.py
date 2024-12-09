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
# solution, the entire sequence of blocks for a given
# file are moved). Then, the checksum is computed.


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


# Disk compression moves the entire sequence of file
# blocks from the end of the disk to the leftmost free
# space block large enough to accomodate moving the
# entire set of blocks.
def compactDrive(driveMap):
   # Start at back of drive
   j = len(driveMap) - 1

   # Find the highest file ID
   while driveMap[j] == '.':
         j -= 1

   # Get the file ID
   fileID = driveMap[j]
      
   while fileID > 0:
      # Get the front of the file
      j2 = j
      while driveMap[j2] == fileID:
         j2 -= 1

      # Calculate file size
      numBlocks = j - j2

      # Find spot from start of disk
      found = False
      i = 0
      while not found and (i < j2):
         # Find free space
         while driveMap[i] != '.':
            i += 1

         # Calculate size of free space
         size = 0
         start = i
         while driveMap[i] == '.':
            i += 1
            size += 1

         # If free space is large enough and
         # the free space is to the left of
         # the file, then move the file.
         if (size >= numBlocks) and (start <= j2):
            found = True
            for k in range(numBlocks):
               driveMap[start + k] = fileID
               driveMap[j2 + 1 + k] = '.'

      j = j2
      fileID -= 1
      while driveMap[j] != fileID:
         j -= 1

   return driveMap 
   

if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input9b.txt")
   drive = parseInput(values)
   driveMap = mapDrive(drive)
   compacted = compactDrive(driveMap)
   checkSum = calcChecksum(compacted)
   print ('6460170597310 is too high')
   print('checksum = ' + str(checkSum))

   

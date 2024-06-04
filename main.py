import os, sys, random, math

# Arg 1: Distance check: short = less than 1/2 average. medium = greater than 1/2 average, less than 3/2 average. long = greater than 3/2 average, less than double average
# Arg 2: Number reps: number of non repeating reps 

def get_distance(sx, sy, dx, dy):
  return ((int(dx) - int(sx))**2 + (int(dy) - int(sy))**2)**(0.5)

def get_heuristic(sx, sy, dx, dy, px, py, i):
    heuristic_type = int(i)
    if px == 0 and py == 0:
      return 0 # Using Dijkstra's algorithm
    if heuristic_type == 1:
        # Using Dijkstra's algorithm
        return 0 
    elif heuristic_type == 2:
      # Using Straight line distance or Euclidean distance
      return ((int(dx) - int(sx))**2 + (int(dy) - int(sy))**2)**(0.5)
    elif heuristic_type == 3:
      # Using heuristic 3. A heuristic that adds a fraction of the distance based
      # on if the turn is a left turn, a straight, or right turn

      fracMultiplier = 1
      vector1 = (int(dx) - int(sx), int(dy) - int(sy))
      vector2 = (int(px) - int(sx), int(py) - int(sy))

      #Calculate the cross product of the two vectors
      cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]

      # Calculate the angle between the vectors using atan2 to handle the sign
      angle_radians = math.atan2(cross_product, vector1[0] * vector2[0] + vector1[1] * vector2[1])

      # Convert radians to degrees
      angle_degrees = math.degrees(angle_radians)

      if angle_degrees < -30:   # Left turn  
        fracMultiplier = 1.5
      elif angle_degrees < 120: # Right turn
        fracMultiplier = 2
      else:                     # Straight turn
        fracMultiplier = 2.5

      return (1/fracMultiplier) * get_distance(sx, sy, dx, dy)
    elif heuristic_type == 4:
      # Using heuristic 4. A Heuristic that prefers to take longer roads to avoid intersections
      distRoad = get_distance(sx, sy, dx, dy)
      return ((691 - distRoad) / 691) * distRoad
    elif heuristic_type == 5:
      # Using heuristic 5, a mixture of heuristic 3 and heuristic 4

      # Using heuristic 3. A heuristic that adds a fraction of the distance based
      # on if the turn is a left turn, a straight, or right turn

      fracMultiplier = 1

      vector1 = (int(dx) - int(sx), int(dy) - int(sy))
      vector2 = (int(px) - int(sx), int(py) - int(sy))

      #Calculate the cross product of the two vectors
      cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]

      # Calculate the angle between the vectors using atan2 to handle the sign
      angle_radians = math.atan2(cross_product, vector1[0] * vector2[0] + vector1[1] * vector2[1])

      # Convert radians to degrees
      angle_degrees = math.degrees(angle_radians)

      if angle_degrees < -30:   # Left turn  
        fracMultiplier = 2
      elif angle_degrees < 120: # Right turn
        fracMultiplier = 2.5
      else:                     # Straight turn
        fracMultiplier = 3
      
      distRoad = get_distance(sx, sy, dx, dy)
        
      return (((691 - distRoad) / (691 * 2)) + (1/fracMultiplier)) * distRoad
        
    else:
        print("Invalid heuristic type specified")
        sys.exit(1)


# Get the current working directory
current_directory = os.getcwd()

# Assuming the CSV file is in the current working directory
file_name = "map.csv"
file_path = os.path.join(current_directory, file_name)

# Check if the file exists
if os.path.exists(file_path):
  Map = {}
  # Open the file in read mode
  with open(file_path, 'r') as file:
    # Read each line in the file
    for line in file:
      # Parse the line by commas
      data = line.strip().split(',')
      if data[1] in Map.keys(): #Check if starting x in Map Dict
        if data[2] in Map[data[1]].keys(): # Check if starting y is in Map Dict
          Map[data[1]][data[2]] = Map[data[1]][data[2]] + [[data[3], data[4]]] #Add new street connection
        else: # Y not in dict
          Map[data[1]][data[2]] = [[data[3], data[4]]] # Create new nested dict with street connection
      else:
        Map[data[1]] = {data[2]: [[data[3], data[4]]]} # Create new nested dict with street connection    
      if data[0] == '2':
        if data[3] in Map.keys():
          if data[4] in Map[data[3]].keys():
            Map[data[3]][data[4]] = Map[data[3]][data[4]] + [[data[1], data[2]]]
          else: 
            Map[data[3]][data[4]] = [[data[1], data[2]]]
        else:
          Map[data[3]] = {data[4]: [[data[1], data[2]]]}
else:
  print(f"File '{file_name}' not found in the current directory.")

aveDist = 0
lowestDist = 100000
highestDist = 0
i = 0
while i < 10000:
  randStartX = (random.choice(list(Map.keys())))
  randStartY = (random.choice(list(Map[str(randStartX)].keys())))
  randDestX = (random.choice(list(Map.keys())))
  randDestY = (random.choice(list(Map[str(randDestX)].keys())))
  dist = get_distance(randStartX, randStartY, randDestX, randDestY)

  aveDist += dist
  if dist < lowestDist and dist != 0:
      lowestDist = dist
  if dist > highestDist:
      highestDist = dist
  i += 1
aveDist = aveDist / 10000
print("Average distance:", aveDist)
print("Lowest distance:", lowestDist)
print("Highest distance:", highestDist)

#Lowest recorded dist 5.65
#Highest recorded dist 5499.76
#Average recordded 1700

i = 0
lb = 0
ub = 0

# Lower and upper bound depending on user input
if sys.argv[1] == 'short':
    lb = 0
    ub = 0.5
elif sys.argv[1] == 'medium':
    lb = 0.5
    ub = 1.5
elif sys.argv[1] == 'long':
    lb = 1.5
    ub = 2
else:
    print("Invalid arguments, use main.py short/medium/long 1-inf 1-5")
    sys.exit(1)
    
zeroFlag = True


while i < int(sys.argv[2]):
  nodeCount1 = 0
  nodeCount2 = 0
  nodeCount3 = 0
  nodeCount4 = 0
  nodeCount5 = 0
  finalPath1 = []
  finalPath2 = []
  finalPath3 = []
  finalPath4 = []
  finalPath5 = []
  dist = -1

  while ((dist < lb*aveDist) or (dist > ub*aveDist)):
    # Reroll start and dest until fit conditions
    randStartX = str(random.choice(list(Map.keys())))
    randStartY = str(random.choice(list(Map[randStartX].keys())))

    randDestX = str(random.choice(list(Map.keys())))
    randDestY = str(random.choice(list(Map[randDestX].keys())))
      
    # Make sure destinations do not match start
    while randDestX == randStartX:
      randDestX = str(random.choice(list(Map.keys())))
    while randDestY == randStartY:
      randDestY = str(random.choice(list(Map[randDestX].keys())))

    dist = get_distance(randStartX, randStartY, randDestX, randDestY)

  
  for heur in range(1, 6):
    visitedNodes = []
    frontier = []
    finalpath = []

    print(str(randStartX) + " " + str(randStartY) + " " + str(heur))

    #Add start to frontier
    visitedNodes.append([randStartX, randStartY])
    frontier.append([randStartX, randStartY, 0, 0])

    #While destination is not in frontier
    while not [randDestX, randDestY] in visitedNodes:
      fitness = 10000 # Unreasonbly high fitness level
      bestFit = [0, 0] # Nonexistent bestfit
      for trees in frontier:
        if str(trees[0]) in Map and str(trees[1]) in Map[str(trees[0])]: 
          for neighbors in Map[str(trees[0])][str(trees[1])]:
            if neighbors in visitedNodes:
              continue
            startX = trees[0]
            startY = trees[1]
            neighborX = neighbors[0]
            neighborY = neighbors[1]
            neighDist = get_distance(startX, startY, neighborX, neighborY)
            neighHeur = get_heuristic(startX, startY, neighborX, neighborY, trees[2], trees[3], heur)
            if neighHeur > neighDist:
              print(str(neighDist) + " < " + str(neighHeur))
              print("NON-ADMISSABLE ERROR")
              sys.exit()
            tmpFitness = neighDist + neighHeur
            if tmpFitness < fitness:
              bestFit = [neighbors[0], neighbors[1], trees[0], trees[1]]
              fitness = tmpFitness
      if bestFit[0] == 0 and bestFit[1] == 0:
        print("0, 0 escaped")
        print("start: " + str(randStartX) +", " + str(randStartY) + "  dest: " + str(randDestX) + ", " + str(randDestY) + " dist: " + str(dist))
        print(heur)
        zeroFlag = False
        break
      frontier = frontier + [bestFit]
      visitedNodes.append([bestFit[0], bestFit[1]])
    if not zeroFlag:
      print("zeroFlag caught")
      break
    btNode = [randDestX, randDestY]
    totalDistance = 0
    while btNode != [randStartX, randStartY]:
      for nodes in frontier:
        if nodes[0] == btNode[0] and nodes[1] == btNode[1]:
          finalpath = [btNode] + finalpath
          totalDistance += get_distance(nodes[0], nodes[1], nodes[2], nodes[3])
          btNode = [nodes[2], nodes[3]]
    finalpath = [btNode] + finalpath
    if heur == 1:
      nodeCount1 = len(visitedNodes)
      finalPath1 = finalpath
    elif heur == 2:
      nodeCount2 = len(visitedNodes)
      finalPath2 = finalpath
    elif heur == 3:
      nodeCount3 = len(visitedNodes)
      finalPath3 = finalpath
    elif heur == 4:
      nodeCount4 = len(visitedNodes)
      finalPath4 = finalpath
    elif heur == 5:
      nodeCount5 = len(visitedNodes)
      finalPath5 = finalpath

    with open(("output"+str(heur))+str(sys.argv[1])+".csv", 'a') as outfile:
      if i == 0:
        outfile.write("Iter,Dist,Pathlength,Frontiersize,Totaldist,Dist" + "\n")
      if heur == 1:
        print("writing to file1")
        outfile.write(str(i)+","+str(sys.argv[1])+","+str(len(finalPath1))+","+str(len(frontier))+","+str(totalDistance)+","+str(dist)+"\n")
      elif heur == 2:
        print("writing to file2")
        outfile.write(str(i)+","+str(sys.argv[1])+","+str(len(finalPath2))+","+str(len(frontier))+","+str(totalDistance)+","+str(dist)+"\n")
      elif heur == 3:
        print("writing to file3")
        outfile.write(str(i)+","+str(sys.argv[1])+","+str(len(finalPath3))+","+str(len(frontier))+","+str(totalDistance)+","+str(dist)+"\n")
      elif heur == 4:
        print("writing to file4")
        outfile.write(str(i)+","+str(sys.argv[1])+","+str(len(finalPath4))+","+str(len(frontier))+","+str(totalDistance)+","+str(dist)+"\n")
      elif heur == 5:
        print("writing to file5")
        outfile.write(str(i)+","+str(sys.argv[1])+","+str(len(finalPath5))+","+str(len(frontier))+","+str(totalDistance)+","+str(dist)+"\n")
  if not zeroFlag:
    print("zeroFlag caught 2")
    zeroFlag = True
    continue
    
  i += 1
#input: a 2D array of 1 and 0 where 0 is walkable and 1 is not, tuple of start and end locations, and path if there is one
#output: a list of tuples indicating target tiles
#talked to Austin and he said i should try to find shortcuts in the paths to optimize it
#squad leader uses a*, other enemies use this
#problem where enemy go back and forth between the same tiles becasue favor tiles closer to the player
#solution: enemy move multiple tiles before updating

def findShortestPath(maze,startLocation,targetLocation,path,visited):
    
    if isRightNextToEachOther(startLocation,targetLocation):
        path.append(targetLocation)       
        return path
    else:
        visited.add(startLocation)
        #create neighbors
        neighbors = [(startLocation[0] + 1,startLocation[1]),(startLocation[0] - 1,startLocation[1]),
                     (startLocation[0],startLocation[1] + 1),(startLocation[0],startLocation[1] - 1)]
        
        #check boundaries and collision and if visited

        neighbors = [(row,col) for (row,col) in neighbors if row >= 0 and row <= len(maze) - 1 and col >= 0 and col <= len(maze[0]) -1 and maze[row][col] != 1]
        
        neighbors = [(row,col) for (row,col) in neighbors if (row,col) not in visited]

        if len(neighbors) == 0:
            return None 
        

        sortedNeighbors = sortByClosestToFurthest(neighbors,targetLocation)
        
        #tile is a tuple of the row and col of the tile
        for tile in sortedNeighbors:
            #if isLegalMove(maze,tile):
            path.append(tile)
            solution = findShortestPath(maze,tile,targetLocation,path[:],visited)
            if solution != None:
                return solution
            else:
                path.pop()
        return None

def sortByClosestToFurthest(neighbors,targetLocation):
    targetRow,targetCol = targetLocation
    newNeighbors = []
    result = []
    for row,col in neighbors:
        distance = (targetRow - row)**2 + (targetCol - col)**2
        newNeighbors.append((row,col,distance))

    sortedNeighbors = sorted(newNeighbors,key= lambda x:x[2])
    for row,col,d in sortedNeighbors:
        result.append((row,col))
    return result
    
def isLegalMove(maze,targetTile):
    row,col = targetTile
    if row < 0 or row > len(maze) - 1 or col < 0 or col > len(maze[0]) - 1 or maze[row][col] == 1:
        return False
    else:
        return True

def isRightNextToEachOther(start,end):
    if start[0] - end[0] == 0 and abs(start[1] - end[1]) == 1:
        return True
    elif start[1] - end[1] == 0 and abs(start[0] - end[0]) == 1:
        return True
    else:
        return False

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# A* pathfinding algorithm visualization
My implementation of A* and its visualization using Python and Pygame.

![Project screenshot](https://user-images.githubusercontent.com/44493112/113470241-5b02b580-9454-11eb-9803-41a95cad7d75.png)
<br>

## :computer: Running the program
```
$ git clone https://github.com/GBoGH/A_star.git
$ pip install -r requirements.txt
```
Run ```main.py```
<br>

## :keyboard:Controls
#### 🖱️ Left mouse button
- First click selects start
- Second click selects end
- Any additional clicks select barriers

#### 🖱️ Rigth mouse button
- Right mouse click erases any node currently clicked on
- If start or end are deleted first left click selects them again

#### ⌨️ Keyboard controls
- R: Randomly selects barriers (can be done only once)
- B: Resets all barriers (also restores the ability to use random barriers)
- P: Resets all open, closed and path nodes
- C: Clears everyhting including start and end
- Enter: Starts the algorithm (and blocks all controls while the algorithm is running)
<br>

## ⚙️ Possible customisations
In file ```custom.py``` you can customise these values to your own liking
- ROWS and COLUMNS: Dimensions of the grid. Please keep square. It should work if not square but it may be buggy
- PROBABILITY: Chance one in X that node will become barrier when using randomly selected barriers. 5 is the most optimal. Higher the number, the less barriers will be created.
<br>

## :a:⭐ Algorithm explanation
A* algorithm is based on "educated guess", the algorithm knows where the end is.  
It uses heuristics, the estimated distance from current node to the end node.  
The formula is: ```F(n) = G(n) + H(n)```.  
- H(n) is the estimated distance from node n to the end node (my algorithm uses Manhattan distance).
- G(n) is the shortest distance to get from start node to node n
- F(n) is the sum of H and G score for current node n. Node with lower F score is the more optimal.


#### Code
```python
count = 0
open_set = PriorityQueue()
open_set.put((0, count, start))
last_node = {}
```
First a set of all nodes is created and start node is inserted. The count variable determines which node was eneterd first if two nodes have identical F scores. The zero stands for F score which is zero for the start node.  l
Also set of last nodes (where did the algorithm come from) is created.  
<br>

```python
g_score = {node: float("inf") for row in grid for node in row}
g_score[start] = 0

f_score = {node: float("inf") for row in grid for node in row}
f_score[start] = h_score(start.position(), end.position())
```
All nodes are given F and G score of infinity, because these scores are not yet found.  
Then G score and H score is assigned to the start node. F score is just H score in this case because G score is zero.  
<br>

```python
while not open_set.empty():

    current = open_set.get()[2]
    
    open_set_hash.remove(current)
    
    for neighbor in current.neighbors:
        temp_g_score = g_score[current] + 1

        if temp_g_score < g_score[neighbor]:
            last_node[neighbor] = current
            g_score[neighbor] = temp_g_score
            f_score[neighbor] = temp_g_score + \
                h_score(neighbor.position(), end.position())

            if neighbor not in open_set_hash:
                count += 1
                open_set.put((f_score[neighbor], count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.make_opened()
```
What is happening in this loop.
- Current node is extracted from the set of open nodes and removed from the hash
- One (because all edges are one) it added to the G score and the G score is compared to the node's neighbors
- Node we came from is updated
- F score and G score are updated
- If the node we are on (the neighbor) has not been considered yet and has a better path, it is added to open set and the node is opened  
<br>

```python
if current != start:
    current.make_closed()
```  
If node has already been considered, close it.  
<br>

```python
if current == end:
    path(last_node, end)
    end.make_end()
    start.make_start()

    finished = True
    return finished
```
If the current node is the end node, path has been found and it is recreated.  
<br>

```python
pyautogui.alert("There isn't any path to be found")
return False
```
If there are no opened nodes and end hasnt been reached, alert is displayed and the function returns False.  
<br>


## ⚖️ License
This project is licensed under the terms of ```MIT License```

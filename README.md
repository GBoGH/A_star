[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# A* pathfinding algorithm visualization
My implementation of A* and its visualization using Python and Pygame.

![Project screenshot](https://user-images.githubusercontent.com/44493112/113470241-5b02b580-9454-11eb-9803-41a95cad7d75.png)
<br><br>
## :computer: Running the program
```
$ git clone https://github.com/GBoGH/A_star.git
$ pip install -r requirements.txt
```
Run ```main.py```<br><br>

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
<br><br>

## ⚙️ Possible customisations
In file ```custom.py``` you can customise the values to your own liking
- ROWS and COLUMNS: Dimensions of the grid. Please keep square. It should work if not square but it may be buggy
- PROBABILITY: Chance one in X that node will become barrier when using randomly selected barriers. 5 is the most optimal
<br><br>

## :a:⭐ Algorithm explanation

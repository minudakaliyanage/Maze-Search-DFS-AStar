<div align="center">

# 🧭 Maze Pathfinding: Depth-First Search vs A*

**AI fundamentals coursework: build a random 6×6 maze, then solve it with uninformed (DFS) and informed (A* with a Manhattan heuristic) search.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![No dependencies](https://img.shields.io/badge/dependencies-standard%20library%20only-brightgreen?style=flat-square)

</div>

---

## 📌 What it does

1. **Builds a 6×6 maze** of nodes `0–35`, with a random **start** (`S`) in the first two columns, a random **goal** (`G`) in the last two columns, and **4 random barriers** (`#`)
2. **Prints the maze** in colour (green start, red goal, blue barriers)
3. **Depth-First Search:** explores 8-directional neighbours in sorted order using a stack, and reports the path and the number of nodes explored
4. **A\* Search:** uses a priority queue ordered by `g + h`, where `h` is the **Manhattan distance** to the goal, and reconstructs the shortest path from predecessor links

The task treats each explored node as **1 minute** of search time, so the two algorithms can be compared on effort as well as path length.

## 🖥️ Sample output

```
0    6    12   #    #    30
#    7    13   19   25   31
2    8    14   20   G    32
3    9    15   21   27   33
4    10   #    22   28   34
S    11   17   23   29   35

-----------------Depth First Search-----------------
Time to Find Goal (in minutes): 32
Final Path: [5, 11, 17, 23, 29, 34, 33, 26]

-----------------A Star Search-----------------
Time to Find Goal (in minutes): 17
Final Path: [5, 10, 15, 20, 26]
```

In this run, **A\* explores roughly half as many nodes as DFS and finds a path 3 steps shorter**.

## 🚀 Run it

```bash
python maze_search.py
```

Each run generates a new random maze. Python 3 is all you need (only `random` and `queue` are used).

## 📂 Files

| File | Description |
|---|---|
| `maze_search.py` | Maze generation, display, DFS and A* implementations |

---

<div align="center"><sub>Built by <a href="https://github.com/minudakaliyanage">Minudaka Liyanage</a></sub></div>

# Maze
Simple maze generator in python (numpy &amp; tkinter)

## Maze generation
The maze is generated using the path merging algorithm, which output a perfect maze. The worst case performance is O(m ^ 2 * n ^ 2) where m is maze width and n is maze height.
It is represented as two boolean arrays: a 0 means no walls. The first array store the horizontal walls and the second the vertical walls.
This representation make the usage of the maze generation algorithm easier.
We then convert this representation to a graph, and more specifically a directed acyclic graph (DAG).

## Maze solving
I use a DFS algorithm to find the path between two points.
We first search for the target node in the maze graph representation (DFS algorithm). Then, we backtrace to the root node and we store parents along the way to build the path.

## Screenshots
![](https://i.ibb.co/JsqMGhB/p1.png)
![](https://i.ibb.co/p1j5dD7/p2.png)

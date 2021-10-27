package main

import (
	Graph "GraphTheoryTask/src/graph"
	Algorithm "GraphTheoryTask/src/graph/GraphAlgorithm"
)

func main() {
	//vertex := []string{"v1", "v2", "v3", "v4", "v5", "v6", "v7"}
	//edge := [][]int{
	//	{0, 2, 0, 1, 0, 0, 0},
	//	{0, 0, 0, 3, 10, 0, 0},
	//	{4, 0, 0, 0, 0, 5, 0},
	//	{0, 0, 2, 0, 2, 8, 4},
	//	{0, 0, 0, 0, 0, 0, 7},
	//	{0, 0, 0, 0, 0, 0, 0},
	//	{0, 0, 0, 0, 0, 1, 0},
	//}
	vertex := []string{"v1", "v2", "v3", "v4", "v5"}
	edge := [][]int{
		{0, 1, 5, 0, 3},
		{0, 0, 2, 0, 0},
		{0, 0, 0, 0, -4},
		{0, 0, 2, 0, 0},
		{0, 0, 0, 3, 0},
	}
	g := new(Graph.Graph)
	g.InitGraph(vertex, edge)
	g.PrintVertex()
	g.PrintEdge()
	a := new(Algorithm.SPFA)
	a.Run(g, 0)
	a.Print()
}

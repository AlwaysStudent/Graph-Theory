package graph

import "fmt"

type Graph struct {
	Vertex []string
	Edge [][]int
}

func (g *Graph)InitGraph(vertex []string, edge [][]int) {
	g.Vertex = vertex[:]
	g.Edge = edge[:][:]
}

func (g *Graph)PrintVertex() {
	for i := range g.Vertex {
		fmt.Printf("%v ", g.Vertex[i])
	}
	fmt.Println()
}

func (g *Graph)PrintEdge() {
	for i := 0; i < len(g.Edge); i++ {
		for j := range g.Edge[i] {
			fmt.Printf("%v ", g.Edge[i][j])
		}
		fmt.Println()
	}
}

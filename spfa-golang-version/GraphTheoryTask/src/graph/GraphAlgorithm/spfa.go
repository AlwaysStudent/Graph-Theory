package GraphAlgorithm

import (
	graph "GraphTheoryTask/src/graph"
	queue "GraphTheoryTask/src/graph/GraphAlgorithm/DataStructure"
	"fmt"
	"math"
)

type SPFA struct {
	From int
	G *graph.Graph
	Distance []int
	PreVertex [][]int
	Visited []bool
	Flag []bool
	Count []int
	IsNegative bool
}

func (spfa *SPFA)Run(graph2 *graph.Graph, vertex int) {
	spfa.G = graph2
	spfa.From = vertex
	vertexNumber := len(spfa.G.Vertex)
	for i := 0;i < vertexNumber;i++ {
		spfa.Distance = append(spfa.Distance, math.MaxInt)
		spfa.Visited = append(spfa.Visited, false)
		spfa.PreVertex = append(spfa.PreVertex, []int{-1})
		spfa.Flag = append(spfa.Flag, false)
		spfa.Count = append(spfa.Count, 0)
	}
	spfa.Distance[vertex] = 0
	spfa.Count[vertex] ++
	q := queue.NewQueue()
	q.Push(vertex)
	for !q.IsEmpty() {
		temp := q.Pop()
		for i := 0; i < vertexNumber; i++ {
			if spfa.G.Edge[temp][i] != 0 {
				if spfa.G.Edge[temp][i] + spfa.Distance[temp] == spfa.Distance[i]{
					var flag bool
					for _, k := range spfa.PreVertex[i] {
						if k == temp {
							flag = true
						}
					}
					if !flag {
						spfa.PreVertex[i] = append(spfa.PreVertex[i], temp)
					}
				}
				if spfa.G.Edge[temp][i] + spfa.Distance[temp] < spfa.Distance[i] {
					spfa.Distance[i] = spfa.G.Edge[temp][i] + spfa.Distance[temp]
					spfa.PreVertex[i] = []int{temp}
					if spfa.Flag[i] == false {
						q.Push(i)
						spfa.Count[i] ++
						spfa.Flag[i] = false
					}
				}
			}
			if spfa.Count[i] > vertexNumber {
				spfa.IsNegative = true
				return
			}
		}
		spfa.Flag[temp] = false
		spfa.Visited[temp] = true
	}
	return
}

func (spfa *SPFA)Print() {
	var tempStringList []string
	var count []int
	for i := 0; i < len(spfa.PreVertex); i++ {
		tempStringList = append(tempStringList, "")
		count = append(count, 0)
		temp := i
		for temp != -1 {
			tempStringList[i] = "[" + spfa.G.Vertex[temp] + "]->" + tempStringList[i]
			t := temp
			temp = spfa.PreVertex[temp][0]
			if temp != -1 {
				count[i] += spfa.G.Edge[temp][t]
			}
		}
		fmt.Println("From [" + spfa.G.Vertex[spfa.From] + "] To [" + spfa.G.Vertex[i] + "] : " + tempStringList[i] + "[Finish]")
		fmt.Println("Distance: ", count[i])
	}
}

//func StringReverse(s string) string {
//	f := func(s string) *[]rune {
//		var temp []rune
//		for _, i := range []rune(s) {
//			defer func(v rune) {
//				temp = append(temp, v)
//			}(i)
//		}
//		return &temp
//	}(s)
//	return string(*f)
//}


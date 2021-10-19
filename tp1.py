from ortools.linear_solver import pywraplp
import networkx as nx

def sudoku(N):
	graph = nx.Graph()
	print(N)

	print(N^2)
	print(N^4)
	print("ola")

	# nodos
	for i in range(1,(N^4)+1):
		print(i)
		graph.add_node(i)

	# colunas
	for i in range(1,(N^4)+1):
		for j in range(i+1,(N^4)+1,N^2):
			graph.add_edge(i,j)

	# linhas
	lim = N^2
	for casa in range(1,(N^4)+1):
		for k in range(casa+1,lim+1):
			graph.add_edge(casa, casa+k)
		if casa % N^2 == 0:
			lim = lim+N^2

	print(graph.nodes.data())
	nx.draw(graph)
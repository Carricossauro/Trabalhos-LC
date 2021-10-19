from ortools.linear_solver import pywraplp
import networkx as nx

def ip_color_op(graph,k):
    # criar solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    #criar dicionario de variaveis x{i,j} 
    x = {}
    for i in graph:
      x[i] = {}
      for j in range(k):
        x[i][j] = solver.BoolVar('x[%i][%i]' % (i,j))
      
    # vertices adjacentes tem cores diferentes
    for o in graph:
      for d in graph[o]:
        for j in range(k):
          solver.Add(x[o][j] + x[d][j] <= 1)

    # Manter o que ja tem cor
    for v in graph:
      if 'color' in graph.nodes[v]:
        solver.Add(x[v][graph.nodes[v]['color']] == 1)
    

    for i in graph:
      solver.Add(sum([x[i][j] for j in range(k)]) == 1)  # ou solver.Add(sum(list(x[i].values())) == 1) 

    # invocar solver e colorir o grafo

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        for i in graph:
            for j in range(k):
                if round(x[i][j].solution_value())==1:
                    graph.nodes[i]['color'] = j
        return True
    else:
        return False

def sudoku(N):
  graph = nx.Graph()
  
  # nodos
  for i in range(1,(N**4)+1):
    graph.add_node(i)
    
  # colunas
  for i in range(1,(N**4)+1):
    for j in range(i+N**2,(N**4)+1,N**2):
      graph.add_edge(i,j)
      
  # linhas
  lim = N**2
  for casa in range(1,(N**4)+1):
    for k in range(casa+1,lim+1):
      graph.add_edge(casa, k)
    if casa % N**2 == 0:
      lim = lim+N**2

  # quadrados
  dic = {}
  for i in range(N**2):
    dic[i] = []

  k = 0
  p = 1
  l = 0
  for i in range(1,N**4+1):
    dic[l + k].append(i)
    if i % N == 0:
      k = (k+1) % N
    if i % N**2 == 0:
      p+=1
      if p > N:
        l+=N
        p=1

  for lista in dic.values():
    for i in lista:
      for j in lista:
        if i != j:
          graph.add_edge(i,j)

  print(graph.edges())
  assert ip_color(graph, N**2)
  # draw_with_colors(graph)

  return graph

def print_sudoku(graph, N):
  # "%02d"
  num = 1
  for i in range(N**2):
    for j in range(N):
      print(" ", end ="")
      for k in range(N):
        if 'color' in graph.nodes[num]:
          print("%02d" % (graph.nodes[num]['color']+1), end =" ")
        else:
          print("..", end =" ")
        num+=1
      if j != N-1:
        print("|", end ="")
    print("\n", end ="")
    if (i+1) % N == 0 and i != N**2-1:
      for y in range(N):
        for x in range((3*N)+1):
          print("-", end ="")
        if y != N-1:
          print("+", end ="")
        else:
          print("\n", end ="")
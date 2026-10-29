from dolfin import *
parameters["reorder_dofs_serial"] = False

mesh = Mesh() 
editor = MeshEditor() 
editor.open(mesh, 'triangle', 2, 2) 
editor.init_vertices(9) 
editor.init_cells(8) 
editor.add_vertex(0, [0.0, 0.0])
editor.add_vertex(1, [0.0, 0.5])
editor.add_vertex(2, [0.0, 1.0])
editor.add_vertex(3, [0.5, 0.0])
editor.add_vertex(4, [0.5, 0.5])
editor.add_vertex(5, [0.5, 1.0])
editor.add_vertex(6, [1.0, 0.0])
editor.add_vertex(7, [1.0, 0.5])
editor.add_vertex(8, [1.0, 1.0])

editor.add_cell(0, [0, 1, 4])
editor.add_cell(1, [0, 4, 3])
editor.add_cell(2, [1, 2, 5])
editor.add_cell(3, [1, 5, 4])
editor.add_cell(4, [3, 4, 7])
editor.add_cell(5, [3, 7, 6])
editor.add_cell(6, [4, 5, 8])
editor.add_cell(7, [4, 8, 7])
editor.close()


V = FunctionSpace(mesh , "CG", 1)

k = Constant(1.0)
f = Constant(10.0)
g = Constant(0.7)

def gamma1(x, on_boundary):
    return on_boundary 
bc = DirichletBC(V, g, gamma1)

u = TrialFunction(V)
v = TestFunction(V)

a = k * inner(grad(u), grad(v)) * dx + u * v * ds 
L = f * v * dx

u = Function(V)
solve(a == L, u, bc)
File("solution.pvd") << u


u_values = u.vector().get_local() 
vertexToDof = vertex_to_dof_map(V)
print(f"1. Общее количество DOF (размерность вектора решения u): {len(u_values)}\n")

print("2. Индексы DOF с координатами и значениями функции u на них:")
for vi in range(mesh.num_vertices()):
    dof = vertexToDof[vi]           
    value = u_values[dof]
    vertex = Vertex(mesh, vi)
    x = vertex.point().x()
    y = vertex.point().y()
    print(f"Vi({vi}) DOF({dof}): ({x:.4f}, {y:.4f}) → u = {value:.4f}")

cell_idx = 4
cell = Cell(mesh, cell_idx)
vertices = cell.entities(0)
dofs = [vertexToDof[vi] for vi in vertices]
values = [u_values[dof] for dof in dofs]
average = sum(values) / len(values)
           
print(f"\n3. DOF ячейки {cell_idx}: {dofs} - ", [f"{v:.4f}" for v in values])
    
print(f"\n4. Среднее значение функции u по DOF ячейки {cell_idx} - ({average:.6f}):")

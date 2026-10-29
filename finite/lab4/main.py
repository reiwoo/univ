from dolfin import *

#mesh = UnitSquareMesh(2, 2)
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


print(f"Mesh: {mesh.num_vertices()} nodes, {mesh.num_cells()} cells\n")
print("1. Center of cells:")
for cell in cells(mesh):
    mid = cell.midpoint()
    print(f"Cell {cell.index()}: ({mid.x():.4f}, {mid.y():.4f})")
print()


print("2. Coordinates of nodes:")
coords = mesh.coordinates()
for i, (x, y) in enumerate(coords):
    print(f"Node {i}: ({x:.4f}, {y:.4f})")
print()


print("3. Index of nodes of cells:")
for cell in cells(mesh):
    vertex_indixes = cell.entities(0)
    print(f"Cell {cell.index():2d}: Nodes: {list(vertex_indixes)}")
print()

print("4. Nodes on borders:")
for vi in range(mesh.num_vertices()):
    vertex = Vertex(mesh, vi)
    xx = vertex.point().x()
    yy = vertex.point().y()                

    borders = []                  
    if abs(xx) < DOLFIN_EPS:
        borders.append("Left")
    if abs(xx - 1.0) < DOLFIN_EPS:
        borders.append("Right")
    if abs(yy) < DOLFIN_EPS:
        borders.append("Bottom")
    if abs(yy - 1.0) < DOLFIN_EPS:
        borders.append("Top")

    if borders:
        borders_str = " + ".join(borders)
        print(f'Node {vi} ({xx:.6f}, {yy:.6f}) : {borders_str} Border')
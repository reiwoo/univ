from dolfin import *
import numpy

parameters["reorder_dofs_serial"] = False
N = 5
mesh = UnitIntervalMesh(N)

k = 0.5
r = 0.1
f = 0.0

Nc = mesh.num_cells()
NN = mesh.num_vertices()
AA = numpy.zeros((NN, NN))
FF = numpy.zeros(NN)
for ci in range(Nc):
    cell = Cell(mesh, ci)
    vertices = cell.entities(0)
    vert0 = Vertex(mesh, vertices[0])
    vert1 = Vertex(mesh, vertices[1])
    h = abs(vert0.point().x() - vert1.point().x())
    dof0 = vertices[0]
    dof1 = vertices[1]
    AA[dof0][dof0] += 1.0 / h * k + h / 6 * 2 * r
    AA[dof1][dof0] += -1.0/ h * k + h/6*r
    AA[dof0][dof1] += -1.0/ h * k + h/6*r
    AA[dof1][dof1] += 1.0 / h * k + h / 6 * 2 * r
    
    #FF[dof0] += f * h / 2
    #FF[dof1] += f * h / 2
print("My Matrix (before BC):")
print(AA)
print(FF)
dof_leftbc = 0
AA[dof_leftbc, :] = 0.0
AA[dof_leftbc, dof_leftbc] = 1.0
FF[dof_leftbc] = 5.0

dof_rightbc = 5
AA[dof_rightbc, :] = 0.0
AA[dof_rightbc, dof_rightbc] = 1.0 
FF[dof_rightbc] = 0.0
print("My Matrix (after BC):")
print(AA)
print(FF)

u_sol = numpy.linalg.solve(AA, FF)
print("My Solve:")
print(u_sol)


V = FunctionSpace(mesh, "CG", 1)
u = TrialFunction(V)
v = TestFunction(V)
kk = Constant(k)
rr = Constant(r)
ff = Constant(f)
a = inner(kk * grad(u), grad(v)) * dx + rr * u * v * dx
L = ff*v*dx
A = Matrix()
assemble(a, A)
b = Vector()
assemble(L, b)

def left_boundary(x, on_boundary):
    return on_boundary and x[0] < DOLFIN_EPS
def right_boundary(x, on_boundary):
    return on_boundary and x[0] > 1.0 - DOLFIN_EPS

bc_left = DirichletBC(V, Constant(5.0), left_boundary)
bc_right = DirichletBC(V, Constant(0.0),  right_boundary)
bc_left.apply(A, b)
bc_right.apply(A, b)

sol = Function(V)
solve(A, sol.vector (), b)
print()
print("FEniCS solution vector after applying DirichletBC")
print(sol.vector().get_local())
solve(a == L, sol)
File("./results/solution.pvd") << u
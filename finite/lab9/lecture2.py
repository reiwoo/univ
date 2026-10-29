from dolfin import *
import numpy

parameters["reorder_dofs_serial"] = False

N = 2
mesh = UnitSquareMesh(N, N)
k = 0.7
Nc = mesh.num_cells()
NN = mesh.num_vertices()

def determinant(aa):
  deta = aa[0][0]*(aa[1][1]*aa[2][2] - aa[1][2]*aa[2][1]) \
        -aa[0][1]*(aa[1][0]*aa[2][2] - aa[1][2]*aa[2][1]) \
        +aa[0][2]*(aa[1][0]*aa[2][1] - aa[1][1]*aa[2][0])
  return abs(deta)

def determinantX(aa, ind):
  deta = 0
  if ind == 0:
    deta = aa[2][2] - aa[1][2]
  if ind == 1:
    deta = aa[0][2] - aa[2][2]
  if ind == 2:
    deta = aa[1][2] - aa[0][2]
  return -deta

def determinantY(aa, ind):
  deta = 0
  if ind == 0:
    deta = aa[2][1] - aa[1][1]
  if ind == 1:
    deta = aa[0][1] - aa[2][1]
  if ind == 2:
    deta = aa[1][1] - aa[0][1]
  return deta

AA = numpy.zeros((NN, NN))
for ci in range(Nc):
  cell = Cell(mesh, ci)
  vertices = cell.entities(0)
  nloc = 3
  aa = numpy.zeros((nloc, nloc))
  for j in range(nloc):
    vertex = Vertex(mesh, vertices[j])
    aa[j][0] = 1.0
    aa[j][1] = vertex.point().x()
    aa[j][2] = vertex.point().y()
  da = determinant(aa)
  for j1 in range(nloc):
    dof1 = vertices[j1]
    dphidx1 = determinantX(aa, j1)/da
    dphidy1 = determinantY(aa, j1)/da
    for j2 in range(nloc):
      dof2 = vertices[j2]
      dphidx2 = determinantX(aa, j2)/da
      dphidy2 = determinantY(aa, j2)/da
      AA[dof1][dof2] += k*(dphidx1*dphidx2 \
			+ dphidy1*dphidy2 )*(da /2)
  
   
print("Our matrix\n")
print(AA)
V = FunctionSpace(mesh, "CG", 1)
u = TrialFunction(V)
v = TestFunction(V)
kk = Constant(k)
f = Constant(1.0)
a = inner(kk * grad(u), grad(v))*dx
L = f*v*dx
A = Matrix()
assemble(a, A)
b = Vector()
assemble(L, b)
print("\nFEniCS matrix\n")
print(A.array())

print(A.array ())
print("\nFEniCS vector b\n")
print(b. get_local ())
print("\nLeft boundary vertices\n")
for vi in range(NN):
	vertex = Vertex(mesh , vi)
	point = vertex.point ()
	x = point.x()
	y = point.y()
	if x < DOLFIN_EPS :
		print("vi: %i, point(%g, %g)" % (vi , x, y))
def boundary(x):
	return x[0] < DOLFIN_EPS

g = Constant (3.0)
bc = DirichletBC (V, g, boundary)
bc.apply(A)
bc.apply(b)

print("\nFEniCS matrix after applying DirichletBC\n")

print(A.array ())

print("\nFEniCS vector b after applying DirichletBC\n")

print(b.get_local())

sol = Function(V)
solve(A, sol.vector (), b)

print("\nFEniCS solution vector after applying DirichletBC\n")
print(sol.vector().get_local())

from dolfin import *
import numpy

parameters["reorder_dofs_serial"] = False
N = 2
mesh = UnitIntervalMesh(N)

k = 1.0
r = 1.0
f = 1.0
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
    print(h)
    dof0 = vertices[0]
    dof1 = vertices[1]
    #AA[dof0][dof0] += 1.0 / h * k + h / 6 * 2 * r
    #AA[dof1][dof0] += -1.0/ h * k + h/6*r
    #AA[dof0][dof1] += -1.0/ h * k + h/6*r
    #AA[dof1][dof1] += 1.0 / h * k + h / 6 * 2 * r
    
    #AA[dof0][dof0] +=  h / 6 * 2 
    #AA[dof1][dof0] +=  h/6
    #AA[dof0][dof1] +=  h/6
    #AA[dof1][dof1] += h / 6 * 2 
    FF[dof0] += 1
    FF[dof1] += 1
    print(FF)
#print(AA)
print() 

V = FunctionSpace(mesh, "CG", 1)
u = TrialFunction(V)
v = TestFunction(V)
kk = Constant(k)
rr = Constant(r)
a = inner(kk * grad(u), grad(v)) * dx + rr * u * v * dx
A = Matrix()
assemble(a, A)
#print(A.array()) 
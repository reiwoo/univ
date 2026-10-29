from dolfin import *
import matplotlib.pyplot as plt

mesh = Mesh("mesh.xml")
boundaries = MeshFunction("size_t", mesh, "mesh_facet_region.xml")
domains = MeshFunction('size_t', mesh, 'mesh_physical_region.xml')
ds = Measure('ds', domain=mesh, subdomain_data=boundaries)
dx = Measure('dx', domain=mesh, subdomain_data=domains)

V = FiniteElement("RT", mesh.ufl_cell(), 1) 
P = FiniteElement("DG", mesh.ufl_cell(), 0)
W = FunctionSpace(mesh, MixedElement(V, P))

(q, u) = TrialFunctions(W)
(r, v) = TestFunctions(W)
n = FacetNormal(mesh)

k = Constant(1.0)
f = Constant(10.0)
g2 = Constant((0.7,0.7))
g = Constant(0.7)
bcs = DirichletBC(W.sub(1), g, boundaries, 2)

a = (inner(q, r)/k)*dx \
    - div(r)*u*dx \
    + div(q)*v*dx \
    + inner(q,n)*inner(r,n)*ds(2)

L = f*v*dx - g*inner(r,n)*ds(1)

w = Function(W)
solve(a == L, w, bcs)
(q,u) = w.split()
fileq = File('./results/q.pvd') 
fileu = File('./results/u.pvd') 

fileq << q
fileu << u


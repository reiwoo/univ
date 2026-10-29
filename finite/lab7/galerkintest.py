from dolfin import *

mesh = Mesh("mesh.xml")
boundaries = MeshFunction("size_t", mesh, "mesh_facet_region.xml")
domains = MeshFunction('size_t', mesh, 'mesh_physical_region.xml')
ds = Measure('ds', domain=mesh, subdomain_data=boundaries)
dx = Measure('dx', domain=mesh, subdomain_data=domains)

k = Constant(1.0)
f = Constant(10.0)
g1 = Constant(0.7)

V = FunctionSpace(mesh, "DG", 1)
u = TrialFunction(V)
v = TestFunction(V)

#class RobinBoundary(SubDomain): 
#	def inside(self, x, on_boundary ): 
#		return on_boundary and (x[0] < DOLFIN_EPS or x[1] < DOLFIN_EPS )


n = FacetNormal(mesh)
h = CellDiameter(mesh)
h_avg = (h('+') + h('-')) / 2.0
alpha = Constant(4.0)
gamma = Constant(8.0)
#RobinBoundary (). mark(boundaries , 1) 
bcs = DirichletBC(V, g1, boundaries, 2)

a = inner(k*grad(u), grad(v))*dx \
    - inner(avg(k*grad(v)), jump(u,n))*dS \
    - inner(jump(v,n), avg(k*grad(u)))*dS \
    + avg(k)*(alpha/h_avg)*inner(jump(v,n), jump(u,n))*dS \
    - inner(k*grad(v), u*n)*ds(1) \
    - inner(v*n, k*grad(u))*ds(1) \
    + k*(gamma/h)*u*v*ds(1) \
    + u*v*ds(2)  #

L = f * v * dx \
    - g1*inner(k*grad(v),n)*ds(1) \
    + k*(gamma/h)*g1*v*ds(1) \
    #

u = Function(V)
solve(a == L, u)
File("./results/galerkin.pvd") << u
from dolfin import *

mesh = Mesh("mesh.xml")
subdomains = MeshFunction("size_t", mesh, "mesh_physical_region.xml")
boundaries = MeshFunction("size_t", mesh, "mesh_facet_region.xml")
V = FunctionSpace(mesh, "CG", 1)
class HeterExpression(UserExpression):
    def eval_cell(self, value, x, ufc_cell):
        if subdomains[ufc_cell.index] == 1:
            value[0] = 1.0
        else:
            value [0] = 50.0

f = Constant(0.0)
k = HeterExpression(degree = 0)
g = Constant(0.0)
alp = Constant(10.0)
uout = Constant(20.0)
bc = DirichletBC(V, g, boundaries , 1)
u = TrialFunction(V)
v = TestFunction(V)
dx = Measure('dx', domain=mesh, subdomain_data=subdomains)
ds = Measure('ds', domain=mesh, subdomain_data=boundaries)
a = inner(k*grad(u), grad(v))*dx + alp*u*v*ds(3)
L = f*v*dx + alp*uout*v*ds(3)
u = Function(V)
solve(a == L, u, bc)
print( 'u(%g, %g) ' % (u.vector().min(), u.vector().max()))
u.rename( 'u ', '0 ')
file = File("./results/temperature.pvd")
file << u
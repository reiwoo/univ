from dolfin import * 
import numpy, sys

#N = 32
#mesh = UnitSquareMesh(N, N)
mesh = Mesh('mesh1.xml') 
domains = MeshFunction('size_t', mesh, 'mesh1_physical_region.xml') 
boundaries = MeshFunction('size_t', mesh, 'mesh1_facet_region.xml')
dx = Measure('dx', domain=mesh, subdomain_data=domains)
ds = Measure('ds', domain=mesh, subdomain_data=boundaries)

m=2
def R(u):
    return (1.0/3.0) * u**3
def DR(u):
    return (3.0/3.0) * u**2

k_val = Constant(0.5)
D = Constant((1.0, 1.0)) 
f = Constant(0.0)
g1 = Constant(1.0)
g2 = Constant(0.0)
def g1_boundary(x): 
	return x[0] < DOLFIN_EPS
def g2_boundary(x): 
	return x[0] > 1.0 - DOLFIN_EPS
V = FunctionSpace (mesh , 'Lagrange' , 1) 
u = TrialFunction(V) 
v = TestFunction(V) 

bc1 = DirichletBC(V, g1, boundaries, 2) 
bc2 = DirichletBC(V, g2, boundaries, 1)     
bcs = [bc1 , bc2]

#Define variational problem for initial guess (q(u)=1, i.e., m=0)
a = inner(grad(u), grad(v)) * dx 
L = f * v * dx
u_ = Function(V)
solve(a == L, u_, bcs)

bc1 = DirichletBC(V, g2, boundaries, 2) 
bc2 = DirichletBC(V, g2, boundaries, 1)  
bcs = [bc1 , bc2]

# Define variational problem for Newton iteration
du = TrialFunction(V)
a = (inner(k_val*grad(du),grad(v)) + DR(u_)*du*v + inner(D,grad(du))*v)*dx
L = -(inner(k_val*grad(u_),grad(v)) + R(u_)*v + inner(D,grad(u_))*v)*dx

#a = inner(q(u_)*grad(du),grad(v))*dx + inner(Dq(u_)*du*grad(u_),grad(v))*dx
#L = -inner(q(u_)*grad(u_), grad(v))*dx

#Newton iteration at the PDE level
du = Function(V)
u = Function(V)
omega =1.0
eps =1.0
tol = 1.0E-5
iter = 0
maxiter =25

while eps > tol and iter<maxiter:
	iter +=1
	print(iter, 'iteration', end=' ')
	solve(a == L, du, bcs) 
	eps = numpy.linalg.norm(du.vector(). get_local(), ord=numpy.Inf)
	print('Norm:', eps)
	u.vector()[:] = u_.vector() + omega*du.vector()
	u_.assign(u)

file = File('./results/newton.pvd') 
file << u
## Find max error
#u_exact = Expression("pow((pow(2, m+1)-1)*x[0] + 1, 1.0/(m+1)) - 1", m=m, degree=1)
#u_e = interpolate(u_exact, V)
#diff = numpy.abs(u_e.vector().get_local() - u.vector().get_local()).max()
#print ('Max error:', diff)

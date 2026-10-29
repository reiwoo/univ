from dolfin import *
import time

mesh = Mesh('mesh.xml') 
domains = MeshFunction('size_t', mesh, 'mesh_physical_region.xml') 
boundaries = MeshFunction('size_t', mesh, 'mesh_facet_region.xml') 
V = FunctionSpace(mesh, 'Lagrange', 1) 

dx = Measure('dx', domain=mesh, subdomain_data=domains)
ds = Measure('ds', domain=mesh, subdomain_data=boundaries)

f = Constant(0.0)
k = Constant(0.1)

bc_left = DirichletBC(V, Constant(2.0), boundaries, 1)
bc_right = DirichletBC(V, Constant(1.0), boundaries, 2)
bcs = [bc_left, bc_right]

u = TrialFunction(V) 
v = TestFunction(V)

a = k * inner(grad(u), grad(v)) * dx
L = f * v * dx

u = Function(V)
U = u.vector()
A = assemble(a)
b = assemble(L)

for bc in bcs:
  bc.apply(A, b)

solver = KrylovSolver('tfqmr', 'additive_schwarz')
cg_prm = solver.parameters["linear_algebra_backend"] = "Epetra"
cg_prm["absolute_tolerance"] = 1E-7     
cg_prm["relative_tolerance"] = 1E-4       
cg_prm["maximum_iterations"] = 1000 

start_time = time.time()
iter = solver.solve(A, U, b)
end_time = time.time()

print(f'Total iterations = {iter}')
print(f"Time: {end_time-start_time:.6f} s.")

File('./results/solution3D.pvd') << u
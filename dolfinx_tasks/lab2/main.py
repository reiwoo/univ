from mpi4py import MPI
import numpy as np
import ufl
from dolfinx import default_scalar_type, fem, io
from dolfinx.fem.petsc import LinearProblem
from dolfinx.io import gmsh as gmshio

GAMMA_L, GAMMA_R, GAMMA_B, GAMMA_T = 1, 2, 3, 4
OMEGA_OUT, OMEGA_IN = 10, 11
k_out, k_in = 1.0, 10.0

comm = MPI.COMM_WORLD

mesh_data = gmshio.read_from_msh("mesh.msh", comm, rank=0, gdim=2)
mesh, cell_tags, facet_tags = (
    mesh_data.mesh,
    mesh_data.cell_tags,
    mesh_data.facet_tags,
)

V = fem.functionspace(mesh, ("Lagrange", 1))
Q = fem.functionspace(mesh, ("DG", 0))
k = fem.Function(Q)
k.x.array[cell_tags.find(OMEGA_OUT)] = k_out
k.x.array[cell_tags.find(OMEGA_IN)] = k_in

fdim = mesh.topology.dim - 1
mesh.topology.create_connectivity(fdim, mesh.topology.dim)

def dirichlet(value, tag):
  dofs = fem.locate_dofs_topological(V, fdim, facet_tags.find(tag))
  return fem.dirichletbc(default_scalar_type(value), dofs, V)

bcs = [dirichlet(1.0, GAMMA_L), dirichlet(0.0, GAMMA_R)]


dx = ufl.Measure("dx", domain=mesh, subdomain_data=cell_tags)
ds = ufl.Measure("ds", domain=mesh, subdomain_data=facet_tags)
u, v = ufl.TrialFunction(V), ufl.TestFunction(V)

alpha, g_B = 5.0, 0.0
beta, u_T = 5.0, 5.5

a = (
    k * ufl.inner(ufl.grad(u), ufl.grad(v)) * dx
    + alpha * u * v * ds(GAMMA_B)
    + beta * u * v * ds(GAMMA_T)
)
L = alpha * g_B * v * ds(GAMMA_B) + beta * u_T * v * ds(GAMMA_T)


problem = LinearProblem(
    a,
    L,
    bcs=bcs,
    petsc_options={"ksp_type": "preonly", "pc_type": "lu"},
)
uh = problem.solve()
uh.name = "u"
k.name = "k"

with io.XDMFFile(comm, "solution.xdmf", "w") as xdmf:
  xdmf.write_mesh(mesh)
  xdmf.write_meshtags(cell_tags, mesh.geometry)
  xdmf.write_meshtags(facet_tags, mesh.geometry)
  xdmf.write_function(k)
  xdmf.write_function(uh)
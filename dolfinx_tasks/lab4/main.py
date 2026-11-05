from mpi4py import MPI
import basix.ufl
import ufl
from dolfinx import fem, io
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

cell = mesh.basix_cell()
RT = basix.ufl.element("RT", cell, 1)
DG = basix.ufl.element("DG", cell, 0)
W = fem.functionspace(mesh, basix.ufl.mixed_element([RT, DG]))

Q0 = fem.functionspace(mesh, ("DG", 0))
k = fem.Function(Q0)
k.x.array[cell_tags.find(OMEGA_OUT)] = k_out
k.x.array[cell_tags.find(OMEGA_IN)] = k_in

dx = ufl.Measure("dx", domain=mesh, subdomain_data=cell_tags)
ds = ufl.Measure("ds", domain=mesh, subdomain_data=facet_tags)
n = ufl.FacetNormal(mesh)

(q, u) = ufl.TrialFunctions(W)
(r, v) = ufl.TestFunctions(W)

g_L, g_R = 1.0, 0.0
alpha, g_B = 5.0, 0.0
beta, u_T = 5.0, 0.5

a = (
    (1 / k) * ufl.inner(q, r) * dx
    + (1 / alpha) * ufl.dot(q, n) * ufl.dot(r, n) * ds(GAMMA_B)
    + (1 / beta) * ufl.dot(q, n) * ufl.dot(r, n) * ds(GAMMA_T)
    - u * ufl.div(r) * dx
    + v * ufl.div(q) * dx
)
L = -(
    g_L * ufl.dot(r, n) * ds(GAMMA_L)
    + g_R * ufl.dot(r, n) * ds(GAMMA_R)
    + g_B * ufl.dot(r, n) * ds(GAMMA_B)
    + u_T * ufl.dot(r, n) * ds(GAMMA_T)
)

#https://jsdokken.com/dolfinx-tutorial/stable/chapter4/mixed_poisson.html
problem = LinearProblem(
    a,
    L,
    petsc_options={
        "ksp_type": "preonly",
        "pc_type": "lu",
        "pc_factor_mat_solver_type": "mumps",
        "ksp_error_if_not_converged": True,
        "mat_mumps_icntl_24": 1,
        "mat_mumps_icntl_25": 0,
    },
    petsc_options_prefix="mixed_poisson_direct",
)

w = problem.solve()
q_h = w.sub(0).collapse()
u_h = w.sub(1).collapse()
u_h.name = "u"
q_h.name = "q"
k.name = "k"

Q_out = fem.functionspace(mesh, ("DG", 0, (2,)))
q_out = fem.Function(Q_out)
q_out.interpolate(q_h)
q_out.name = "q"

with io.XDMFFile(comm, "solution.xdmf", "w") as xdmf:
  xdmf.write_mesh(mesh)
  xdmf.write_meshtags(cell_tags, mesh.geometry)
  xdmf.write_meshtags(facet_tags, mesh.geometry)
  xdmf.write_function(k)
  xdmf.write_function(u_h)
  xdmf.write_function(q_out)
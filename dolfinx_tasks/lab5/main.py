from mpi4py import MPI
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

V = fem.functionspace(mesh, ("DG", 0))
Q = fem.functionspace(mesh, ("DG", 0))
k = fem.Function(Q)
k.x.array[cell_tags.find(OMEGA_OUT)] = k_out
k.x.array[cell_tags.find(OMEGA_IN)] = k_in

dx = ufl.Measure("dx", domain=mesh, subdomain_data=cell_tags)
ds = ufl.Measure("ds", domain=mesh, subdomain_data=facet_tags)
dS = ufl.Measure("dS", domain=mesh)

n = ufl.FacetNormal(mesh)
h = ufl.CellDiameter(mesh)
h_avg = (h("+") + h("-")) / 2
k_avg = 2 * k("+") * k("-") / (k("+") + k("-"))

u, v = ufl.TrialFunction(V), ufl.TestFunction(V)

g_L, g_R = 1.0, 0.0
alpha, g_B = 5.0, 0.0
beta, u_T = 5.0, 0.5

alpha_g = 4.0
gamma_g = 8.0

a = (
    k * ufl.inner(ufl.grad(u), ufl.grad(v)) * dx
    - ufl.inner(ufl.avg(k * ufl.grad(u)), n("+")) * ufl.jump(v) * dS
    - ufl.inner(ufl.avg(k * ufl.grad(v)), n("+")) * ufl.jump(u) * dS
    + (alpha_g / h_avg) * k_avg * ufl.jump(u) * ufl.jump(v) * dS
    - k * ufl.inner(ufl.grad(u), n) * v * (ds(GAMMA_L) + ds(GAMMA_R))
    - k * ufl.inner(ufl.grad(v), n) * u * (ds(GAMMA_L) + ds(GAMMA_R))
    + (gamma_g / h) * k * u * v * (ds(GAMMA_L) + ds(GAMMA_R))
    + alpha * u * v * ds(GAMMA_B)
    + beta * u * v * ds(GAMMA_T)
)
L = (
    - k * ufl.inner(ufl.grad(v), n) * g_L * ds(GAMMA_L) + (gamma_g / h) * k * g_L * v * ds(GAMMA_L)
    - k * ufl.inner(ufl.grad(v), n) * g_R * ds(GAMMA_R) + (gamma_g / h) * k * g_R * v * ds(GAMMA_R)
    + alpha * g_B * v * ds(GAMMA_B)
    + beta * u_T * v * ds(GAMMA_T)
)

problem = LinearProblem(
    a,
    L,
    petsc_options={"ksp_type": "preonly", "pc_type": "lu"},
    petsc_options_prefix="tf",
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
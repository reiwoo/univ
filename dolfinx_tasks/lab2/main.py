import dolfinx.fem.petsc
from mpi4py import MPI
import numpy as np
import typing
import ufl


def u_ex(mod, x):
    return mod.sin(2 * mod.pi * x[0])


def setup_problem(
    N: int,
) -> typing.Tuple[dolfinx.fem.FunctionSpace, dolfinx.fem.Form, dolfinx.fem.Form]:
    """Set up bilinear and linear form of the singular Poisson problem

    Args:
        N (int): Number of elements in each direction of the mesh.

    Returns:
        The function space, the bilinear form and the linear form of the problem.

    """

    domain = dolfinx.mesh.create_unit_square(
        MPI.COMM_WORLD, N, N, cell_type=dolfinx.mesh.CellType.quadrilateral
    )
    V = dolfinx.fem.functionspace(domain, ("Lagrange", 1))
    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)

    x = ufl.SpatialCoordinate(domain)
    u_exact = u_ex(ufl, x)
    f = -ufl.div(ufl.grad(u_exact))
    n = ufl.FacetNormal(domain)
    g = -ufl.dot(ufl.grad(u_exact), n)

    F = ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
    F += ufl.inner(g, v) * ufl.ds
    F -= f * v * ufl.dx
    return V, *dolfinx.fem.form(ufl.system(F))

from petsc4py import PETSc

nullspace = PETSc.NullSpace().create(constant=True, comm=MPI.COMM_WORLD)
petsc_options = {
    "ksp_error_if_not_converged": True,
    "ksp_type": "preonly",
    "pc_type": "lu",
    "pc_factor_mat_solver_type": "mumps",
    "ksp_monitor": None,
}
ksp = PETSc.KSP().create(MPI.COMM_WORLD)
ksp.setOptionsPrefix("singular_direct")
opts = PETSc.Options()
opts.prefixPush(ksp.getOptionsPrefix())
for key, value in petsc_options.items():
    opts[key] = value
ksp.setFromOptions()
for key, value in petsc_options.items():
    del opts[key]
opts.prefixPop()
V, a, L = setup_problem(40)
A = dolfinx.fem.petsc.assemble_matrix(a)
A.assemble()
b = dolfinx.fem.petsc.assemble_vector(L)
b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES, mode=PETSc.ScatterMode.REVERSE)
ksp.setOperators(A)
assert nullspace.test(A)
A.setNullSpace(nullspace)
uh = dolfinx.fem.Function(V)
ksp.solve(b, uh.x.petsc_vec)
uh.x.scatter_forward()

ksp.destroy()
def compute_L2_error(uh: dolfinx.fem.Function) -> float:
    mesh = uh.function_space.mesh
    u_exact = u_ex(ufl, ufl.SpatialCoordinate(mesh))
    error_L2 = dolfinx.fem.form(ufl.inner(uh - u_exact, uh - u_exact) * ufl.dx)
    error_local = dolfinx.fem.assemble_scalar(error_L2)
    return np.sqrt(mesh.comm.allreduce(error_local, op=MPI.SUM))
print(f"Direct solver L2 error {compute_L2_error(uh):.5e}")
u_exact = u_ex(ufl, ufl.SpatialCoordinate(V.mesh))
ex_mean = V.mesh.comm.allreduce(
    dolfinx.fem.assemble_scalar(dolfinx.fem.form(u_exact * ufl.dx)), op=MPI.SUM
)
approx_mean = V.mesh.comm.allreduce(
    dolfinx.fem.assemble_scalar(dolfinx.fem.form(uh * ufl.dx)), op=MPI.SUM
)
print(f"Mean value of manufactured solution: {ex_mean}")
print(f"Mean value of computed solution (direct solver): {approx_mean}")
assert np.isclose(ex_mean, approx_mean), "Mean values do not match!"
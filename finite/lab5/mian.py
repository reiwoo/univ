from dolfin import *

mesh1 = Mesh('mesh1.xml')
domains1 = MeshFunction('size_t', mesh1, 'mesh1_physical_region.xml')
boundaries1 = MeshFunction('size_t', mesh1, 'mesh1_facet_region.xml')
mesh2 = Mesh('mesh2.xml')
domains2 = MeshFunction('size_t', mesh2, 'mesh2_physical_region.xml')
boundaries2 = MeshFunction('size_t', mesh2, 'mesh2_facet_region.xml')
mesh3 = Mesh('mesh3.xml')
domains3 = MeshFunction('size_t', mesh3, 'mesh3_physical_region.xml')
boundaries3 = MeshFunction('size_t', mesh3, 'mesh3_facet_region.xml')
mesh4 = Mesh('mesh4.xml')
domains4 = MeshFunction('size_t', mesh4, 'mesh4_physical_region.xml')
boundaries4 = MeshFunction('size_t', mesh4, 'mesh4_facet_region.xml')

V1 = FunctionSpace(mesh1, 'Lagrange', 1)
V2 = FunctionSpace(mesh2, 'Lagrange', 1)
V3 = FunctionSpace(mesh3, 'Lagrange', 1)
V4 = FunctionSpace(mesh4, 'Lagrange', 1)

dx1 = Measure('dx', domain=mesh1, subdomain_data=domains1)
dx2 = Measure('dx', domain=mesh2, subdomain_data=domains2)
dx3 = Measure('dx', domain=mesh3, subdomain_data=domains3)
dx4 = Measure('dx', domain=mesh4, subdomain_data=domains4)

u0_val = Constant(0.0)
g_L = Constant(10.0)
g_B = Constant(0.0)
g_T = Constant(0.0)
k = Constant(0.1)
T = 6.0
tau = 0.06

bc_1_1 = DirichletBC(V1, g_L, boundaries1, 1)
bc_2_1 = DirichletBC(V1, g_T, boundaries1, 3)
bc_3_1 = DirichletBC(V1, g_B, boundaries1, 4)
bcs1 = [bc_1_1, bc_2_1, bc_3_1]

bc_1_2 = DirichletBC(V2, g_L, boundaries2, 1)
bc_2_2 = DirichletBC(V2, g_T, boundaries2, 3)
bc_3_2 = DirichletBC(V2, g_B, boundaries2, 4)
bcs2 = [bc_1_2, bc_2_2, bc_3_2]

bc_1_3 = DirichletBC(V3, g_L, boundaries3, 1)
bc_2_3 = DirichletBC(V3, g_T, boundaries3, 3)
bc_3_3 = DirichletBC(V3, g_B, boundaries3, 4)
bcs3 = [bc_1_3, bc_2_3, bc_3_3]

bc_1_4 = DirichletBC(V4, g_L, boundaries4, 1)
bc_2_4 = DirichletBC(V4, g_T, boundaries4, 3)
bc_3_4 = DirichletBC(V4, g_B, boundaries4, 4)
bcs4 = [bc_1_4, bc_2_4, bc_3_4]

u0_1 = interpolate(u0_val, V1)
u0_2 = interpolate(u0_val, V2)
u0_3 = interpolate(u0_val, V3)
u0_4 = interpolate(u0_val, V4)


u1 = TrialFunction(V1)
v1 = TestFunction(V1)
u2 = TrialFunction(V2)
v2 = TestFunction(V2)
u3 = TrialFunction(V3)
v3 = TestFunction(V3)
u4 = TrialFunction(V4)
v4 = TestFunction(V4)
a1 = (u1/tau) * v1 * dx1 + k * inner(grad(u1), grad(v1)) * dx1
L1 = (u0_1/tau) * v1 * dx1
a2 = (u2/tau) * v2 * dx2 + k * inner(grad(u2), grad(v2)) * dx2
L2 = (u0_2/tau) * v2 * dx2
a3 = (u3/tau) * v3 * dx3 + k * inner(grad(u3), grad(v3)) * dx3
L3 = (u0_3/tau) * v3 * dx3
a4 = (u4/tau) * v4 * dx4 + k * inner(grad(u4), grad(v4)) * dx4
L4 = (u0_4/tau) * v4 * dx4
u1 = Function(V1)
u2 = Function(V2)
u3 = Function(V3)
u4 = Function(V4)
file1 = File('./results/solution_1.pvd')
file2 = File('./results/solution_2.pvd')
file3 = File('./results/solution_3.pvd')
file4 = File('./results/solution_4.pvd')


error_file = open('./results/errors.txt', 'w')  
error_file.write("time        L2_abs           L2_rel             H1_abs           H1_rel\n")  
t = 0
steps = 1
while t < T:
    t += tau
    solve(a1 == L1, u1, bcs1)
    solve(a2 == L2, u2, bcs2)
    solve(a3 == L3, u3, bcs3)
    solve(a4 == L4, u4, bcs4)
    file1 << u1
    file2 << u2
    file3 << u3
    file4 << u4
    u0_1.assign(u1)
    u0_2.assign(u2)
    u0_3.assign(u3)
    u0_4.assign(u4)
    if (steps % 5 == 0 ):     
        
        error_file.write(f"______________________________________________________________________________________\n")
        u4_proj1 = project(u4, V1)
        L2_abs1 = errornorm(u4_proj1, u1, 'L2')
        H1_abs1 = errornorm(u4_proj1, u1, 'H1')
        L2_norm1 = norm(u4_proj1, 'L2')
        H1_norm1 = norm(u4_proj1, 'H1')
        L2_rel1 = L2_abs1 / L2_norm1 if L2_norm1 > 1e-12 else 0.0
        H1_rel1 = H1_abs1 / H1_norm1 if H1_norm1 > 1e-12 else 0.0
        error_file.write(f"{t:.2f}      {L2_abs1:.3e}        {L2_rel1:.3e}           {H1_abs1:.3e}      {H1_rel1:.3e}\n")
        
       
        u4_proj2 = project(u4, V2)
        L2_abs2 = errornorm(u4_proj2, u2, 'L2')
        H1_abs2 = errornorm(u4_proj2, u2, 'H1')
        L2_norm2 = norm(u4_proj2, 'L2')
        H1_norm2 = norm(u4_proj2, 'H1')
        L2_rel2 = L2_abs2 / L2_norm2 if L2_norm2 > 1e-12 else 0.0
        H1_rel2 = H1_abs2 / H1_norm2 if H1_norm2 > 1e-12 else 0.0
        error_file.write(f"{t:.2f}      {L2_abs2:.3e}         {L2_rel2:.3e}          {H1_abs2:.3e}      {H1_rel2:.3e}\n")
        

        u4_proj3 = project(u4, V3)
        L2_abs3 = errornorm(u4_proj3, u3, 'L2')
        H1_abs3 = errornorm(u4_proj3, u3, 'H1')
        L2_norm3 = norm(u4_proj3, 'L2')
        H1_norm3 = norm(u4_proj3, 'H1')
        L2_rel3 = L2_abs3 / L2_norm3 if L2_norm3 > 1e-12 else 0.0
        H1_rel3 = H1_abs3 / H1_norm3 if H1_norm3 > 1e-12 else 0.0
        error_file.write(f"{t:.2f}      {L2_abs3:.3e}         {L2_rel3:.3e}          {H1_abs3:.3e}      {H1_rel3:.3e}\n")
    
    steps += 1

error_file.close()
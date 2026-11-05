//gmsh -2 mesh.geo -o mesh.msh

lc  = 0.04;
lci = 0.02;

Point(1) = {0, 0, 0, lc};
Point(2) = {1, 0, 0, lc};
Point(3) = {1, 1, 0, lc};
Point(4) = {0, 1, 0, lc};

Line(1) = {1, 2};
Line(2) = {2, 3}; 
Line(3) = {3, 4};
Line(4) = {4, 1};

Point(5) = {0.5, 0.5, 0, lci};
Point(6) = {0.7, 0.5, 0, lci};
Point(7) = {0.5, 0.7, 0, lci};
Point(8) = {0.3, 0.5, 0, lci};
Point(9) = {0.5, 0.3, 0, lci};

Circle(5) = {6, 5, 7};
Circle(6) = {7, 5, 8};
Circle(7) = {8, 5, 9};
Circle(8) = {9, 5, 6};

Curve Loop(1) = {1, 2, 3, 4};
Curve Loop(2) = {5, 6, 7, 8};

Plane Surface(1) = {1, 2};
Plane Surface(2) = {2};

Physical Curve("Gamma_L", 1) = {4};
Physical Curve("Gamma_R", 2) = {2};
Physical Curve("Gamma_B", 3) = {1};
Physical Curve("Gamma_T", 4) = {3};
Physical Curve("Interface", 5) = {5, 6, 7, 8};

Physical Surface("Omega_out", 10) = {1};
Physical Surface("Omega_in",  11) = {2};

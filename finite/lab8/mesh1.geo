SetFactory("OpenCASCADE");

H = 1.0;
L = 2.5;

Point(1) = {0, 0, 0, 0.03};
Point(2) = {L, 0, 0, 0.03};
Point(3) = {L, H, 0, 0.03};
Point(4) = {0, H, 0, 0.03};

Line(1) = {1, 2};  
Line(2) = {2, 3};  
Line(3) = {3, 4};
Line(4) = {4, 1};

Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

Physical Curve(1) = {2};
Physical Curve(2) = {4};
Physical Curve(3) = {1, 3};
Physical Surface(1) = {1};

Mesh 2;
Mesh.MshFileVersion = 2;
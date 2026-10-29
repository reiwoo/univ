SetFactory("OpenCASCADE");
Mesh.MshFileVersion = 2.0;

LX = 1;
LY = 1;
p1 = 1;

Point(1) = {0, 0, 0, p1};
Point(2) = {0, LY, 0, p1};
Point(3) = {LX, LY, 0, p1};
Point(4) = {LX, 0, 0, p1};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

//+
Physical Curve(5) = {1, 2, 3, 4};
//+
Curve Loop(2) = {2, 3, 4, 1};
//+
Plane Surface(1) = {2};
//+
Physical Surface(6) = {1};

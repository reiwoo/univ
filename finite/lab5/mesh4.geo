Mesh.MshFileVersion = 2.0;

LX = 2;
LY = 1;
p = 0.2 / 32;

Point(1) = {0, 0, 0, p};
Point(2) = {0, LY, 0, p};
Point(3) = {LX, LY, 0, p};
Point(4) = {LX, 0, 0, p};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Point(5) = {0.5, 0.5, 0, p};
Point(6) = {0.5, 0.7, 0, p};
Point(7) = {0.3, 0.5, 0, p};
Point(8) = {0.5, 0.3, 0, p};
Point(9) = {0.7, 0.5, 0, p};
Point(10) = {1.5, 0.5, 0, p};
Point(11) = {1.7, 0.5, 0, p};
Point(12) = {1.5, 0.3, 0, p};
Point(13) = {1.3, 0.5, 0, p};
Point(14) = {1.5, 0.7, 0, p};

Circle(15) = {7, 5, 6};
Circle(16) = {6, 5, 9};
Circle(17) = {9, 5, 8};
Circle(18) = {8, 5, 7};
Circle(19) = {13, 10, 14};
Circle(20) = {14, 10, 11};
Circle(21) = {11, 10, 12};
Circle(22) = {12, 10, 13};

Line Loop(1) = {1, 2, 3, 4};
Line Loop(2) = {15, 16, 17, 18};
Line Loop(3) = {19, 20, 21, 22};
Plane Surface(1) = {1, 2, 3};
Physical Surface(1) = {1};

Physical Line(1) = {1};
Physical Line(2) = {3};
Physical Line(3) = {2};
Physical Line(4) = {4};
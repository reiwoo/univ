SetFactory("OpenCASCADE");
Mesh.MshFileVersion = 2.0;

lc = 0.02;

Point(1) = {0, 0, 0, lc};
Point(2) = {-0.25, -0.25, 0, lc};
Point(3) = {0.25, -0.25, 0, lc};
Point(4) = {0.25, 0.25, 0, lc};
Point(5) = {-0.25, 0.25, 0, lc};
Line(1) = {2, 3};
Line(2) = {3, 4};
Line(3) = {4, 5};
Line(4) = {5, 2};
Curve Loop(1) = {1, 2, 3, 4};  

Point(6) = {1, 0, 0, lc};
Point(7) = {0, 1, 0, lc};
Point(8) = {-1, 0, 0, lc};
Point(9) = {0, -1, 0, lc};
Circle(5) = {6, 1, 7};
Circle(6) = {7, 1, 8};
Circle(7) = {8, 1, 9};
Circle(8) = {9, 1, 6};
Curve Loop(2) = {5, 6, 7, 8};  


Plane Surface(1) = {2, 1};  
Physical Curve(2) = {1, 2, 3, 4};  
Physical Curve(1) = {5, 6, 7, 8}; 
Physical Surface(1) = {1}; 
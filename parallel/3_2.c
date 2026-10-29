#include <stdio.h>
#include <mpi.h>
#include <math.h>

//2. Реализовать параллельное численное решение задачи теплопроводности итерационным методом Якоби.
//   Задача одномерная и выглядит следующим образом:
//   -k*(d^2 u / dx^2) = 0, u = 1 при x = 0, u = 0 при x = 1.

int main(int argc, char** argv) {
    
    MPI_Finalize();
    return 0;
}
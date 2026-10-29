#include <stdio.h>
#include <mpi.h>
#include <math.h>

/* 
    1. Реализовать параллельное численное решение определенного интеграла 
   методом левых прямоугольников (или правых, или средних, или трапеций, как вам удобнее). 
   Вид интеграла выбираете сами.
*/

int main(int argc, char** argv) {

    double func(double x) {
        return sin(x);         
    }

    int rank, commsize;
    double a = 0.0, b = 1.0;
    long long n = 1000000000;   
    double start_time, end_time;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &commsize);

    MPI_Bcast(&n, 1, MPI_LONG_LONG, 0, MPI_COMM_WORLD);
    n -= n % commsize;
    
    double dx = (b - a) / n;
    long long perprocinter = n / commsize;
    
    start_time = MPI_Wtime();
    double local_sum = 0.0;
    for (long long i = 0; i < perprocinter; i++) {
        long long global_i = rank * perprocinter + i;
        double x = a + dx * global_i;
        local_sum += func(x);

    }

    double global_sum = 0.0;
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    end_time = MPI_Wtime();

    if (rank == 0) {
        double result = global_sum * dx;
        printf("Intervals Count: %lld - Procs: %d\n", n,commsize);
        printf("Calcu value: %.21f\n", result);
        printf("Exact value: %.21f\n", 1.0 - cos(1.0));
        printf("Error      : %.21f\n", result - (1.0 - cos(1.0)));
        printf("Time: %.4f s\n", end_time - start_time);

    }
    MPI_Finalize();
    return 0;
}
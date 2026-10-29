#include <omp.h>
#include <stdio.h>
#include <math.h>
#include <iostream>

/*  1. Реализовать параллельное вычисление числа Пи с помощью рядов\формул. 
    Существует много формул (Википедия поможет). Надо выбрать свой.  */

//g++ -Wall -fopenmp ./4_1.cc -o 4_1
//./4_1

using namespace std;

int main(int argc, char** argv) {
    omp_set_num_threads(6);
    const long num_steps = 1000000000;  
    double pi = 0.0;
    double step = 1.0 / (double)num_steps;

    double start_time = omp_get_wtime(); 
    #pragma omp parallel for reduction(+:pi)
    for (long i = 0; i < num_steps; i++) {
        double x = (i + 0.5) * step;
        pi += step * 4.0 / (1.0 + x * x);
    }
    double end_time = omp_get_wtime();  

    double time = end_time - start_time;
    double exact_pi = 3.141592653589793238462643383279502;  
    double error = pi - exact_pi; 

    printf("Calcu value: %.24f\n", pi);
    printf("Exact value: %.24f\n", exact_pi);
    printf("Error: %.24f\n", error);
    printf("Time: %.4f s\n", time);

    return 0;
}
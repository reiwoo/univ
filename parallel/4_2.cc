#include <omp.h>
#include <iostream>
#include <cmath>
#include <iomanip>
#include <random>
#include <vector>

/*
    2. Приблизьте число Пи методом Монте-Карло: генерируя случайные числа 
    внутри квадратной области и вписанной в неё окружности. Википедия поможет.
    Параллельность в этом случае подразумевается в том, что каждый процесс 
    должен будет выполнить этот процесс и в конце надо будет вывести на экран 
    среднее из всех полученных чисел Пи (в теории он должен получиться самым точным из всех).
    Показать погрешность полученных результатов порознь и после нахождения среднего по полученным Пи. */

//g++ -Wall -fopenmp ./4_2.cc -o 4_2
//./4_2

int main() {
    int num_threads = 8;
    omp_set_num_threads(num_threads);
    const long total_darts = 100000;
    std::vector<double> pi(num_threads, 0.0);
    std::vector<long> hits(num_threads, 0.0);

    double start_time = omp_get_wtime();

    #pragma omp parallel
    {
        int id = omp_get_thread_num();
        std::mt19937 gen(11 + id);
        std::uniform_real_distribution<double> dist(0.0, 1.0);

        long inside = 0;
        for (long i = 0; i < total_darts; ++i) {
            double x = dist(gen);
            double y = dist(gen);
            if (x*x + y*y <= 1.0)
                inside++;
        }
        hits[id] = inside;
        pi[id] = 4.0 * double(inside) / total_darts;
        #pragma omp critical
        {
            printf("Thread %2d : TotalDarts = %ld,  / Hit inside Circle = %ld,  / Pi = %.12f\n",
                id, total_darts, inside, pi[id]);
        }
    }

    double end_time = omp_get_wtime();

    double sum = 0.0;
    for (int i = 0; i < num_threads; i++) {
    sum += pi[i];
    }   
    double time = end_time - start_time;
    double calcpi = sum / num_threads;
    double exact_pi = 3.141592653589793238462643383279502;  
    double error = calcpi - exact_pi; 

    printf("Calcu value: %.24f\n", calcpi);
    printf("Exact value: %.24f\n", exact_pi);
    printf("Error: %.24f\n", error);
    printf("Time: %.4f s\n", time);
}
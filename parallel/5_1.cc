#include <omp.h>
#include <iostream>
#include <cmath>
#include <iomanip>
#include <random>
#include <vector>

/*
    1. У вас есть пароль. Для простоты, будем считать, что он состоит только из 4 букв нижнего регистра.
    Необходимо его подобрать. Используйте #pragma omp parallel for  */

//g++ -Wall -fopenmp ./5_1.cc -o 5_1
//./5_1

using namespace std;

int main() {
    omp_set_num_threads(3);

    string secret_pass = "mako";
    string found_password = "";
    bool found = false;

    double start_time = omp_get_wtime();

    #pragma omp parallel for shared(found, found_password)
    for (int a = 0; a < 26; a++) {
        for (int b = 0; b < 26; b++) {
            for (int c = 0; c < 26; c++) {
                for (int d = 0; d < 26; d++) {

                    if (found) { 
                        continue;
                    }
                    char s[5];
                    sprintf(s, "%c%c%c%c", 'a'+a, 'a'+b, 'a'+c, 'a'+d);

                    if (string(s) == secret_pass) {
                        #pragma omp critical
                        {
                            if (!found) {
                                found = true;
                                found_password = s;
                            }
                        }
                    }
                }
            }
        }
    }

    double end_time = omp_get_wtime();

    printf("Guesseed word: %s\n", found_password.c_str());
    printf("Time: %.4f s\n", end_time - start_time);
}
#include <iostream>
#include <cmath>
using namespace std;

double f1(double u, double uu, double v) { return (u*(2.4-u-6*uu-4*v)); }
double f2(double u, double uu, double v) { return (uu*(4-uu-u-10*v)); }
double g1(double u, double uu, double v) { return (-v*(1.0-0.25*u-4*uu+v)); }

int main() {
    int N=100;
    double D1=0.0001, D2=0.0002, D3=0.0001;
    double x[N+1], alpha[N+1],beta[N+1],c1,c2,c3;
    double u1[N+1][N+1],u2[N+1][N+1],v1[N+1][N+1];
    double tao=0.09, h=1.0/N, a1=D1*tao/(h*h), b1=a1;

    for (int i=0; i<N; i++) {   // в книге i<N, но мы исправим на <=N в Python
        x[i]=i*h;
        u1[i][0]=5*pow((x[i])-0.5,2)+0.2;
        u2[i][0]=3*pow((x[i])-0.5,2)+0.05;
        v1[i][0]=pow((x[i])-0.5,2)+0.3;
    }

    for (int j=0; j<N; j++) {
        // u1
        alpha[1]=0; beta[1]=0;
        u1[0][j+1]=1.45;
        for (int i=1; i < N; i++) {
            c1=2*a1+1;
            alpha[i+1]=b1/(c1-a1*alpha[i]);
            double d=u1[i][j]+f1(u1[i][j],u2[i][j],v1[i][j])*tao;
            beta[i+1]=(a1*beta[i]+d)/(c1-a1*alpha[i]);
        }
        u1[N][j+1]=beta[N]/(1-alpha[N]);
        for (int i=N-1; i>0; i--) {
            u1[i][j+1]=u1[i+1][j+1]*alpha[i+1]+beta[i+1];
        }

        // u2 (аналогично)
        a2=D2*tao/(h*h); b2=a2;
        alpha[1]=0; beta[1]=0;
        u2[0][j+1]=0.5;   // ← как на фото
        for (int i=1; i < N; i++) {
            c2=2*a2+1;
            alpha[i+1]=b2/(c2-a2*alpha[i]);
            double d=u2[i][j]+f2(u1[i][j],u2[i][j],v1[i][j])*tao;
            beta[i+1]=(a2*beta[i]+d)/(c2-a2*alpha[i]);
        }
        u2[N][j+1]=beta[N]/(1-alpha[N]);
        for (int i=N-1; i>0; i--) {
            u2[i][j+1]=u2[i+1][j+1]*alpha[i+1]+beta[i+1];
        }

        // v
        a3=D3*tao/(h*h); b3=a3;
        alpha[1]=0; beta[1]=0.5;   // ← как на фото
        v1[0][j+1]=0.3;            // ← как на фото
        for (int i=1; i < N; i++) {
            c3=2*a3+1;
            alpha[i+1]=b3/(c3-a3*alpha[i]);
            double d=v1[i][j]+g1(u1[i][j],u2[i][j],v1[i][j])*tao;
            beta[i+1]=(a3*beta[i]+d)/(c3-a3*alpha[i]);
        }
        v1[N][j+1]=beta[N]/(1-alpha[N]);
        for (int i=N-1; i>0; i--) {
            v1[i][j+1]=v1[i+1][j+1]*alpha[i+1]+beta[i+1];
        }
    }

    // Вывод финальных значений (как в книге)
    for (int i=0; i<N; i++) {
        cout << u1[i+1][N] << endl;
    }
    cout << endl;
    for (int i=0; i<N; i++) {
        cout << u2[i+1][N] << endl;
    }
    cout << endl;
    for (int i=0; i<N; i++) {
        cout << v1[i+1][N] << endl;
    }
    return 0;
}
import time
import math
import cupy as cp
import numpy as np
import matplotlib.pyplot as plt
#from numba import cuda
import copy
#@cuda.jit
def mandelbrot_gpu(xpixels=2000, maxiter=500, xmin= -1.7687782, xmax=-1.7687794, ymin=-0.0017384, ymax=-0.0017394):
    ypixels = round(xpixels / (xmax - xmin) * (ymax - ymin))
    x = cp.linspace(xmin, xmax, xpixels, dtype=cp.float64)
    y = cp.linspace(ymin, ymax, ypixels, dtype=cp.float64)
    #x = cuda.blockIdx.x
    #y = cuda.threadIdx.x
    X, Y = cp.meshgrid(x, y, indexing="ij")

    C = X + 1j * Y
    Z = cp.zeros_like(C)
    mat = cp.zeros(C.shape, dtype=cp.float64)

    for n in range(maxiter):
        mask = (Z.real * Z.real + Z.imag * Z.imag) <= 4.0
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        escaped = mask & (Z.real * Z.real + Z.imag * Z.imag > 4.0)
        mat[escaped] = n + 1 - cp.log(cp.log(cp.abs(Z[escaped]))) / math.log(2)

    return mat


def save_image_gpu(mat_gpu, filename="mandelbrot_gpu.png", cmap="summer", powern=0.5, dpi=300):
    mat_gpu = cp.power(mat_gpu, powern)
    mat = cp.asnumpy(mat_gpu)
    cmap_obj = copy.copy(plt.get_cmap(cmap))
    cmap_obj.set_under("black")
    plt.figure(figsize=(mat.shape[0] / dpi, mat.shape[1] / dpi))
    plt.imshow(mat.T, cmap=cmap_obj, vmin=1, origin="lower")
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.savefig(filename, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close()

start = time.time()
mat_gpu = mandelbrot_gpu(xpixels=3840, maxiter=500)
save_image_gpu(mat_gpu, "mandelbrot_gpu_4k.png")
print(f"GPU time: {time.time() - start:.2f} s")

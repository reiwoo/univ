import time, math
import cupy as cp
import matplotlib.pyplot as plt
#source ./pycuda_env/bin/activate

#W, H = 3840, 3200
W, H = 3840, 3200
#xmin, xmax = -1.7687794, -1.7687782
#ymin, ymax = -0.0017394, -0.0017384
xmin, xmax = -1.5, 1.5
ymin, ymax = -1.5, 1.5

N = 600
print(f"Grid: {W}x{H},  iterations: {N}")
start_time = time.time()

x = cp.linspace(xmin, xmax, W, dtype=cp.float64)
y = cp.linspace(ymin, ymax, H, dtype=cp.float64).reshape(H, 1)
Z = x + 1j * y

#C = -0.5251993 -0.5251993j
C = 0.35 + 0.35j
mask = cp.ones(Z.shape, dtype=bool)
print(f"Total Alive Pixels: {mask.size}")
image = cp.zeros(Z.shape, dtype=cp.float64)

for n in range(N):
    Z[mask] = Z[mask] * Z[mask] + C
    modulus = Z.real*Z.real + Z.imag*Z.imag
    escaped = mask & (modulus > 4.0)

    if escaped.any():
        # mat[x,y] = n + 1 - math.log(math.log(abs(z*z+c)))
        image[escaped] = n + 1 - cp.log2(cp.log(cp.sqrt(modulus[escaped])))
        #image[escaped] = n
        mask[escaped] = False

    if not mask.any():
        print(f"All Pixels died")
        break
    
    if n % 100 == 0:
        print(f"Iter[{n}]: Alive {(int(mask.sum())/mask.size)*100:.12f}%")
        
#plt.figure(figsize=(16, 9))
print(f"RunTime {time.time() - start_time:.4f}s.")
plt.imsave("julia4k.png", cp.asnumpy(image), cmap="bone", origin="lower")
#plt.imshow(cp.asnumpy(image), cmap="bone", origin="lower")
#plt.show()
import numpy as np

def arx_model_solved(A, B, u, e=None):
    broj_odbiraka = len(u)
    
    A = np.flip(-A[1:])
    B = np.flip(B)

    a = len(A)
    b = len(B)

    padding = np.zeros(a)
    if e is None:
        e = np.zeros(len(u))

    y = np.zeros(broj_odbiraka + a)
    u = np.concatenate([padding, u])
    e = np.concatenate([padding, e])

    for i in range(a, broj_odbiraka + a):
        y[i] = A @ y[i - a: i] + B @ u[i - b: i] + e[i]

    return y[a:]

def nepoznati_model(u):
    A = np.array([1, -1.368, 0.7525])
    B = np.array([1.108])

    e = .03 * np.random.randn(len(u))

    return arx_model_solved(A, B, u, e)

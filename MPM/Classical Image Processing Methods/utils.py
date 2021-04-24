import numpy as np


def euc(p1, p2):
    return np.sqrt(((p1 - p2) ** 2).sum())


def cos(p1, p2):
    return (p1 * p2).sum() / (euc(p1, 0) * euc(p2, 0))

    
def create_circle(d):
    assert d % 2
    r = d//2
    arr = ((np.arange(d) - r)**2)[None, :]
    mask = arr + arr.T
    circle = np.zeros((d, d), dtype=np.uint8)
    circle[mask <= r**2] = 1
    return circle


def create_chess(d):
    val = np.random.binomial(1, 0.5)
    idxs = np.arange(d**2)
    flat = np.empty(d**2)
    flat[idxs % 2 == 0] = val
    flat[idxs % 2 == 1] = 1 - val
    return flat.reshape(d, d).astype(np.uint8)

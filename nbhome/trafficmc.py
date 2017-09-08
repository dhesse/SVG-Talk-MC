import numpy as np

class TrafficMC(object):
    """Nagel Schreckenberg traffic model.
    
    Args:
        N (int): Length of the road.
        k (int): Number of cars, bust be <= N.
        M (int): Speed limit.
        p (float): Probability of slowing down.
    """
    def __init__(self, N, k, M, p):
        assert(N >= k)
        self.N, self.p, self.M, self.k = N, p, M, k
        self.x = np.sort(np.random.choice(N, k, False))
        self.v = np.zeros(k, int)
        assert all(self.x[:-1] < self.x[1:])
    def step(self):
        """Take on step in simulation time.
        
        All the cars will perform the following actions.
        
        1. If going slower than the speed limit, increase speed by 1.
        2. If getting too close to the car in front, decrease the
           speed enough not to crash.
        3. With probability `p`, decrease the speed.
        """
        self.v = np.minimum(self.v + 1, self.M)
        d = (np.roll(self.x, -1) - self.x) % self.N
        self.v = np.minimum(self.v, d - 1)
        mask = np.random.uniform(size=self.k) < self.p
        self.v[mask] -= 1
        self.v = np.maximum(self.v, 0)
        self.x += self.v
        self.x %= self.N

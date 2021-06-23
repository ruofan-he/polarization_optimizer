import numpy as np

def kernel(x0,x1, t1, t2, t3):
    l0 = len(x0)
    l1 = len(x1)
    delta = np.array([[(x0[i] == x1[j]).all() for j in range(l1)] for i in range(l0)])
    x0 = np.array([[x0[i] for j in range(l1)] for i in range(l0)])
    x1 = np.array([[x1[j] for j in range(l1)] for i in range(l0)])

    assert len(x0.shape) == len(x1.shape)
    m_distance = np.linalg.norm(x0-x1, axis=2) if len(x0.shape) == 3 else np.abs(x0-x1)
    return t1*np.exp(-m_distance**2/ t2) + t3*delta

def x_regulation(x, dim):
    _x = x if type(x) == np.ndarray else np.array(x)
    assert len(_x.shape) == 1 or len(_x.shape) == 2
    if len(_x.shape) == 1:
        if dim == 1:
            _x = _x[:,np.newaxis]
        elif dim == len(_x.shape):
            _x = _x[np.newaxis,:]
        else: raise
    assert _x.shape[1] == dim
    return _x

def y_regulation(y):
    _y = y if type(y) == np.ndarray else np.array(y)
    assert len(_y.shape) == 1 or len(_y.shape) == 2
    if len(_y.shape) == 1: _y = _y[:,np.newaxis]
    assert _y.shape[1] == 1
    return _y

class Gauss_Process_Regressor:
    def __init__(self, dim, t1 = 1, t2 = 1, t3 = 0):
        self.x_train = None
        self.y_train = None
        self.K = None
        self.K_inv = None
        self.dim = dim
        self.gauss_t = [t1, t2, t3]
    
    def set_data(self, x_train, y_train):
        _x = x_regulation(x_train, self.dim)
        _y = y_regulation(y_train)

        assert len(_x) == len(_y)

        self.x_train = _x
        self.y_train = _y
        self.calc_kernel()


    def append_data(self, x_train, y_train):
        _x = x_regulation(x_train, self.dim)
        _y = y_regulation(y_train)

        assert len(_x) == len(_y)

        self.x_train = np.append(self.x_train, _x, axis = 0)
        self.y_train = np.append(self.y_train, _y, axis = 0)
        self.calc_kernel()
    
    def calc_kernel(self):
        self.K = kernel(self.x_train, self.x_train, *self.gauss_t)
        self.K_inv = np.linalg.inv(self.K)

    def estimation(self, x_test):
        _x = x_regulation(x_test, self.dim)
        x_test = _x

        K_s = kernel(self.x_train, x_test, *self.gauss_t)
        K_ss = kernel(x_test, x_test, *self.gauss_t)

        mean = K_s.T@self.K_inv@self.y_train
        sigma = K_ss - K_s.T@self.K_inv@K_s

        return mean.flatten(), sigma


        
        
        





        
        
        




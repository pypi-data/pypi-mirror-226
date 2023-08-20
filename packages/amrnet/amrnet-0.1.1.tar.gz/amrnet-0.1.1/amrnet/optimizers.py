"""
An optimizer is used to adjust the network parameters based on gradients computed from back propagtion
"""
import numpy as np

from amrnet.nn import NeuralNet

class Optimizer:
    
    def step(self, net: NeuralNet) -> None:
        
        raise NotImplementedError
    
    
class SGD(Optimizer):
    
    def __init__(self, lr: float = 0.01) -> None:
        
        self.lr = lr
        
        
    def step(self, net: NeuralNet) -> None:
        
        for param, grad in net.params_and_grads():
            
            param -= self.lr * grad
            
            
class AdaGrad(SGD):
    
    def __init__(self, lr: float = 0.01, epsilon: float = 1e-5) -> None:
        super().__init__(lr)
        
        self.epsilon = epsilon
        
    def step(self, net: NeuralNet) -> None:
        
        i = 0
        
        for param, grad in net.params_and_grads():
            
            param -= self.lr / (np.sqrt(self.epsilon) + np.sqrt(grad * grad)) * grad
            
            
            
            
                
           
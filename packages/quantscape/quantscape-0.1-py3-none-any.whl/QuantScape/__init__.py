import numpy as np
from scipy.stats import norm

class BlackScholes:    
    def __init__(self, K): 
        self.K = K
        
        self.d1 = (np.log(S0/self.K) + (r + ((sigma**2)/2))*T) / (sigma * np.sqrt(T))
        self.d2 = self.d1 - sigma*np.sqrt(T)
        
    def call(self):
        bs_call_price = (S0 * norm.cdf(self.d1, 0, 1)) - (self.K * np.exp(-r*T) * norm.cdf(self.d2, 0, 1))
        
        return bs_call_price
        
    def put(self):
        bs_put_price = self.K * np.exp(r*T) * norm.cdf(-self.d2, 0 , 1) - S0 * norm.cdf(-self.d1, 0, 1)
        
        return bs_put_price
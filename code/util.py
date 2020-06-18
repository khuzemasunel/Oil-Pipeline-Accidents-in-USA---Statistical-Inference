# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 02:35:16 2020

@author: khuze
"""
import numpy as np

class Utility:
    
    def ecdf(data):
        n = len(data)
        x = np.sort(data)
        y = np.arange(1, n+1) / n
        return x, y
    
    def perform_bernoulli_trials(n, p):
        """Perform n Bernoulli trials with success probability p
        and return number of successes."""

        n_success = 0
    
        for i in range(n):
            random_number = np.random.random()
            if random_number < p:
                n_success+=1
                
        return n_success
    
    def bootstrap_replicate_1d(data, func):
        """Generate bootstrap replicate of 1D data."""
        bs_sample = np.random.choice(data, len(data))
        return func(bs_sample)
    
    def draw_bs_reps(self,data, func, size=1):
        """Draw bootstrap replicates."""

        bs_replicates = np.empty(size)
        
        for i in range(size):
            bs_replicates[i] = self.bootstrap_replicate_1d(data,func)
    
        return bs_replicates

    
        
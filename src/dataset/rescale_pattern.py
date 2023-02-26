# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 10:18:16 2023

@author: tom
@description:
    Simple script to resize the pattern to the maximal size it needs to be. 
    This will reduce the computing time when creating the dataset.
"""

import skimage as sk

if __name__ == "__main__":
    
    # Load the pattern
    pattern_name = "tag52_13_00000.png"
    pattern = sk.io.imread(pattern_name, as_gray=True)
    
    # Rescale it to a smaller size
    size = (48, 48)
    pattern_rescaled = sk.transform.resize(pattern, size, anti_aliasing=False)
    
    # Save it
    sk.io.imsave('pattern_{}.png'.format(size), pattern_rescaled)
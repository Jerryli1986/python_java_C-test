#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jerry
"""
#write a program to calculate the factorial of a number

def fatorial(n) :
    if n>1 :
        return n*fatorial(n-1)
    else:
        return 1;

    
if __name__=="__main__":
    n=10
    result=fatorial(n)
    print(result)
    
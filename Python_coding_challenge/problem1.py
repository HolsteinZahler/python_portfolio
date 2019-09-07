#Computes the 500th coefficient of the Taylor series for the 
#generating function of partitions of n into parts of size 1,5,10,20,50, or 100.
#The generating function is 1/((1-x)*(1-x^5)*(1-x^10)*(1-x^20)*(1-x^50)*(1-x^100))
#The algopy library does most of the work here.  This script follows the method given here:
#https://pythonhosted.org/algopy/examples/series_expansion.html

import time
start_time=time.time()
import numpy
from algopy import UTPM

def f(x):
	return 1/((1-x)*(1-x**5)*(1-x**10)*(1-x**20)*(1-x**50)*(1-x**100))

D= 501; P=1
x = UTPM(numpy.zeros((D,P)))
x.data[0,0] = 0
x.data[1,0] = 1

y=f(x)
#Returns the 500 coefficient of the Taylor series of f(x) centered at 0:
print(int(y.data[500,0]))
end_time=time.time()
print("CPU time including library initialization: %f" %(end_time-start_time))
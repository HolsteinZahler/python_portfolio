#This uses a built in solver in scipy.  It finds the minimum
# for -A, which is the opposite maximum of A.
import time
start_time=time.time()
import csv
import numpy as np
from scipy.optimize import linear_sum_assignment

with open('matrix.ssv', 'r') as f:
  matrix = list(csv.reader(f, delimiter=' '))

matrix = np.array(matrix[0:], dtype=np.int)
matrix = -matrix
matrix_sz=len(matrix)

[rows,cols]=linear_sum_assignment(matrix)
#print(rows)
#print(cols)
sum=0
for i in range(0,matrix_sz):
  sum+=matrix[rows[i],cols[i]]
print(-sum)
end_time=time.time()
print("CPU time including library initialization: %f" %(end_time-start_time))
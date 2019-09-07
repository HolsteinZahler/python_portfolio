import time
start_time=time.time()

#Compute binomial coeficients
def nCr(n, r):
  if (r>n):
    return 0;
  else:
    numerator=1
    denominator=1
    for i in range(n-r+1,n+1):
      numerator*=i
    for i in range(1,r+1):
      denominator*=i
    return numerator/denominator

#Computes the number of solutions to x_1+x_2+...+x_k=n with 1<=x_i<=M
#Using principle of inclusion/exclusion
def sum_soln_ct(n,k,M):
  sum_soln=nCr(n-1,k-1)
  sign=1
  for i in range(1,k+1):
    if (n>i*M+1):
      sign*=-1
      sum_soln+=nCr(k,i)*sign*nCr(n-i*M-1,k-1)
  return sum_soln

oberyn_rolls_lt_i=0
gregor_rolls_i=0
gregor_wins_ct=0

for i in range(4, 8):
  oberyn_rolls_lt_i+=sum_soln_ct(i,4,10)

for i in range(9, 41):
  oberyn_rolls_lt_i+=sum_soln_ct(i-1,4,10)
  gregor_rolls_i=sum_soln_ct(i,8,5)
  gregor_wins_ct+=oberyn_rolls_lt_i*gregor_rolls_i
#  Used to test that there are 9999 oberyn rolls less than 40.
#  if (i==40):
#    print("==========")
#    print sum_soln_ct(i,8,5)
#    print oberyn_rolls_lt_i

print(gregor_wins_ct/float(5**8*10**4))
end_time=time.time()
print("CPU time including library initialization: %f" %(end_time-start_time))
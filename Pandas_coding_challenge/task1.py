#[2019-08-22] Herman Schaumburg herman.schaumburg@gmail.com
#
#Revision 2
#
#Use the command below to run this script with the example data file
# ny-demographics.csv:
# python3 task1.py ny-demographics ny-demographics-out
#
#It produces two output files ny-demographics-out_revised.csv ny-demographics-out_unrevised.csv
#
#
#To run, you need python and the library pandas.
#
#Here are instructions on installing pandas.
#
#https://pandas.pydata.org/pandas-docs/stable/install.html
#
#
#I used the following method to install pandas:
#Installing from PyPI
#pandas can be installed via pip from PyPI.
#
#pip install pandas
#
#
#

#importing libraries
import pandas as pd
import numpy as np
import sys
from datetime import datetime

#The following handles arguements and throws an error if the wrong number are given.
num_arg=len(sys.argv)-1
if num_arg!=2:
	print( "Two arguements must be supplied -- input file and output file without csv extension.")
input_file=sys.argv[1]
input_file+=".csv"
print( "Input File....."+input_file)
output_file=sys.argv[2]
print("Output Files...."+output_file+"_unrevised.csv"+" "+output_file+"_revised.csv")

#The following lines are for timing
print ("Starting...")
startTime = datetime.now()

#Create data frame for input
df = pd.read_csv(input_file, dtype={'geoid11': object})

#Create data frame to hold output
columns=['geoid5',
'geoid5name',
'population',
'asian share',
'black share',
'hispanic share',
'white share',
'tracts',
'asian majority tracts',
'black majority tracts',
'hispanic majority tracts',
'white majority tracts',
'nomajority tracts']
df_out=pd.DataFrame(columns=columns)

#Converting geoid11 to 5
def get_digits(item):
	return str(item)[0:5]

df['geoid11'] =df['geoid11'].map(get_digits)
df['geoid11'] = pd.to_numeric(df['geoid11'])
#Finished converting geoid11 to 5

#Extracting unique geoid5 id's for output
df_out['geoid5']=pd.Series(df['geoid11'], name='geoid5').unique()


#Split up geoid11name name
df['geoid11name'].replace(regex=True,inplace=True,to_replace=r'Census Tract ',value=r'')

# new data frame with split value columns
new = df['geoid11name'].str.split(",", n = 1, expand = True)

# making seperate last name column from new data frame
df['County, State']= new[1]

# Dropping old Name columns
df.drop(columns =['geoid11name'], inplace = True)

#Extract unique values in geoid5name
df_out['geoid5name']=pd.Series(df['County, State'], name='geoid5').unique()
num_rows_of_output=df_out.shape[0]

#Get only revised populations in input data frame
df['Rpopulation'] = df['population'].str.extract(r"\(r(.*?)\)", expand=False)
#Get only unrevised populations that are revised later
df['Population'] = df['population'].str.extract(r"(.*?)\(r", expand=False)
#Fill in these collumns with ones that were not revised
df.Rpopulation.fillna(df.population, inplace=True)
df['Rpopulation'] = pd.to_numeric(df['Rpopulation'])
df.Population.fillna(df.population, inplace=True)
df['Population']=pd.to_numeric(df['Population'])
#Replace population in input data frame by deleting and renaming collumns
df=df.drop('population', axis=1)
df.rename(columns = {'Population':'population'}, inplace = True)

#Initializing lists for counting the majority tracts
num_rows_of_input=df.shape[0]
asian_majority_tracts=[]
black_majority_tracts=[]
hispanic_majority_tracts=[]
white_majority_tracts=[]
nomajority_tracts=[]
tracts=[]

#This for loop is used to find the nonempty tracts and identify those tracts with a majority  or
#nonmajority ethnicity.
#Rev 2 improved syntax
for j in range(0, num_rows_of_input):
	if df['population'][j]>0:
		half_population=float(0.5*df['population'][j])
		val_w=float(df['white'][j])
		val_h=float(df['hispanic'][j])
		val_b=float(df['black'][j])
		val_a=float(df['asian'][j])
		w=float(0)
		h=float(0)
		b=float(0)
		a=float(0)
		n=float(0)
		if (val_w>half_population):
			w=1
		elif (val_h>half_population):
			h=1
		elif (val_b>half_population):
			b=1
		elif (val_a>half_population):
			a=1
		if w+h+b+a==0:
			n=1
		white_majority_tracts.append(w)
		hispanic_majority_tracts.append(h)
		black_majority_tracts.append(b)
		asian_majority_tracts.append(a)
		nomajority_tracts.append(n)
		tracts.append(1)
	else:
		white_majority_tracts.append(0)
		hispanic_majority_tracts.append(0)
		black_majority_tracts.append(0)
		asian_majority_tracts.append(0)
		nomajority_tracts.append(0)
		tracts.append(1)

#Storing lists into data frame
df['asian_major_tract']=asian_majority_tracts
df['white_major_tract']=white_majority_tracts
df['hispanic_major_tract']=hispanic_majority_tracts
df['black_major_tract']=black_majority_tracts
df['nonmajority_tract']=nomajority_tracts
df['tract']=tracts

#Initializing variable to store the numbers of county populations
num_rows_of_output=df_out.shape[0]
population_sum=[]
asian_share=[]
black_share=[]
hispanic_share=[]
white_share=[]
asian_majority_tracts=[]
black_majority_tracts=[]
hispanic_majority_tracts=[]
white_majority_tracts=[]
nomajority_tracts=[]
num_tracts=[]

#Most work is done in this loop, it computes the population sums, those for each demographic,
#how many tracts are in each county, and different share fractions.
for j in range(0, num_rows_of_output):
	#population_sum.append(df.loc[df['geoid11'] == df_out['geoid5'][j], 'population'].sum())
	#Rev2 fixed syntax to store the indexes used in the above command to find them only once rather
	#than repeatedly.

	indices=df.loc[df['geoid11'] == df_out['geoid5'][j], 'population'].index.values

	population_sum.append(df.loc[indices, 'population'].sum())
	asian_sum= df.loc[indices,'asian'].sum()
	black_sum=df.loc[indices,'black'].sum()
	hispanic_sum=df.loc[indices,'hispanic'].sum()
	white_sum=df.loc[indices,'white'].sum()

	asian_majority_tracts_sum=df.loc[indices, 'asian_major_tract'].sum()
	black_majority_tracts_sum=df.loc[indices, 'black_major_tract'].sum()
	hispanic_majority_tracts_sum=df.loc[indices, 'hispanic_major_tract'].sum()
	white_majority_tracts_sum=df.loc[indices, 'white_major_tract'].sum()
	nomajority_tracts_sum=df.loc[indices, 'nonmajority_tract'].sum()
	tracts_sum=df.loc[indices,  'tract'].sum()

	num_tracts.append(tracts_sum)
	if population_sum[j]>0:
		asian_share.append(asian_sum/float(population_sum[j]))
		black_share.append(black_sum/float(population_sum[j]))
		hispanic_share.append(hispanic_sum/float(population_sum[j]))
		white_share.append(white_sum/float(population_sum[j]))
		asian_majority_tracts.append(asian_majority_tracts_sum)
		black_majority_tracts.append(black_majority_tracts_sum)
		hispanic_majority_tracts.append(hispanic_majority_tracts_sum)
		white_majority_tracts.append(white_majority_tracts_sum)
		nomajority_tracts.append(nomajority_tracts_sum)
	else:
		asian_share.append('NA')
		black_share.append('NA')
		hispanic_share.append('NA')
		white_share.append('NA')
		asian_majority_tracts.append('NA')
		black_majority_tracts.append('NA')
		hispanic_majority_tracts.append('NA')
		white_majority_tracts.append('NA')
		nomajority_tracts.append('NA')
		num_tracts.append(tracts_sum)

df_out['population']=population_sum
df_out['asian share']=asian_share
df_out['black share']=black_share
df_out['hispanic share']=hispanic_share
df_out['white share']=white_share
df_out['tracts']=num_tracts
df_out['asian majority tracts']=asian_majority_tracts
df_out['black majority tracts']=black_majority_tracts
df_out['hispanic majority tracts']=hispanic_majority_tracts
df_out['white majority tracts']=white_majority_tracts
df_out['nomajority tracts']=nomajority_tracts

#Export dataframe to csv
df_out.to_csv('output_unrevised.csv', index=False)

#Find total county populations based on revised population numbers.
population_sum=[]
for j in range(0, num_rows_of_output):
	population_sum.append(df.loc[df['geoid11'] == df_out['geoid5'][j], 'Rpopulation'].sum())

df_out['population']=population_sum

#Export dataframe to csv
df_out.to_csv('output_revised.csv', index=False)
total_time=datetime.now() - startTime
print( "CPU time used ", total_time)
print( "...Done")

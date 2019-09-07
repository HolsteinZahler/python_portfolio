import pandas as pd
from sklearn.model_selection import train_test_split

import numpy as np

#Read data file
#https://www.kaggle.com/mlg-ulb/creditcardfraud/version/3
data = pd.read_csv('creditcard.csv')

#Seperate data from target
#	Last column of data is currently the target (class = 1 for fraudulant transaction 0 for normal transaction)
col_labels=[]
for col_label in data.columns:
	col_labels.append(col_label)
#print(col_labels)
target_col_label=col_labels[len(col_labels)-1]
col_labels=col_labels[0:len(col_labels)-1]
target=data[target_col_label]
data=data[col_labels]
#print(data.head(n=40))
#print(target.head(n=40))

data_train, data_test, target_train, target_test = train_test_split(data,target, test_size = 0.30
, random_state = 10)


#Naive-Bayes Estimator
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import auc
from sklearn.metrics import accuracy_score
gnb = GaussianNB()
pred = gnb.fit(data_train, target_train).predict(data_test)

num_false_pos=0
num_false_neg=0
num_fraud_cases=0
caught_frauds=0
num_of_pred=len(pred)
for i in range(0,num_of_pred):
#	print(target_test[i])
	if pred[i]==0 and target_test.iloc[i]==1:
		num_false_neg+=1
	elif pred[i]==1 and target_test.iloc[i]==0:
		num_false_pos+=1
	if target_test.iloc[i]==1:
		num_fraud_cases+=1
		if pred[i]==1:
			caught_frauds+=1
print("*** Naive-Bayes Estimater Results ***")
print("Length of target data  "+str(target_test.shape[0]))
print("Number of predictions made:  "+str(num_of_pred))
print("Number of frauds committed:  "+str(num_fraud_cases))
print("Number of frauds caught:  "+str(caught_frauds))
print("Number of false positives:  "+str(num_false_pos))
print("Number of false negatives:  "+str(num_false_neg))
print("Naive-Bayes accuracy : ",accuracy_score(target_test, pred, normalize = True))
#print("Naive-Bayes AUC : ",auc(target_test, pred))

#LinearSVC
from sklearn.svm import LinearSVC
#create an object of type LinearSVC
#Got convergence warning without having dual=False.  max_iter default is 1000
svc_model = LinearSVC(random_state=0, dual=False)
#train the algorithm on training data and predict using the testing data
pred = svc_model.fit(data_train, target_train).predict(data_test)

num_false_pos=0
num_false_neg=0
num_fraud_cases=0
caught_frauds=0
num_of_pred=len(pred)
for i in range(0,num_of_pred):
#	print(target_test[i])
	if pred[i]==0 and target_test.iloc[i]==1:
		num_false_neg+=1
	elif pred[i]==1 and target_test.iloc[i]==0:
		num_false_pos+=1
	if target_test.iloc[i]==1:
		num_fraud_cases+=1
		if pred[i]==1:
			caught_frauds+=1
print("*** LinearSVC Results ***")
print("Length of target data  "+str(target_test.shape[0]))
print("Number of predictions made:  "+str(num_of_pred))
print("Number of frauds committed:  "+str(num_fraud_cases))
print("Number of frauds caught:  "+str(caught_frauds))
print("Number of false positives:  "+str(num_false_pos))
print("Number of false negatives:  "+str(num_false_neg))
print("LinearSVC accuracy : ",accuracy_score(target_test, pred, normalize = True))


#K-Neighbors Classifier
from sklearn.neighbors import KNeighborsClassifier
#create object of the lassifier
neigh = KNeighborsClassifier(n_neighbors=3, p=1)
#Train the algorithm
neigh.fit(data_train, target_train)
# predict the response
pred = neigh.predict(data_test)
num_false_pos=0
num_false_neg=0
num_fraud_cases=0
caught_frauds=0
num_of_pred=len(pred)
for i in range(0,num_of_pred):
#	print(target_test[i])
	if pred[i]==0 and target_test.iloc[i]==1:
		num_false_neg+=1
	elif pred[i]==1 and target_test.iloc[i]==0:
		num_false_pos+=1
	if target_test.iloc[i]==1:
		num_fraud_cases+=1
		if pred[i]==1:
			caught_frauds+=1
print("*** K-Neighbors Classifier Results ***")
print("Length of target data  "+str(target_test.shape[0]))
print("Number of predictions made:  "+str(num_of_pred))
print("Number of frauds committed:  "+str(num_fraud_cases))
print("Number of frauds caught:  "+str(caught_frauds))
print("Number of false positives:  "+str(num_false_pos))
print("Number of false negatives:  "+str(num_false_neg))
print("K-Neighbors Classifier accuracy : ",accuracy_score(target_test, pred, normalize = True))

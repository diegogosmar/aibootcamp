#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.metrics import classification_report
from sklearn import metrics
import pandas as pd
import statsmodels.api as sm

E="Excellent"
M="Medium"
T="Terrible"

# True values
x_true = [E,E,E,E,E,E,E,E,E,E, M,M,M,M,M,M,M,M,M,M, T,T,T,T,T,T,T,T,T,T]
# Predicted values
y_pred = [E,E,E,E,T,M,E,E,E,E, M,M,M,E,M,E,M,T,M,M, T,E,T,T,T,T,T,T,T,T]

# Print the Confusion Matrix
print(metrics.confusion_matrix(x_true, y_pred))

# Print the precision, recall, f1-score and accuracy
print(classification_report(x_true, y_pred, digits=3))


# In[2]:


from sklearn.metrics import r2_score
y_true = [3, -2.5, 2, 8]
y_pred = [3, -2.5, 2, 8]

r2 = r2_score(y_true, y_pred)

print("Coefficient of determination: %.3f"%r2)


# In[3]:


import numpy as np
y_mean = np.mean(y_true)
print("Oservation Mean value: %.3f"%y_mean)


# In[4]:


y_true = [3, -2.5, 2, 8]
y_pred = [2.625, 2.625, 2.625, 2.625]

r2 = r2_score(y_true, y_pred)

print("Coefficient of determination: %.3f"%r2)


# In[5]:


import numpy as np
from scipy.stats import f, norm
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# first f
rv1 = f(dfn=3, dfd=15, loc=0, scale=1)
x = np.linspace(rv1.ppf(0.0001), rv1.ppf(0.9999), 100)
y = rv1.pdf(x) 

plt.xlim(0,5)
plt.plot(x,y, 'b-')

# second f 
rv2 = f(dfn=10, dfd=50, loc=0, scale=1)
x = np.linspace(rv2.ppf(0.0001), rv2.ppf(0.9999), 100)
y = rv2.pdf(x) 

plt.plot(x,y, 'r--')


# In[6]:


df = pd.read_csv('http://gosmar.eu/ml/cats.csv', index_col=0) 
print(df.head(6))
print(len(df))


# In[7]:


#To_be_predicted
y = df.Hwt
#Intependent var
X = df.Bwt
#Add constant to better fit the linear model
X = sm.add_constant(X)


# In[8]:


model=sm.OLS(y, X)


# In[9]:


model = model.fit()


# In[10]:


# Create the X array from the min to the max observations
X_obs = np.linspace(X.Bwt.min(), X.Bwt.max(), len(df))[:, np.newaxis]
X_obs = sm.add_constant(X_obs)
# Let's calculate the predicted values
y_pred = model.predict(X_obs)

fig = plt.figure()
fig.subplots_adjust(top=3.8, right = 1.9)
ax1 = fig.add_subplot(211)

plt.scatter(X.Bwt, y, alpha=0.3) # Plot the raw data
plt.title("Linear Regression", fontsize=20)
plt.xlabel("Body weight in kg.", fontsize=20)
plt.ylabel("Heart weight in g.", fontsize=20)
plt.plot(X_obs[:, 1], y_pred, 'r', alpha=0.9) # Add the regression line, colored in red


# In[11]:


model.summary()


# In[12]:


model.params


# In[13]:


print(model.pvalues)


# In[14]:


df = pd.read_csv('http://gosmar.eu/ml/putter.csv', index_col=0) 
print(df.head(6))
print(len(df))


# In[15]:


#To_be_predicted
y = df.Made
#Intependent var
X = df.Length


# In[16]:


# Create the X array from the min to the max observations
X_obs = np.linspace(np.amin(X), np.amax(X), len(df))[:, np.newaxis]

fig = plt.figure()
fig.subplots_adjust(top=3.8, right = 1.9)
ax1 = fig.add_subplot(211)

plt.scatter(X_obs, y, alpha=0.3) # Plot the raw data
plt.title("Logistic Regression - Golf Putt", fontsize=20)
plt.xlabel("Distance (meters)", fontsize=20)
plt.ylabel("Hole Probability", fontsize=20)

#plt.plot(X_obs[:, 1], y_pred, 'r', alpha=0.9) # Add the regression line, colored in red


# In[17]:


# Create the X array from the min to the max observations
X_obs = np.linspace(np.amin(X), np.amax(X), len(df))[:, np.newaxis]

fig = plt.figure()
fig.subplots_adjust(top=3.8, right = 1.9)
ax1 = fig.add_subplot(211)

plt.scatter(X_obs, y, alpha=0.3) # Plot the raw data
plt.title("Logistic Regression - Golf Putt", fontsize=20)
plt.xlabel("Distance (meters)", fontsize=20)
plt.ylabel("Hole Probability", fontsize=20)

z = 1 / (1 + np.exp((1.5*X_obs)-9))
plt.plot(X_obs, z, 'r', alpha=0.9) # Add the reverse Sigmoid function

z = 1 / (1 + np.exp((1.5*X_obs)-8.5))
plt.plot(X_obs, z, 'r--', alpha=0.9) # Add the reverse Sigmoid function

z = 1 / (1 + np.exp((1.5*X_obs)-9.5))
plt.plot(X_obs, z, 'r--', alpha=0.9) # Add the reverse Sigmoid function

z = 1 / (1 + np.exp((1.5*X_obs)-10))
plt.plot(X_obs, z, 'r--', alpha=0.9) # Add the reverse Sigmoid function

z = 1 / (1 + np.exp((1.5*X_obs)-8))
plt.plot(X_obs, z, 'r--', alpha=0.9) # Add the reverse Sigmoid function


# In[18]:


#To_be_predicted
y = df.Made
#Intependent var
X = df.Length

print(X.shape[0])
print(y.shape[0])


# In[19]:


from sklearn.naive_bayes import GaussianNB


# In[20]:


df = pd.read_csv('http://gosmar.eu/ml/email_features.csv') 
print(df.head(3))
print(len(df))


# In[21]:


#Separate independent and target features
X=df.drop(['Status'], axis=1)
y=df['Status']

#Define the model
model = GaussianNB()

#Fitting
model.fit(X, y)


# In[22]:


#Predict for NUM=800 chars, Size=15 MBytes, Special=8 chars

print("0: no-SPAM 1: SPAM")
print(model.predict([[800, 15, 8]]))


# In[23]:


#Predict for NUM=150 chars, Size=8 MBytes, Special=3 chars

print("0: no-SPAM 1: SPAM")
print(model.predict([[250, 8, 3]]))


# In[24]:


#Print the probabilities for each message: 
#col[0]=P(no-SPAM() 
#col[1]=P(SPAM)

print(model.predict_proba(X))


# In[25]:


df = pd.read_csv('http://gosmar.eu/ml/nuclear.csv', index_col=0) 
print(df.head(6))
print(len(df))


# In[26]:


import matplotlib.pyplot as plt

#To_be_predicted
y = df.cost

# Create the X array from the min to the max observations
X_obs = np.linspace(1, 32, len(df))[:, np.newaxis]

fig = plt.figure()
fig.subplots_adjust(top=1.8, right = 2, hspace = 0.2)

ax1 = fig.add_subplot(241)
counts, bins = np.histogram(y)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("Cost", fontsize=20)

ax2 = fig.add_subplot(242)
counts, bins = np.histogram(df.date)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("Date", fontsize=20)

ax3 = fig.add_subplot(243)
counts, bins = np.histogram(df.t1)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("t1-t2", fontsize=20)

ax4 = fig.add_subplot(243)
counts, bins = np.histogram(df.t2)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("t2-t2", fontsize=20)

ax4 = fig.add_subplot(244)
counts, bins = np.histogram(df.cap)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("cap", fontsize=20)

ax5 = fig.add_subplot(245)
counts, bins = np.histogram(df.pr)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("pr", fontsize=20)

ax6 = fig.add_subplot(246)
counts, bins = np.histogram(df.ct)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("ct", fontsize=20)

ax6 = fig.add_subplot(247)
counts, bins = np.histogram(df.bw)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("bw", fontsize=20)

ax6 = fig.add_subplot(248)
counts, bins = np.histogram(df.pt)
plt.hist(bins[:-1], bins, weights=counts)
plt.title("pt", fontsize=20)

plt.xlabel("", fontsize=20)
plt.ylabel("", fontsize=20)


# In[27]:


df = pd.read_csv('http://gosmar.eu/ml/nuclear2.csv', index_col=0) 
import seaborn as sns; sns.set()
X=df.drop(['pr','ne','ct','t1','t2','bw','pt','cum.n','date'], axis=1)
ax = sns.heatmap(X)


# In[28]:


df = pd.read_csv('http://gosmar.eu/ml/nuclear2.csv', index_col=0) 
print(df.info())
import seaborn as sns; sns.set()
sns.heatmap(df.isnull(), cbar=False)


# In[29]:


df = pd.read_csv('http://gosmar.eu/ml/nuclear.csv', index_col=0) 
import seaborn as sns; sns.set()
fig, ax = plt.subplots(figsize=(10,10))
fig.subplots_adjust(top=0.8, right = 1, hspace = 0.5)
ax = sns.heatmap(df.corr(), cmap="YlGnBu", annot = True)


# In[ ]:





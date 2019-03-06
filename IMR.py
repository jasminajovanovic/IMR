#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import numpy as np


# In[2]:


dfImr = pd.read_csv("./IMR, 2007-2016.txt", sep='\t', )
dfImr.dropna(subset=['State'], inplace = True)
dfImr = dfImr.set_index('State')
dfImr.head()


# In[3]:


dfImrByStateByRace = pd.read_csv("./IMR BY state by RACE, 2007-2016.txt", sep='\t')
dfImrByStateByRace.dropna(subset=['State'], inplace = True)
dfImrByStateByRace = dfImrByStateByRace.set_index("State")
dfImrByStateByRace.head()


# In[4]:


pdMerged = pd.merge(dfImr, dfImrByStateByRace, on='State', left_index=True)


# In[7]:


dfImrByRace = pd.read_csv("./IMR by race, 2007-2016.txt", sep='\t')
dfImrByRace.dropna(subset=['Race'], inplace=True)
dfImrByRace['expected'] = dfImrByRace['Death Rate'].mean()


# In[8]:


dfImrByRace.head()


# In[9]:


dfImrByCountyByRace = pd.read_csv("./IMR by county by race, 2007-2016.txt", sep='\t')
dfImrByCountyByRace.dropna(subset=['Race'], inplace=True)
dfImrByCountyByRace.shape


# In[10]:


# remove rows with unreliable death rate data (fewer than 20 deaths)
dfImrByCountyByRace = dfImrByCountyByRace.loc[dfImrByCountyByRace['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]
# convert death rate to float
dfImrByCountyByRace['Death Rate'] = dfImrByCountyByRace['Death Rate'].map(lambda x: float(x))
dfImrByCountyByRace.head()


# In[11]:


blacks = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2054-5']['Death Rate']
natives = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '1002-5']['Death Rate']
whites = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2106-3']['Death Rate']
asians = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == 'A-PI']['Death Rate']


# In[12]:


dfImrByCountyByRace.boxplot('Death Rate', by="Race", figsize=(20, 10))


# In[13]:


# ANOVA shows that one (or more) race(s) is significantly different than the rest
stats.f_oneway(blacks, natives, whites, asians)


# In[14]:


from statsmodels.stats import multicomp


# In[15]:


# use pairwise tukeyhsd to find out which race is significnalty different than the rest  
answer = multicomp.pairwise_tukeyhsd(dfImrByCountyByRace['Death Rate'], dfImrByCountyByRace['Race'], alpha=0.05)


# In[16]:


# reject True proves the hypothesis - that there is significant difference between two means
print(answer)


# In[18]:


dfImrByYearByRace = pd.read_csv("./imr by year by race, 2007-2016.txt", sep='\t')


# In[19]:


dfImrByYearByRace.dropna(subset=['Year of Death'], inplace=True)
dfImrByYearByRace['Race'] = ['Unknown' if myrace is np.nan else myrace for myrace in dfImrByYearByRace['Race']]


# In[20]:


dfImrByYearByRace.head()


# In[21]:


dfPlot = dfImrByYearByRace.pivot('Year of Death', 'Race', 'Death Rate')
dfPlot.reset_index(inplace=True)


# In[22]:


dfPlot.head()


# In[23]:


plt.plot(dfPlot['Year of Death'], dfPlot['Unknown'], label='Unknown')
plt.plot(dfPlot['Year of Death'], dfPlot['American Indian or Alaska Native'], label='American Indian or Alaska Native')
plt.plot(dfPlot['Year of Death'], dfPlot['Asian or Pacific Islander'], label='Asian or Pacific Islander')
plt.plot(dfPlot['Year of Death'], dfPlot['Black or African American'], label='Black or African American')
plt.plot(dfPlot['Year of Death'], dfPlot['White'], label='White')
plt.ylim(0, 20)
plt.legend()
plt.title ("IMR by Race, 2001-2016")


# In[ ]:


# leading cause of death
# leading cause of death by age
# leading cause of death by race
# death by age by race


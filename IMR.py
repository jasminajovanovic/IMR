#!/usr/bin/env python
# coding: utf-8

# In[178]:


import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import numpy as np


# In[15]:


dfImr = pd.read_csv("./IMR, 2007-2016.txt", sep='\t', )
dfImr.dropna(subset=['State'], inplace = True)
dfImr = dfImr.set_index('State')
dfImr.head()


# In[27]:


dfImrByStateByRace = pd.read_csv("./IMR BY state by RACE, 2007-2016.txt", sep='\t')
dfImrByStateByRace.dropna(subset=['State'], inplace = True)
dfImrByStateByRace = dfImrByStateByRace.set_index("State")
dfImrByStateByRace.head()


# In[28]:


pdMerged = pd.merge(dfImr, dfImrByStateByRace, on='State', left_index=True)


# In[29]:


(14.28+6.58)/2


# In[30]:


pdMerged.sort_values(by='State')


# In[50]:


dfImrByRace = pd.read_csv("./IMR by race, 2007-2016.txt", sep='\t')
dfImrByRace.dropna(subset=['Race'], inplace=True)
dfImrByRace['expected'] = dfImrByRace['Death Rate'].mean()


# In[60]:


dfImrByRace.head()


# In[47]:


critical_value = stats.chi2.ppf(q = 0.95, df = 3)
critical_value


# In[49]:


dfImrByRace['Death Rate'].mean()


# In[53]:


stats.chisquare(dfImrByRace['Death Rate'], dfImrByRace['expected'])


# In[ ]:





# In[87]:


dfImrByCountyByRace = pd.read_csv("./IMR by county by race, 2007-2016.txt", sep='\t')
dfImrByCountyByRace.dropna(subset=['Race'], inplace=True)
dfImrByCountyByRace.shape


# In[102]:


dfImrByCountyByRace = dfImrByCountyByRace.loc[dfImrByCountyByRace['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]
dfImrByCountyByRace['Death Rate'] = dfImrByCountyByRace['Death Rate'].map(lambda x: float(x))
dfImrByCountyByRace.head()


# In[103]:


blacks = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2054-5']['Death Rate']
natives = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '1002-5']['Death Rate']
whites = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2106-3']['Death Rate']
asians = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == 'A-PI']['Death Rate']


# In[104]:





# In[107]:


dfImrByCountyByRace.boxplot('Death Rate', by="Race", figsize=(20, 10))


# In[108]:


stats.f_oneway(blacks, natives, whites, asians)


# In[131]:


from statsmodels.stats import multicomp
len(blacks)


# In[130]:


len(natives)


# In[133]:


answer = multicomp.pairwise_tukeyhsd(dfImrByCountyByRace['Death Rate'], dfImrByCountyByRace['Race'], alpha=0.05)


# In[135]:


print(answer)


# In[140]:


from matplotlib import pyplot as plt


# In[143]:


dfImrByYearByRace = pd.read_csv("./imr by year by race, 2007-2016.txt", sep='\t')


# In[191]:


dfImrByYearByRace.dropna(subset=['Year of Death'], inplace=True)
dfImrByYearByRace['Race'] = ['Unknown' if myrace is np.nan else myrace for myrace in dfImrByYearByRace['Race']]


# In[192]:


dfImrByYearByRace.head()


# In[193]:


dfPlot = dfImrByYearByRace.pivot('Year of Death', 'Race', 'Death Rate')
dfPlot.reset_index(inplace=True)
dfPlot.rename(columns={'nan':'Undeclared'}, inplace=True)


# In[194]:


dfPlot.head()


# In[197]:


plt.plot(dfPlot['Year of Death'], dfPlot['Unknown'], label='Unknown')
plt.plot(dfPlot['Year of Death'], dfPlot['American Indian or Alaska Native'], label='American Indian or Alaska Native')
plt.plot(dfPlot['Year of Death'], dfPlot['Asian or Pacific Islander'], label='Asian or Pacific Islander')
plt.plot(dfPlot['Year of Death'], dfPlot['Black or African American'], label='Black or African American')
plt.plot(dfPlot['Year of Death'], dfPlot['White'], label='White')
plt.ylim(0, 20)
plt.legend()


# In[ ]:





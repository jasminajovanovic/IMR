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


# In[67]:


dfImrByCountyByRace = pd.read_csv("./IMR by county by race, 2007-2016.txt", sep='\t')
dfImrByCountyByRace.dropna(subset=['Race'], inplace=True)
dfImrByCountyByRace.shape


# In[70]:


# remove rows with unreliable death rate data (fewer than 20 deaths)
dfImrByCountyByRace = dfImrByCountyByRace.loc[dfImrByCountyByRace['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]
# dfImrByCountyByRace.loc[dfImrByCountyByRace['Race'] is np.nan]
# todo: include uknown race
# dfImrByCountyByRace['Race'] = ["Unknown" if race is np.nan else race for race in dfImrByCountyByRace['Race']]

# convert death rate to float
dfImrByCountyByRace['Death Rate'] = dfImrByCountyByRace['Death Rate'].map(lambda x: float(x))


# In[71]:


blacks = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2054-5']['Death Rate']
natives = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '1002-5']['Death Rate']
whites = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2106-3']['Death Rate']
asians = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == 'A-PI']['Death Rate']
unknown = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race'] == 'Unknown']['Death Rate']


# In[72]:


dfImrByCountyByRace.boxplot('Death Rate', by="Race", figsize=(20, 10))


# In[13]:


# ANOVA shows that one (or more) race(s) is significantly different than the rest
stats.f_oneway(blacks, natives, whites, asians)


# In[309]:


dfImrByCountyByRace.loc[(dfImrByCountyByRace['Race'] == "Black or African American") & (dfImrByCountyByRace['County'] == 'Allen County, IN')]


# In[310]:


dfImrByCountyByRace.loc[(dfImrByCountyByRace['Race'] == "Black or African American") & (dfImrByCountyByRace['County'] == 'Santa Clara County, CA')]


# In[331]:


blacksByCounty = dfImrByCountyByRace.set_index(['Race', 'County']).sort_values(['Race', 'Death Rate'], ascending=False).loc['Black or African American']
# groupedByRace.sort_values(['Race', 'Death Rate'], ascending=False).loc['Black or African American']
blacksByCounty = blacksByCounty.loc[blacksByCounty['Death Rate'].notnull()]
# for county in blacksByCounty.index:
#     blacksByCounty
# blacksByCounty


# In[340]:


blacksHighestImrCounties = blacksByCounty.head(10)
blacksHighestImrCounties.to_csv("./AfricanAmericanHighestImrCounties.csv")


# In[339]:


blacksLowestImrCounties = blacksByCounty.tail(10)
blacksLowestImrCounties.to_csv("./AfricanAmericanLowestImrCounties.csv")


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



# leading cause of death by age
# leading cause of death by race
# death by age by race
# WHO rates by country


# In[183]:


# Death Rate by age
dfImrByAgeByCause = pd.read_csv("./IMR by age by cause, 2007-2016.txt", sep='\t')
dfImrByAgeByCause.sort_values(by='Death Rate', ascending=False).head(30)


# In[ ]:


dfImrByAgeByCause['Age of Infant at Death'] = ["Unknown" if age is np.nan else age for age in dfImrByAgeByCause['Age of Infant at Death']]
# dfImrByAgeByCause.dropna(subset=['Age of Infant at Death'], inplace=True)
dfImrByAgeByCause = dfImrByAgeByCause.loc[dfImrByAgeByCause['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]
#convert death rate to float
dfImrByAgeByCause['Death Rate'] = dfImrByAgeByCause['Death Rate'].map(lambda x: float(x))
# dfImrByAgeByCause.sort_values(by=['Death Rate'], ascending = False).head(20)


# In[248]:


dfTotalsbyAgebyCause = dfImrByAgeByCause.loc[(dfImrByAgeByCause['Notes']=='Total') & (dfImrByAgeByCause['Age of Infant at Death'].notnull()) ]


# In[258]:


# dfTotalsbyAgebyCause['Death Rate']
dfTotalsbyAgebyCause['Death Rate'] = [float(rate) for rate in dfTotalsbyAgebyCause['Death Rate']]


# In[259]:


plt.barh(dfTotalsbyAgebyCause['Age of Infant at Death'], width=dfTotalsbyAgebyCause['Death Rate'])
# plt.barh(temp['Age of Infant at Death'], width=temp['Death Rate'])
# plt.yticks(dfTotalsbyAgebyCause['Age of Infant at Death'], dfTotalsbyAgebyCause['Age of Infant at Death'], rotation="vertical")
# plt.tight_layout
# plt.xlim(0, 5)
plt.title("IMR vs Age")
plt.ylabel("Age of Infant at Death")
plt.xlabel("Death Rate")
plt.show()


# In[255]:


# removes rows that show total
dfImrByAgeByCause = dfImrByAgeByCause.loc[(dfImrByAgeByCause['Notes'] != 'Total')].sort_values(by=['Death Rate'], ascending=False).head(20)


# In[256]:


infantsUnder1Hour = dfImrByAgeByCause.loc[dfImrByAgeByCause['Age of Infant at Death'] == 'Under 1 hour'].sort_values(by='Death Rate', ascending=False).head(3)
infantsUnder1Day = dfImrByAgeByCause.loc[dfImrByAgeByCause['Age of Infant at Death'] == '1 - 23 hours'].sort_values(by='Death Rate', ascending=False).head(3)
infants1To6Days = dfImrByAgeByCause.loc[dfImrByAgeByCause['Age of Infant at Death'] == '1 - 6 days'].sort_values(by='Death Rate', ascending=False).head(3)
infants7To27Days = dfImrByAgeByCause.loc[dfImrByAgeByCause['Age of Infant at Death'] == '7 - 27 days'].sort_values(by='Death Rate', ascending=False).head(3)
infants1monthTo1Year = dfImrByAgeByCause.loc[dfImrByAgeByCause['Age of Infant at Death'] == '28 - 364 days'].sort_values(by='Death Rate', ascending=False).head(3)


# In[257]:


groupedByAgeTop3 = dfImrByAgeByCause.sort_values(by=['Age of Infant at Death', 'Death Rate'], ascending=False).groupby('Age of Infant at Death').head(3)
groupedByAgeTop3.head()


# In[ ]:





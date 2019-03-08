#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import numpy as np
from statsmodels.stats import multicomp


# ## Infant Mortaility by Race

# In[2]:


dfImrByCountyByRace = pd.read_csv("./IMR by county by race, 2007-2016.txt", sep='\t')
# dfImrByCountyByRace['Race'] = ["Unknown" if race is np.nan else race for race in dfImrByCountyByRace['Race']]

dfImrByCountyByRace.dropna(subset=['Death Rate'], inplace=True)


# In[3]:


# remove rows with unreliable death rate data (fewer than 20 deaths)
dfImrByCountyByRace = dfImrByCountyByRace.loc[dfImrByCountyByRace['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]
# dfImrByCountyByRace.loc[dfImrByCountyByRace['Race'] is np.nan]

# convert death rate to float
dfImrByCountyByRace['Death Rate'] = dfImrByCountyByRace['Death Rate'].map(lambda x: float(x))


# In[4]:


blacks = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2054-5']['Death Rate']
natives = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '1002-5']['Death Rate']
whites = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == '2106-3']['Death Rate']
asians = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race Code'] == 'A-PI']['Death Rate']
unknown = dfImrByCountyByRace.loc[dfImrByCountyByRace['Race'] == 'Unknown']['Death Rate']


# In[5]:


ax = dfImrByCountyByRace.boxplot('Death Rate', by="Race", figsize=(20, 10))
fig = ax.get_figure()
fig.savefig('Death Rate by Race.png')


# ### ANOVA shows that one (or more) race(s) is significantly different than the rest

# In[6]:


stats.f_oneway(blacks, natives, whites, asians)


# In[7]:


blacksByCounty = dfImrByCountyByRace.set_index(['Race', 'County']).sort_values(['Race', 'Death Rate'], ascending=False).loc['Black or African American']
blacksByCounty = blacksByCounty.loc[blacksByCounty['Death Rate'].notnull()]


# In[8]:


blacksHighestImrCounties = blacksByCounty.head(10)
blacksHighestImrCounties.to_csv("./AfricanAmericanHighestImrCounties.csv")


# In[9]:


blacksLowestImrCounties = blacksByCounty.tail(10)
blacksLowestImrCounties.to_csv("./AfricanAmericanLowestImrCounties.csv")


# In[10]:


# use pairwise tukeyhsd to find out which race is significnalty different than the rest  
answer = multicomp.pairwise_tukeyhsd(dfImrByCountyByRace['Death Rate'], dfImrByCountyByRace['Race'], alpha=0.05)


# In[11]:


# reject True proves the hypothesis - that there is significant difference between two means
print(answer)


# ## Infant Mortality by Race, 2007-2016

# In[12]:


dfImrByYearByRace = pd.read_csv("./imr by year by race, 2007-2016.txt", sep='\t')


# In[13]:


dfImrByYearByRace.dropna(subset=['Year of Death'], inplace=True)
dfImrByYearByRace['Race'] = ['Unknown' if myrace is np.nan else myrace for myrace in dfImrByYearByRace['Race']]


# In[14]:


dfImrByYearByRace.head()


# In[15]:


dfPlot = dfImrByYearByRace.pivot('Year of Death', 'Race', 'Death Rate')
dfPlot.reset_index(inplace=True)


# In[16]:


dfPlot.head()


# In[17]:


plt.plot(dfPlot['Year of Death'], dfPlot['Unknown'], label='Unknown')
plt.plot(dfPlot['Year of Death'], dfPlot['American Indian or Alaska Native'], label='American Indian or Alaska Native')
plt.plot(dfPlot['Year of Death'], dfPlot['Asian or Pacific Islander'], label='Asian or Pacific Islander')
plt.plot(dfPlot['Year of Death'], dfPlot['Black or African American'], label='Black or African American')
plt.plot(dfPlot['Year of Death'], dfPlot['White'], label='White')
plt.ylim(0, 20)
plt.legend()
plt.title ("IMR by Race, 2001-2016")
plt.savefig("IMR by Race, 2001-2016.png")
plt.show()


# In[18]:


# TODO
# WHO rates by country


# ## Leading cause of infant mortality by age
# 

# In[19]:


# Death Rate by age
dfImrByAgeByCause = pd.read_csv("./IMR by age by cause, 2007-2016.txt", sep='\t')

# Convert NaN to Unknown for the age of infant
dfImrByAgeByCause['Age of Infant at Death'] = ["Unknown" if age is np.nan else age for age in dfImrByAgeByCause['Age of Infant at Death']]

# Remove rows with Unreliable in Death Rate column (fewer than 20 reported cases)
dfImrByAgeByCause = dfImrByAgeByCause.loc[dfImrByAgeByCause['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]

# Convert Death Rate to float
dfImrByAgeByCause['Death Rate'] = dfImrByAgeByCause['Death Rate'].map(lambda x: float(x))

# Save totals in new df
dfTotalsbyAgebyCause = dfImrByAgeByCause.loc[(dfImrByAgeByCause['Notes']=='Total') & (dfImrByAgeByCause['Age of Infant at Death']!= 'Unknown')]

# Remove Totals and summary rows
dfImrByAgeByCause = dfImrByAgeByCause[(dfImrByAgeByCause['Notes']!="Total")& (dfImrByAgeByCause["Death Rate"].notnull())]

# Sort descending by Death Rate
dfImrByAgeByCause.sort_values(by='Death Rate', ascending=False, inplace=True)

dfImrByAgeByCause.head()


# In[20]:


rects = plt.barh(dfTotalsbyAgebyCause['Age of Infant at Death'], width=dfTotalsbyAgebyCause['Death Rate'], color='blue')
plt.title("IMR vs Age")
plt.ylabel("Age of Infant at Death")
plt.xlabel("Death Rate")
plt.xlim(0, 4)
plt.savefig("IMR vs age.png")
plt.show()


# In[21]:


# removes rows that show total
dfImrByAgeByCause = dfImrByAgeByCause.loc[(dfImrByAgeByCause['Notes'] != 'Total')].sort_values(by=['Death Rate'], ascending=False).head(20)


# In[22]:


indexedImrByAgeByCause = dfImrByAgeByCause.set_index(["Age of Infant at Death", "Cause of death"])
indexedImrByAgeByCause.sort_values(["Age of Infant at Death Code", "Death Rate"], ascending=[True, False], inplace=True)
indexedImrByAgeByCause.head()


# In[23]:


x_axis = dfImrByAgeByCause['Cause of death'].head(6)

y_axis = dfImrByAgeByCause['Death Rate'].head(6)
rects = plt.bar(range(len(x_axis)),y_axis, color='teal')
plt.xticks(range(len(x_axis)), x_axis, rotation='vertical')
plt.xlim(-1,6)
plt.ylim(0, 0.65)
for rect in rects:
    indx = rects.index(rect)
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/1.1, height + 0.02,
             dfImrByAgeByCause['Age of Infant at Death'].iloc[indx],
             ha='center', va='bottom', color='black', rotation = 45)
    
plt.xlabel("Cause of Mortality")
plt.ylabel("Mortality Rate (per 1000)")
plt.title("Leading Causes of Infant Mortality")

plt.savefig("Leading Causes of Infant Mortality.png")
plt.show()


# ## Leading cause of infant mortality by race
# 

# In[24]:


dfImrByRaceByCause = pd.read_csv("./imr by race by cause, 2007-2016.txt", sep='\t')

# remove Unreliable from Death Rate colum (fewer than 20 reported cases)

dfImrByRaceByCause = dfImrByRaceByCause.loc[dfImrByRaceByCause['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]
# remove totals
dfImrByRaceByCause = dfImrByRaceByCause[(dfImrByRaceByCause['Notes']!='Total') & dfImrByRaceByCause['Death Rate'].notnull()]

# convert death rate to float
dfImrByRaceByCause['Death Rate'] = dfImrByRaceByCause['Death Rate'].map(lambda x: float(x))

# sort by race ascending, death rate descending
dfImrByRaceByCause = dfImrByRaceByCause.sort_values(['Race', 'Death Rate'], ascending=[True, False])

dfImrByRaceByCause.head()


# In[25]:


leadingCauseOfDeathByRace = pd.DataFrame()
for race in dfImrByRaceByCause['Race'].unique():
       leadingCauseOfDeathByRace = leadingCauseOfDeathByRace.append(dfImrByRaceByCause[dfImrByRaceByCause['Race'] == race][['Race', 'Cause of death', 'Death Rate']].head(1))

leadingCauseOfDeathByRace

secondLeadingCauseOfDeathByRace = pd.DataFrame()
for race in dfImrByRaceByCause['Race'].unique():
       secondLeadingCauseOfDeathByRace = secondLeadingCauseOfDeathByRace.append(dfImrByRaceByCause[dfImrByRaceByCause['Race'] == race][['Race', 'Cause of death', 'Death Rate']].head(2).tail(1))

secondLeadingCauseOfDeathByRace


thirdLeadingCauseOfDeathByRace = pd.DataFrame()
for race in dfImrByRaceByCause['Race'].unique():
       thirdLeadingCauseOfDeathByRace = thirdLeadingCauseOfDeathByRace.append(dfImrByRaceByCause[dfImrByRaceByCause['Race'] == race][['Race', 'Cause of death', 'Death Rate']].head(3).tail(1))

thirdLeadingCauseOfDeathByRace

fourthLeadingCauseOfDeathByRace = pd.DataFrame()
for race in dfImrByRaceByCause['Race'].unique():
       fourthLeadingCauseOfDeathByRace = fourthLeadingCauseOfDeathByRace.append(dfImrByRaceByCause[dfImrByRaceByCause['Race'] == race][['Race', 'Cause of death', 'Death Rate']].head(4).tail(1))


# In[26]:


causes = x_axis.unique()
races = dfImrByRaceByCause['Race'].unique()


# In[27]:


mylist = []
for cause in causes:
    for thisrace in races:
        if ((dfImrByRaceByCause['Cause of death'] == cause) & (dfImrByRaceByCause['Race'] == thisrace)).any():
            myrow = dfImrByRaceByCause.loc[(dfImrByRaceByCause['Cause of death'] == cause) & (dfImrByRaceByCause['Race'] == thisrace)]
            mylist.append({
                'Race': thisrace,
                'Cause of death': cause,
                'Death Rate' : myrow.iloc[0]['Death Rate']})
        else:
            mylist.append({
                'Race': thisrace,
                'Cause of death': cause,
                'Death Rate' : 0})

dfImrByRaceByCausePlotting = pd.DataFrame(mylist)

dfImrByRaceByCausePlotting = dfImrByRaceByCausePlotting.pivot(index='Race', columns='Cause of death', values='Death Rate')

dfImrByRaceByCausePlotting = dfImrByRaceByCausePlotting[[
 'Extreme immaturity',
 'Sudden infant death syndrome - SIDS',
 'Other ill-defined and unspecified causes of mortality',
 'Accidental suffocation and strangulation in bed',
 'Other preterm infants']]


# In[28]:


ax = dfImrByRaceByCausePlotting.plot.bar(stacked=True, ylim=(0,7), figsize=(8, 6), title="Leading Causes of of IMR by Race")
ax.set_ylabel("Death Rate (per 1000)")

fig = ax.get_figure()
fig.savefig('Leading Causes of IMR by Race.png')


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


dfImrByCountyByRace = pd.read_csv("datafiles/IMR by county by race, 2007-2016.txt", sep='\t')
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


ax = dfImrByCountyByRace.boxplot('Death Rate', by="Race", figsize=(10, 6))
fig = ax.get_figure()
ax.set_xticklabels (['American Indian/\nAlaska native', 'Asian/\nPacific Islander', 'Black/\nAfrican American', 'White'])
fig.savefig('Images/Death Rate by Race.png')


# ### ANOVA shows that one (or more) race(s) is significantly different than the rest

# In[6]:


stats.f_oneway(blacks, natives, whites, asians)


# In[7]:


blacksByCounty = dfImrByCountyByRace.set_index(['Race', 'County']).sort_values(['Race', 'Death Rate'], ascending=False).loc['Black or African American']
blacksByCounty = blacksByCounty.loc[blacksByCounty['Death Rate'].notnull()]


# In[8]:


blacksHighestImrCounties = blacksByCounty.head(10)
blacksHighestImrCounties.to_csv("datafiles/AfricanAmericanHighestImrCounties.csv")


# In[9]:


blacksLowestImrCounties = blacksByCounty.tail(10)
blacksLowestImrCounties.to_csv("datafiles/AfricanAmericanLowestImrCounties.csv")


# In[10]:


# use pairwise tukeyhsd to find out which race is significnalty different than the rest  
answer = multicomp.pairwise_tukeyhsd(dfImrByCountyByRace['Death Rate'], dfImrByCountyByRace['Race'], alpha=0.05)


# In[11]:


# reject True proves the hypothesis - that there is significant difference between two means
print(answer)


# ## Infant Mortality by Race, 2007-2016

# In[12]:


dfImrByYearByRace = pd.read_csv("datafiles/imr by year by race, 2007-2016.txt", sep='\t')


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
plt.xlabel("Year")
plt.ylabel("Death Rate (per 1000)")
plt.title ("IMR by Race, 2007-2016")
plt.rcParams["figure.figsize"] = [8, 6]
plt.savefig("Images/IMR by Race, 2007-2016.png")
plt.show()


# In[18]:


# TODO
# WHO rates by country


# ## Leading cause of infant mortality by age
# 

# In[19]:


# Death Rate by age
dfImrByAgeByCause = pd.read_csv("datafiles/IMR by age by cause, 2007-2016.txt", sep='\t')

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


# In[46]:


rects = plt.barh(dfTotalsbyAgebyCause['Age of Infant at Death'], width=dfTotalsbyAgebyCause['Death Rate'], color='blue', alpha=.5, edgecolor='black')
plt.title("IMR vs Age")
plt.ylabel("Age of Infant at Death")
plt.xlabel("Death Rate")
plt.xlim(0, 2.5)
plt.rcParams["figure.figsize"] = [11, 9]
plt.savefig("Images/IMR vs age.png")
plt.show()


# In[21]:


# removes rows that show total
dfImrByAgeByCause = dfImrByAgeByCause.loc[(dfImrByAgeByCause['Notes'] != 'Total')].sort_values(by=['Death Rate'], ascending=False).head(20)


# In[22]:


indexedImrByAgeByCause = dfImrByAgeByCause.set_index(["Age of Infant at Death", "Cause of death"])
indexedImrByAgeByCause.sort_values(["Age of Infant at Death Code", "Death Rate"], ascending=[True, False], inplace=True)
indexedImrByAgeByCause.head()


# In[148]:


x_axis = dfImrByAgeByCause['Cause of death'].head(6)

y_axis = dfImrByAgeByCause['Death Rate'].head(6)
rects = plt.bar(range(len(x_axis)),y_axis, color='teal', alpha=0.5, edgecolor='black' )

plt.xticks(range(len(x_axis)), ['Extreme\nImmaturity', 'Sudden\nInfant Death\nSyndrom\nSIDS', 'Extreme\nImmaturity', 'Other\nIll-defined/\nUnspecificed\nCauses', 'Accidental\nSuffocation\nStrangulation\nin bed', 'Other\nPreterm\nInfants'], rotation='horizontal')
plt.xlim(-1,6)
plt.ylim(0, 0.65)
for rect in rects:
    indx = rects.index(rect)
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/1.1, height + 0.02,
             dfImrByAgeByCause['Age of Infant at Death'].iloc[indx],
             ha='center', va='bottom', color='black', rotation = 45)
   
plt.xlabel("Cause of Death")
plt.ylabel("Mortality Rate (per 1000)")
plt.title("Leading Causes of Infant Mortality")
plt.rcParams["figure.figsize"] = [12, 8]
# plt.tight_layout()
plt.savefig("Images/Leading Causes of Infant Mortality.png")
plt.show()


# In[43]:


# dfImrByAgeByCause.plot('Cause of death', "Death Rate", kind='bar')


# ## Leading cause of infant mortality by race
# 

# In[25]:


dfImrByRaceByCause = pd.read_csv("datafiles/imr by race by cause, 2007-2016.txt", sep='\t')

# remove Unreliable from Death Rate colum (fewer than 20 reported cases)
dfImrByRaceByCause = dfImrByRaceByCause.loc[dfImrByRaceByCause['Death Rate'].map(lambda x: 'Unreliable' not in str(x))]

# remove totals
dfImrByRaceByCause = dfImrByRaceByCause[(dfImrByRaceByCause['Notes']!='Total') & dfImrByRaceByCause['Death Rate'].notnull()]

# convert death rate to float
dfImrByRaceByCause['Death Rate'] = dfImrByRaceByCause['Death Rate'].map(lambda x: float(x))

# sort by race ascending, death rate descending
dfImrByRaceByCause = dfImrByRaceByCause.sort_values(['Race', 'Death Rate'], ascending=[True, False])

dfImrByRaceByCause.head()


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


ax = dfImrByRaceByCausePlotting.plot.bar(stacked=True, ylim=(0,7), figsize=(11, 9),  width=0.75, title="Leading Causes of IMR by Race", rot=0)
ax.set_ylabel("Death Rate (per 1000)")
ax.set_xticklabels (['American Indian/\nAlaska native', 'Asian/\nPacific Islander', 'Black/\nAfrican American', 'White'])
fig = ax.get_figure()
fig.savefig('Images/Leading Causes of IMR by Race.png')


# ## IMR by Month Prenatal Care Began
# 

# In[29]:


dfImrByPrenatalCareStart = pd.read_csv("./datafiles/imr by prenatal care start, 2007-2016.txt", sep='\t')


# In[30]:


dfImrByPrenatalCareStart = dfImrByPrenatalCareStart[['Month Prenatal Care Began', 'Death Rate']].dropna(subset=["Month Prenatal Care Began", "Death Rate"])


# In[31]:


dfImrByPrenatalCareStart


# In[32]:


dfImrByPrenatalCareStart.plot("Month Prenatal Care Began", "Death Rate", kind='bar')


# In[33]:


dfImrByPrenatalByRace = pd.read_csv("datafiles/IMR By prenatal care by race, 2007-2016.txt", sep='\t')


# In[34]:


dfNoPrenatalcareByRace = dfImrByPrenatalByRace.loc[(dfImrByPrenatalByRace['Month Prenatal Care Began'] == 'No prenatal care') & (dfImrByPrenatalByRace['Notes']!='Total')]
dfNoPrenatalcareByRace['Death Rate'] = [float(x) for x in dfNoPrenatalcareByRace['Death Rate']]


# In[35]:


df1stMonthPrenatalcareByRace = dfImrByPrenatalByRace.loc[(dfImrByPrenatalByRace['Month Prenatal Care Began'] == '1st month') & (dfImrByPrenatalByRace['Notes']!='Total')]
df1stMonthPrenatalcareByRace['Death Rate'] = [0 if 'Unreliable' in str(x) else x for x in df1stMonthPrenatalcareByRace['Death Rate']]
df1stMonthPrenatalcareByRace['Death Rate'] = [float(x) for x in df1stMonthPrenatalcareByRace['Death Rate']]


# In[36]:


# df1stMonthPrenatalcareByRace


# In[37]:


plt.bar(np.arange(len(dfNoPrenatalcareByRace['Race'])), dfNoPrenatalcareByRace['Death Rate'], label='No Prenatal Care', width=0.25)
plt.bar(np.arange(len(df1stMonthPrenatalcareByRace['Race'])) + 0.25, df1stMonthPrenatalcareByRace['Death Rate'], label='1st Month Prenatal Care', width=0.25)
plt.xticks(np.arange(len(dfNoPrenatalcareByRace['Race'])), dfNoPrenatalcareByRace['Race'])
plt.legend()


# ## Percent of Premature Births by Race

# In[62]:


dfExtremePrematurityByRace = pd.read_csv("datafiles/extreme prematurity by race, 2007-2017.txt", sep='\t')


# In[147]:


# dfExtremePrematurityByRace.dropna(subset=['Births'])


# In[66]:


def totalForRace(df, race):
    total = df.loc[df['Bridged Race'] == race]['Births'].mean()
    return total
    


# In[87]:


dfExtremePrematurityByRace.dropna(subset=['Births'], inplace=True)


# In[67]:


totalForRace(dfExtremePrematurityByRace, "White")


# In[68]:


totalForRace(dfExtremePrematurityByRace, "Black or African American")


# In[90]:


dfExtremePrematurityByRace['Total for Race'] = dfExtremePrematurityByRace.apply((lambda x: totalForRace(dfExtremePrematurityByRace, x['Bridged Race'])), axis=1) 


# In[149]:


# dfExtremePrematurityByRace


# In[93]:


dfExtremePrematurityAfricanAmerican = dfExtremePrematurityByRace.loc[dfExtremePrematurityByRace['Bridged Race'] == 'Black or African American']


# In[95]:


# dfExtremePrematurityAfricanAmerican


# In[99]:


dfExtremePrematurity20to27 = dfExtremePrematurityByRace.loc[dfExtremePrematurityByRace['OE Gestational Age 10'] == '20 - 27 weeks']


# In[103]:


dfExtremePrematurity20to27['Percent of Total Births'] = dfExtremePrematurity20to27.apply((lambda row: row['Births']/row['Total for Race']*100), axis=1)


# In[102]:


dfExtremePrematurity20to27


# ## Include Hispanic Origin

# In[40]:


dfHispanicByCause = pd.read_csv("datafiles/imr by hispanice origin by cause, 2007-2016.txt", sep='\t')


# In[105]:


# dfHispanicByCause.sort_values(by=['Death Rate'], ascending=False).head(20)


# ## US IMR Compared to Other Wealthy Nations

# In[139]:


dfWhoByCountry = pd.read_csv("datafiles/who by country.csv.csv", header=1)


# In[140]:


dfWhoByCountry.rename(columns={'Both sexes':'IMR'}, inplace=True)
dfWhoByCountry.loc[dfWhoByCountry['Country'] == 'United Kingdom of Great Britain and Northern Ireland', 'Country'] = 'United Kingdom'
dfWhoByCountry.head()


# In[141]:


plotImrByCountry = dfWhoByCountry.groupby('Country').mean().sort_values(by='IMR', ascending=False)


# In[142]:


plotImrByCountry.head()


# In[150]:


# plt.bar(plotImrByCountry['Country'], plotImrByCountry['IMR'])
# plotImrByCountry.index


# In[177]:


rects = plt.barh(plotImrByCountry.index, plotImrByCountry['IMR'], alpha=0.5, edgecolor='black')
plt.title("IMR 2007-2017 ")
plt.xlabel("Infant Deaths per 1000 Births")

for rect in rects:
    indx = rects.index(rect)
    width = rect.get_width()

    plt.text(width - 0.2, rect.get_y()+0.2,
         plotImrByCountry['IMR'].iloc[indx].round(2),
         ha='center', va='bottom', color='black', rotation = 'horizontal')
    
rects[0].set_color('red')
plt.rcParams["figure.figsize"] = [16, 6]
plt.savefig("Images/imr by country.png")
plt.show()


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[3]:


file= "datafiles/birth_weight.csv"
birthweight_df=pd.read_csv(file)
birthweight_df


# In[4]:


total_rate = list(birthweight_df["Death Rate Per 1,000"])


# In[5]:


birthweight_df


# In[6]:


list_rate = []
sum_rate = birthweight_df["Death Rate Per 1,000"].sum()
for rate in total_rate:
    rate_percent = (rate / sum_rate) * 100
    list_rate.append(rate_percent)


# In[7]:


birthweight_df["Deaths Rate"] =list_rate
birthweight_df["Deaths Percent (%)"] = birthweight_df["Deaths Rate"].map("{0:.2f}%".format)


# In[8]:


birthweight_df


# In[9]:


rate_percent = list(birthweight_df["Deaths Rate"])
birth_weight = list(birthweight_df["Birth Weight Code"])


# In[10]:


bw_x_axis = birth_weight
bw_y_axis = rate_percent


# In[11]:


birthweight_df["Birth Weight Code"]


# In[12]:


birthweight_df["Deaths Rate"]


# In[13]:


label = [" ~ 0.5kg", "~0.9kg", "~1.5kg", "~ 1.9kg", "~2.5kg", "~3.0kg", "~3.5kg","~4.0kg","~4.5kg", "~5.0kg","5.0~8.1 kg","Not Stated"]
plt.bar(bw_x_axis, bw_y_axis, color = "#D35400", alpha = 0.5,align ="center")
plt.title(f"Birth Weights Infant Mortality Rate",fontsize=15)
plt.xlabel("Weights", fontsize= 10)
plt.ylabel("Infant Mortality Rate",fontsize= 10)
plt.xticks(bw_x_axis, label, fontsize=10, rotation=30)
plt.savefig("Images/Birth Weights Infant Mortality Rate.png")
plt.show()


# In[15]:


file= "datafiles/total_low_brith_weight_by_race.csv"
total_birthweight_df=pd.read_csv(file)
total_birthweight_df


# In[16]:


for i in range(6,10):
    total_birthweight_df[f"200{i}"]=total_birthweight_df[f"200{i}"].str.replace("%", "")


# In[17]:


for i in range(10,16):
    total_birthweight_df[f"20{i}"]=total_birthweight_df[f"20{i}"].str.replace("%", "")


# In[18]:


total_birthweight_df


# In[19]:


for i in range(6,10):
    total_birthweight_df[f"200{i}"]=total_birthweight_df[f"200{i}"].str.replace(",", "")
    total_birthweight_df[f"200{i}"]=total_birthweight_df[f"200{i}"].astype(float)


# In[20]:


for i in range(10,16):
    total_birthweight_df[f"20{i}"]=total_birthweight_df[f"20{i}"].str.replace(",", "")
    total_birthweight_df[f"20{i}"]=total_birthweight_df[f"20{i}"].astype(float)


# In[21]:


total_birthweight_df['2006'].astype(float)
total_birthweight_df.dtypes


# In[22]:


percent_race_df = pd.DataFrame(total_birthweight_df[total_birthweight_df["Data Type"].isin(["Percent"])])
total_race_df =pd.DataFrame(total_birthweight_df[total_birthweight_df["Data Type"].isin(["Number"])])


# In[23]:


race_list = list(total_race_df["Race"])


# In[24]:


race_list = race_list[0:5]


# In[25]:


percent_race_df=percent_race_df.iloc[0:5]


# In[26]:


percent_race_df["Race"] = race_list


# In[27]:


percent_race_df=percent_race_df.set_index("Race")
total_race_df=total_race_df.set_index("Race")


# In[28]:


percent_race_df = percent_race_df.drop("Data Type",axis=1)


# In[29]:


total_race_df=total_race_df.drop("Data Type",axis=1)


# In[30]:


average_percent_race_list = []
for race in race_list :
    average_percent_race_list.append(percent_race_df.loc[f"{race}"].mean())


# In[31]:


percent_race_df["Average %"] = average_percent_race_list


# In[32]:


percent_race_df.dtypes


# In[33]:


percent_race_df


# In[34]:


bw_race_x_axis = race_list 
bw_race_y_axis = list(percent_race_df["Average %"])


# In[35]:


bw_race_y_axis


# In[36]:


label = ['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White']
plt.figure(figsize=(10,8))
plt.bar(bw_race_x_axis, bw_race_y_axis, color = "#7FB3D5", alpha = 0.5,align ="center")
plt.title(f"Birth Weights Infant Mortality Rate by Race",fontsize=15)
plt.xlabel("Race", fontsize= 10)
plt.ylabel("Infant Mortality Rate (Average %)",fontsize= 10)
plt.xticks(bw_race_x_axis, label, fontsize=10, rotation=90)
plt.savefig("Images/Birth Weights Infant Mortality Rate by Race.png")
plt.show()


# In[39]:


file= "datafiles/overweight_rates.csv"
overweight_df=pd.read_csv(file)
overweight_df


# In[40]:


overweight_df = overweight_df.set_index("Location")


# In[41]:


list_overweight = list(overweight_df.loc['United States'])


# In[42]:


list_overweight


# In[43]:


overweight_df.dtypes


# In[44]:


label = ['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White']
plt.figure(figsize=(10,8))
plt.bar(label,list_overweight, color = "#8E44AD", alpha = 0.5,align ="center")
plt.title(f"Overweight and Obesity Rates for Adults by Race/Ethnicity",fontsize=15)
plt.xlabel("Race", fontsize= 10)
plt.ylabel("Average %",fontsize= 10)
plt.xticks(fontsize=10, rotation=90)
plt.ylim(0,100)
plt.savefig("Images/Overweight and Obesity Rates for Adults by Race.png")
plt.show()
#plt.xticks(x_axis, label, fontsize=10, rotation=90)


# In[46]:


file= "datafiles/total_rate_hypertension_race.csv"
hypertension_df=pd.read_csv(file)
hypertension_df


# In[47]:


hypertension_df.dtypes


# In[48]:


hypertension_df =hypertension_df.set_index("Location")


# In[49]:


list_hypertension=list(hypertension_df.loc["United States"])


# In[50]:


list_hypertension


# In[51]:


label = ['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White']
plt.figure(figsize=(10,8))
plt.bar(label,list_hypertension, color = "#EC7063", alpha = 0.5,align ="center")
plt.title(f"Prevalence of hypertension among US adults (18+)",fontsize=15)
plt.xlabel("Race", fontsize= 10)
plt.ylabel("Average %",fontsize= 10)
plt.xticks(fontsize=10, rotation=90)
plt.ylim(0,100)
plt.savefig("Images/Prevalence of hypertension among US adults.png")
plt.show()


# In[53]:


file= "datafiles/IMR_by_race.csv"
IMR_df=pd.read_csv(file)
IMR_df


# In[54]:


IMR_df=IMR_df.set_index("Location")


# In[55]:


list_IMR_rate=list(IMR_df.loc["United States"])


# In[56]:


label = ['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White']
bar_width=0.3
plt.figure(figsize=(10,8))
r1=np.arange(len(label))
r2=[x + bar_width for x in r1]
r3=[x + bar_width for x in r2]
plt.bar(r1, bw_race_y_axis,color = "#7fe5b9",width=bar_width,edgecolor='white', label='Preterm Baby')
plt.bar(r2,list_hypertension, color = "#bde592",width=bar_width,edgecolor='white', label='Hypertension')
plt.bar(r3,list_overweight, color = "#ffba50", width=bar_width,edgecolor='white', label='Overweight')
plt.plot(label, list_IMR_rate,label = "IMR Rate",color = "#fc6060", marker='o', linestyle='dashed',linewidth=2, markersize=12)
plt.title(f"Infant Mortality Rate Factors by Race",fontsize=15)
plt.xlabel("Race", fontsize= 10)
plt.ylabel("Rate (Average %)",fontsize= 10)
plt.xticks([r+bar_width for r in range(len(label))],['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White'], fontsize=10, rotation=90)
plt.savefig("Images/IMR Factors by Race.png")
plt.ylim(0,100)
plt.legend()
plt.show()


# In[57]:


get_ipython().system('jupyter nbconvert --to script kim_birth_weight.ipynb')


# In[ ]:





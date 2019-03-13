#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


file= "datafiles/birth_weight.csv"
birthweight_df=pd.read_csv(file)
birthweight_df


# In[3]:


total_rate = list(birthweight_df["Death Rate Per 1,000"])


# In[4]:


birthweight_df


# In[5]:


list_rate = []
sum_rate = birthweight_df["Death Rate Per 1,000"].sum()
for rate in total_rate:
    rate_percent = (rate / sum_rate) * 100
    list_rate.append(rate_percent)


# In[6]:


birthweight_df["Deaths Rate"] =list_rate
birthweight_df["Deaths Percent (%)"] = birthweight_df["Deaths Rate"].map("{0:.2f}%".format)


# In[7]:


birthweight_df


# In[8]:


rate_percent = list(birthweight_df["Deaths Rate"])
birth_weight = list(birthweight_df["Birth Weight Code"])


# In[9]:


bw_x_axis = birth_weight
bw_y_axis = rate_percent


# In[10]:


birthweight_df["Birth Weight Code"]


# In[11]:


birthweight_df["Deaths Rate"]


# In[12]:


label = [" ~ 0.5kg", "~0.9kg", "~1.5kg", "~ 1.9kg", "~2.5kg", "~3.0kg", "~3.5kg","~4.0kg","~4.5kg", "~5.0kg","5.0~8.1 kg","Not Stated"]
plt.figure(figsize=(10,8))
plt.bar(bw_x_axis, bw_y_axis, color = "#D35400", alpha = 0.5,align ="center")
plt.title(f"Birth Weights Infant Mortality Rate",fontsize=15)
plt.xlabel("Weights", fontsize= 10)
plt.ylabel("Infant Mortality Rate",fontsize= 10)
plt.xticks(bw_x_axis, label, fontsize=10, rotation=30)
plt.savefig("Images/bw_Birth Weights Infant Mortality Rate.png")
plt.show()


# In[13]:


file= "datafiles/total_low_brith_weight_by_race.csv"
total_birthweight_df=pd.read_csv(file)
total_birthweight_df


# In[14]:


for i in range(6,10):
    total_birthweight_df[f"200{i}"]=total_birthweight_df[f"200{i}"].str.replace("%", "")


# In[15]:


for i in range(10,16):
    total_birthweight_df[f"20{i}"]=total_birthweight_df[f"20{i}"].str.replace("%", "")


# In[16]:


total_birthweight_df


# In[17]:


for i in range(6,10):
    total_birthweight_df[f"200{i}"]=total_birthweight_df[f"200{i}"].str.replace(",", "")
    total_birthweight_df[f"200{i}"]=total_birthweight_df[f"200{i}"].astype(float)


# In[18]:


for i in range(10,16):
    total_birthweight_df[f"20{i}"]=total_birthweight_df[f"20{i}"].str.replace(",", "")
    total_birthweight_df[f"20{i}"]=total_birthweight_df[f"20{i}"].astype(float)


# In[19]:


total_birthweight_df['2006'].astype(float)
total_birthweight_df.dtypes


# In[20]:


percent_race_df = pd.DataFrame(total_birthweight_df[total_birthweight_df["Data Type"].isin(["Percent"])])
total_race_df =pd.DataFrame(total_birthweight_df[total_birthweight_df["Data Type"].isin(["Number"])])


# In[21]:


race_list = list(total_race_df["Race"])


# In[22]:


race_list = race_list[0:5]


# In[23]:


percent_race_df=percent_race_df.iloc[0:5]


# In[24]:


percent_race_df["Race"] = race_list


# In[25]:


percent_race_df=percent_race_df.set_index("Race")
total_race_df=total_race_df.set_index("Race")


# In[26]:


percent_race_df = percent_race_df.drop("Data Type",axis=1)


# In[27]:


total_race_df=total_race_df.drop("Data Type",axis=1)


# In[28]:


average_percent_race_list = []
for race in race_list :
    average_percent_race_list.append(percent_race_df.loc[f"{race}"].mean())


# In[29]:


percent_race_df["Average %"] = average_percent_race_list


# In[30]:


percent_race_df.dtypes


# In[31]:


percent_race_df


# In[32]:


bw_race_x_axis = race_list 
bw_race_y_axis = list(percent_race_df["Average %"])


# In[33]:


bw_race_y_axis


# In[34]:


label = ['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White']
plt.figure(figsize=(7,5))
plt.bar(bw_race_x_axis, bw_race_y_axis, color = "#7FB3D5", alpha = 0.5,align ="center")
plt.title(f"Birth Weights Infant Mortality Rate by Race",fontsize=15)
plt.xlabel("Race", fontsize= 10)
plt.ylabel("Infant Mortality Rate (Average %)",fontsize= 10)
plt.xticks(bw_race_x_axis, label, fontsize=10, rotation=90)
plt.savefig("Images/bw_Birth Weights Infant Mortality Rate by Race.png")
plt.show()


# In[35]:


file= "datafiles/overweight_rates.csv"
overweight_df=pd.read_csv(file)
overweight_df


# In[36]:


overweight_df = overweight_df.set_index("Location")


# In[37]:


list_overweight = list(overweight_df.loc['United States'])


# In[38]:


list_overweight


# In[39]:


overweight_df.dtypes


# In[40]:


label = ['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White']
plt.figure(figsize=(10,8))
plt.bar(label,list_overweight, color = "#8E44AD", alpha = 0.5,align ="center")
plt.title(f"Overweight and Obesity Rates for Adults by Race/Ethnicity",fontsize=15)
plt.xlabel("Race", fontsize= 10)
plt.ylabel("Average %",fontsize= 10)
plt.xticks(fontsize=10, rotation=90)
plt.ylim(0,100)
plt.savefig("Images/bw_Overweight and Obesity Rates for Adults by Race.png")
plt.show()
#plt.xticks(x_axis, label, fontsize=10, rotation=90)


# In[41]:


file= "datafiles/total_rate_hypertension_race.csv"
hypertension_df=pd.read_csv(file)
hypertension_df


# In[42]:


hypertension_df.dtypes


# In[43]:


hypertension_df =hypertension_df.set_index("Location")


# In[44]:


list_hypertension=list(hypertension_df.loc["United States"])


# In[45]:


list_hypertension


# In[46]:


label = ['American Indian', 'Asian and Pacific Islander', 'African American', 'Hispanic or Latino', 'Non-Hispanic White']
plt.figure(figsize=(10,8))
plt.bar(label,list_hypertension, color = "#EC7063", alpha = 0.5,align ="center")
plt.title(f"Prevalence of hypertension among US adults (18+)",fontsize=15)
plt.xlabel("Race", fontsize= 10)
plt.ylabel("Average %",fontsize= 10)
plt.xticks(fontsize=10, rotation=90)
plt.ylim(0,100)
plt.savefig("Images/bw_Prevalence of hypertension among US adults.png")
plt.show()


# In[47]:


file= "datafiles/IMR_by_race.csv"
IMR_df=pd.read_csv(file)
IMR_df


# In[48]:


IMR_df=IMR_df.set_index("Location")


# In[49]:


list_IMR_rate=list(IMR_df.loc["United States"])


# In[51]:


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
plt.ylim(0,100)
plt.legend()
plt.savefig("Images/bw_IMR Factors by Race.png", bb)
plt.show()


# In[ ]:





# In[ ]:





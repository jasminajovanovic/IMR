#!/usr/bin/env python
# coding: utf-8

# In[1]:


#
# Logan Caldwell
#

get_ipython().run_line_magic('matplotlib', 'notebook')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

mothers_age_state_csv = "datafiles/mothers_age_state_grouped.csv"

df_mothers_age_state = pd.read_csv(mothers_age_state_csv)

df_mothers_age_state.head(15)


# In[2]:


df_mothers_age_state.describe()

### Dropna working correctly here??
df_mothers_age_state.dropna(axis=0, how="any")
df_mothers_age_state["Age of Mother"].unique()


# In[3]:


df_mothers_age_state.mean()


# In[4]:


ages_15_19 = df_mothers_age_state[df_mothers_age_state["Age of Mother"] == "15-19 years"]
ages_20_24 = df_mothers_age_state[df_mothers_age_state["Age of Mother"] == "20-24 years"]
ages_25_29 = df_mothers_age_state[df_mothers_age_state["Age of Mother"] == "25-29 years"]
ages_30_34 = df_mothers_age_state[df_mothers_age_state["Age of Mother"] == "30-34 years"]
ages_35_39 = df_mothers_age_state[df_mothers_age_state["Age of Mother"] == "35-39 years"]
ages_40_44 = df_mothers_age_state[df_mothers_age_state["Age of Mother"] == "40-44 years"]

ages_15_19["Death Rate"] = ages_15_19["Death Rate"].str.replace("\s*\(Unreliable\)", "")
ages_20_24["Death Rate"] = ages_20_24["Death Rate"].str.replace("\s*\(Unreliable\)", "")
ages_25_29["Death Rate"] = ages_25_29["Death Rate"].str.replace("\s*\(Unreliable\)", "")
ages_30_34["Death Rate"] = ages_30_34["Death Rate"].str.replace("\s*\(Unreliable\)", "")
ages_35_39["Death Rate"] = ages_35_39["Death Rate"].str.replace("\s*\(Unreliable\)", "")
ages_40_44["Death Rate"] = ages_40_44["Death Rate"].str.replace("\s*\(Unreliable\)", "")


# In[5]:


ages_15_19["Death Rate"] = ages_15_19["Death Rate"].astype(float)
ages_20_24["Death Rate"] = ages_20_24["Death Rate"].astype(float)
ages_25_29["Death Rate"] = ages_25_29["Death Rate"].astype(float)
ages_30_34["Death Rate"] = ages_30_34["Death Rate"].astype(float)
ages_35_39["Death Rate"] = ages_35_39["Death Rate"].astype(float)
ages_40_44["Death Rate"] = ages_40_44["Death Rate"].astype(float)

ages_15_19_IMR_mean = (ages_15_19["Death Rate"].mean())
ages_20_24_IMR_mean = (ages_20_24["Death Rate"].mean())
ages_25_29_IMR_mean = (ages_25_29["Death Rate"].mean())
ages_30_34_IMR_mean = (ages_30_34["Death Rate"].mean())
ages_35_39_IMR_mean = (ages_35_39["Death Rate"].mean())
ages_40_44_IMR_mean = (ages_40_44["Death Rate"].mean())

IMR_rate_means_by_age_list = [ages_15_19_IMR_mean,ages_20_24_IMR_mean,ages_25_29_IMR_mean,ages_30_34_IMR_mean,ages_35_39_IMR_mean,ages_40_44_IMR_mean]
IMR_rate_means_by_age_list


# In[6]:


df_mothers_age_state_means = df_mothers_age_state.mean()
df_mothers_age_state_means.head()


# In[7]:


df_mothers_age_state.set_index("State")
df_mothers_age_state_grouped = df_mothers_age_state.groupby(by="State", group_keys=True,)
df_mothers_age_state.mean()


# In[8]:


age_ticks = [0,1,2,3,4,5]
age_ranges_list = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44"]

x=[0,1,2,3,4,5]


# In[9]:


m_age_IMR_plot = plt.scatter(age_ranges_list, IMR_rate_means_by_age_list, )


# In[20]:


plt.title("Mother's Age and Infant Mortality Rate")
plt.xlabel("Age of Mother")
plt.ylabel("Infant Mortality Rate")
plt.grid()
# plt.legend(loc="best", labels=age_ranges_list)
plt.xlim(-1,6)
plt.ylim(0, max(IMR_rate_means_by_age_list)+2)
plt.tight_layout()


# In[21]:


plt.show()


# In[22]:


plt.savefig("IMR_and_age_of_mother_plot")


# In[ ]:





# In[ ]:





# In[ ]:





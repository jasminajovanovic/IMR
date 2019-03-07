#!/usr/bin/env python
# coding: utf-8

# In[1]:



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import csv
import os
import pandas as pd
import scipy.stats as stats
import gmaps
from config import gkey

# Configure gmaps
gmaps.configure(api_key=gkey)


# In[2]:


filename = 'Resources/Education_Infant_Death_Records_2007_2016.csv'
filename_df = pd.read_csv(filename, encoding="ISO-8859-1")
filename_df


# In[3]:


education_sorted =filename_df.sort_values(["Death Rate"],ascending=False)
education_sorted


# In[4]:


del education_sorted['Deaths']
del education_sorted['Education Code']
del education_sorted['Births']
del education_sorted['Notes']
education_sorted.head()


# In[5]:


plt.plot(education_sorted["Death Rate"], 
            education_sorted["Education"])

# Incorporate the other graph properties
plt.style.use('seaborn')
plt.title(f"Death rate by Education level")
plt.ylabel("Death Rate")
plt.xlabel("Education")
plt.grid(True)
plt.xlim(0, 20)
plt.ylim(0, 10)
# Save the figure
plt.savefig("Resources/Education.png")

# Show plot
plt.show()


# In[6]:


x_axis = education_sorted['Education']
y_axis = education_sorted['Death Rate']
plt.tight_layout()
plt.ylabel("Death Rate")
plt.xlabel("Education")
plt.bar(x_axis, y_axis, color="b", align="center")
plt.xticks(education_sorted['Education'], rotation="vertical")

plt.savefig("Resources/rated_by_Education.png")
plt.show()


# In[7]:


countyfilename = 'Resources/County_Infant_Death_Records_2007_2016.csv'
countyfilename_df = pd.read_csv(countyfilename, encoding="ISO-8859-1")
countyfilename_df.head()


# In[8]:


#county_sorted.loc[county_sorted['Education']!= "Unknown/Not on certificate"]


# In[9]:


county_sorted =countyfilename_df.sort_values(["Death Rate"],ascending=False)
exclude_unknown = county_sorted.loc[county_sorted['Education']!= "Unknown/Not on certificate"]
exclude_unknown.head()


# In[10]:


usdafilename = 'Resources/Education_USDA.csv'
usdafilename_df = pd.read_csv(usdafilename, encoding="ISO-8859-1")
usdafilename_df


# In[11]:


del usdafilename_df['Less than a high school diploma, 2013-17']
del usdafilename_df['High school diploma only, 2013-17']
del usdafilename_df["Some college or associate's degree, 2013-17"]
del usdafilename_df["Bachelor's degree or higher, 2013-17"]
del usdafilename_df["Unnamed: 11"]
        


# In[12]:


usdafilename_df = usdafilename_df.dropna()
         


# In[13]:


renamed_code = usdafilename_df.rename(columns={"FIPS Code":"GEOID"})
renamed_code['GEOID'] = renamed_code['GEOID'].map(lambda x: int(x))
renamed_code.head()


# In[14]:


gazfilename = 'Resources/2017_Gaz_counties_national.csv'
gazfilename_df = pd.read_csv(gazfilename, encoding="ISO-8859-1")
gazfilename_df


# In[15]:


del gazfilename_df['USPS']
del gazfilename_df['ANSICODE']
del gazfilename_df["NAME"]
del gazfilename_df["ALAND"]
del gazfilename_df['AWATER']
del gazfilename_df['ALAND_SQMI']
del gazfilename_df["AWATER_SQMI"]
gazfilename_df.head()


# In[16]:


merge_table = pd.merge(renamed_code, gazfilename_df, on="GEOID")
merge_table 


# In[17]:


merge_table.columns


# In[18]:


merge_table.columns = ['GEOID', 'State', 'Area name',
       'Percent of adults with less than a high school diploma, 2013-17',
       'Percent of adults with a high school diploma only, 2013-17',
       'Percent of adults completing some college or associate\'s degree, 2013-17',
       'Percent of adults with a bachelor\'s degree or higher, 2013-17',
       'INTPTLAT',
       'INTPTLONG']
merge_table.head()


# In[19]:


merge_table.INTPTLONG.dtype


# In[20]:


# Store latitude and longitude in locations
locations = merge_table[["INTPTLAT", "INTPTLONG"]]
# Plot Heatmap
fig = gmaps.figure()
BD = merge_table["Percent of adults with a bachelor's degree or higher, 2013-17"]
# Create heat layer
heat_layer = gmaps.heatmap_layer(locations, weights=BD , 
                                 dissipating=False, max_intensity=10,
                                 point_radius=0.25)


# Add layer
fig.add_layer(heat_layer)

# Display figure
fig


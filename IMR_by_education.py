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


def weighted_education(row):
    a = row['Percent of adults with less than a high school diploma, 2013-17']*0.1
    b = row['Percent of adults with a high school diploma only, 2013-17']*0.2
    c = row["Percent of adults completing some college or associate's degree, 2013-17"]*0.5
    d = row["Percent of adults with a bachelor's degree or higher, 2013-17"]*0.8
    return (a+b+c+d)


# In[20]:


merge_table['Weighted Education Score'] = merge_table.apply(weighted_education, axis=1)


# In[21]:


merge_table.head()


# In[22]:


# Store latitude and longitude in locations
locations = merge_table[["INTPTLAT", "INTPTLONG"]]
# Plot Heatmap
fig = gmaps.figure()
BD = merge_table["Weighted Education Score"]
# Create heat layer
heat_layer = gmaps.heatmap_layer(locations, weights=BD , 
                                 dissipating=False, max_intensity=100,
                                 point_radius=0.5)


# Add layer
fig.add_layer(heat_layer)

# Display figure
fig


# ###  10 HIGHEST&LOWEST DEATH RATES by COUNTIES 

# In[23]:


higherfilename = 'Resources/AfricanAmericanHighestImrCounties.csv'
higherfilename_df = pd.read_csv(higherfilename, encoding="ISO-8859-1")
#higherfilename_df.head()


# In[24]:


higherfilename_df['County Code'] = higherfilename_df['County Code'].map(lambda x: int(x))
higherfilename_df.head()


# In[25]:


lowerfilename = 'Resources/AfricanAmericanLowestImrCounties.csv'
lowerfilename_df = pd.read_csv(lowerfilename, encoding="ISO-8859-1")
#lowerfilename_df.head()


# In[26]:


lowerfilename_df['County Code'] = lowerfilename_df['County Code'].map(lambda x: int(x))
lowerfilename_df.head()


# ### FIND HIGHEST DEATH RATE COUNTIES ON MAP

# In[27]:


highestrenamed_code = higherfilename_df.rename(columns={"County Code":"GEOID"})
highestmerge_table = pd.merge(highestrenamed_code, merge_table, on="GEOID")
#highestmerge_table 


# In[28]:


del highestmerge_table['County']
del highestmerge_table['Notes']
del highestmerge_table["Deaths"]
del highestmerge_table["Births"]
del highestmerge_table['State']
del highestmerge_table['Area name']
highestmerge_table


# In[29]:


coordinates = [
    (41.091855, -85.072230),
    (32.577195, -93.882423),
    (39.469354, -74.633758),
    (39.196927, -84.544187),
    (40.282503, -74.703724),
    (36.761006, -119.655019),
    (33.553444, -86.896536),
    (42.588240, -73.974010),
    (41.617699, -86.288159),
    (37.681045, -97.461054)
]


# In[30]:


figure_layout = {
    'width': '400px',
    'height': '300px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}
fig = gmaps.figure(layout=figure_layout)


# In[31]:


# Assign the marker layer to a variable
markers = gmaps.marker_layer(coordinates)
# Add the layer to the map
fig.add_layer(markers)
#fig


# In[32]:


fig = gmaps.figure()

fig.add_layer(heat_layer)
fig.add_layer(markers)

fig


# ### FIND LOWEST DEATH RATE COUNTIES ON MAP

# In[33]:


lowestrenamed_code = lowerfilename_df.rename(columns={"County Code":"GEOID"})
lowestmerge_table = pd.merge(lowestrenamed_code, merge_table, on="GEOID")
del lowestmerge_table['County']
del lowestmerge_table['Notes']
del lowestmerge_table["Deaths"]
del lowestmerge_table["Births"]
del lowestmerge_table['State']
del lowestmerge_table['Area name']
lowestmerge_table


# In[34]:


coordinates2 = [
    (44.670893, -93.062481),
    (42.481711, -71.394917),
    (40.848711, -73.852939	),
    (61.174250, -149.284329),
    (40.439621, -74.407430),
    (41.987196, -70.741942),
    (40.959698, -74.074727),
    (41.037890, -74.298280),
    (42.642711, -70.865107),
    (37.220777, -121.690622)
]


# In[35]:


figure_layout2 = {
    'width': '400px',
    'height': '300px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}
fig2 = gmaps.figure(layout=figure_layout2)


# In[36]:


# Assign the marker layer to a variable
markers2 = gmaps.marker_layer(coordinates2)
# Add the layer to the map
fig.add_layer(markers2)
#fig


# In[37]:


fig = gmaps.figure()

fig.add_layer(heat_layer)
fig.add_layer(markers2)

fig


# In[ ]:





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


# ### Education levels vs Death Rate in USA by CDC

# In[2]:


filename = 'datafiles/Education_Infant_Death_Records_2007_2016.csv'
filename_df = pd.read_csv(filename, encoding="ISO-8859-1")


# In[3]:


education_sorted =filename_df.sort_values(["Death Rate"],ascending=False)


# In[4]:


exclude_unknown = education_sorted.loc[education_sorted['Education']!= "Unknown/Not on certificate"]


# In[5]:


del exclude_unknown['Deaths']
del exclude_unknown['Education Code']
del exclude_unknown['Births']
del exclude_unknown['Notes']
exclude_unknown.head()


# In[ ]:





# In[6]:


plt.plot(exclude_unknown["Death Rate"], 
            exclude_unknown["Education"])

# Incorporate the other graph properties
plt.style.use('seaborn')
plt.title(f"Death rate by Education level 2007-2016")
plt.ylabel("Death Rate (per 1000)")
plt.xlabel("Education level")
plt.grid(True)
plt.xlim(2, 10)
plt.ylim(0, 9)
# Save the figure
plt.savefig("Images/Education_lever_line.png")

# Show plot
plt.show()


# In[7]:


x_axis = exclude_unknown['Education']
y_axis = exclude_unknown['Death Rate']
plt.tight_layout()
plt.ylabel("Death Rate per 1000")
plt.xlabel("Education level 2007-2016")
plt.bar(x_axis, y_axis, color="b", align="center")
plt.xticks(exclude_unknown['Education'], rotation="vertical")

plt.savefig("Images/Education_level_barchart.png")
plt.show()


# ### Education level in USA by USDA

# In[8]:


usdafilename = 'datafiles/Education_USDA.csv'
usdafilename_df = pd.read_csv(usdafilename, encoding="ISO-8859-1")


# In[9]:


del usdafilename_df['Less than a high school diploma, 2013-17']
del usdafilename_df['High school diploma only, 2013-17']
del usdafilename_df["Some college or associate's degree, 2013-17"]
del usdafilename_df["Bachelor's degree or higher, 2013-17"]
del usdafilename_df["Unnamed: 11"]
        


# In[10]:


usdafilename_df = usdafilename_df.dropna()
         


# In[11]:


renamed_code = usdafilename_df.rename(columns={"FIPS Code":"GEOID"})
renamed_code['GEOID'] = renamed_code['GEOID'].map(lambda x: int(x))
renamed_code


# In[12]:


gazfilename = 'datafiles/2017_Gaz_counties_national.csv'
gazfilename_df = pd.read_csv(gazfilename, encoding="ISO-8859-1")


# In[13]:


del gazfilename_df['USPS']
del gazfilename_df['ANSICODE']
del gazfilename_df["NAME"]
del gazfilename_df["ALAND"]
del gazfilename_df['AWATER']
del gazfilename_df['ALAND_SQMI']
del gazfilename_df["AWATER_SQMI"]
gazfilename_df.head()


# In[14]:


merge_table = pd.merge(renamed_code, gazfilename_df, on="GEOID")


# In[15]:


merge_table.columns


# In[16]:


merge_table.columns = ['GEOID', 'State', 'Area name',
       'Percent of adults with less than a high school diploma, 2013-17',
       'Percent of adults with a high school diploma only, 2013-17',
       'Percent of adults completing some college or associate\'s degree, 2013-17',
       'Percent of adults with a bachelor\'s degree or higher, 2013-17',
       'INTPTLAT',
       'INTPTLONG']
merge_table.head()


# In[17]:


def weighted_education(row):
    a = row['Percent of adults with less than a high school diploma, 2013-17']*0
    b = row['Percent of adults with a high school diploma only, 2013-17']*0.4
    c = row["Percent of adults completing some college or associate's degree, 2013-17"]*0.6
    d = row["Percent of adults with a bachelor's degree or higher, 2013-17"]*0.8
    return (a+b+c+d)


# In[18]:


merge_table['Weighted Education Score'] = merge_table.apply(weighted_education, axis=1)


# In[19]:


merge_table


# In[20]:


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


# ### Education vs High IMR by counties

# In[21]:


highcounties = 'datafiles/high_IMR_county.csv'
highcounties_df = pd.read_csv(highcounties, encoding="ISO-8859-1")
highcounties_df


# In[22]:


coordinates3 = [
    (32.577195, -93.882423),
    (30.543930, -91.093131),
    (32.267788, -90.466017),
    (39.300032, -76.610476),
    (33.553444, -86.896536),
    (35.183794, -89.895397),
    (38.635699, -90.244582),
    (39.196927, -84.544187),
    (42.284664, -83.261953),
    (35.050192, -78.828719)
]


# In[23]:


figure_layout3 = {
    'width': '400px',
    'height': '300px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}
fig3 = gmaps.figure(layout=figure_layout3)


# In[24]:


# Assign the marker layer to a variable
markers3 = gmaps.marker_layer(coordinates3)
# Add the layer to the map
fig.add_layer(markers3)
#fig


# In[25]:


fig = gmaps.figure()

fig.add_layer(heat_layer)
fig.add_layer(markers3)

fig


# ### Education vs Low IMR by counties

# In[26]:


lowcounties = 'datafiles/low_IMR_county.csv'
lowcounties_df = pd.read_csv(lowcounties, encoding="ISO-8859-1")
lowcounties_df


# In[27]:


coordinates4 = [
    (38.051817, -122.745974),
    (39.865669, -74.258864),
    (37.414672, -122.371546),
    (39.325414, -104.925987),
    (40.959698, -74.074727),
    (40.858896, -74.547292),
    (37.220777, -121.690622),
    (37.727239, -123.032229),
    (40.565527, -74.619938),
    (40.287048, -74.152446)
]


# In[28]:


figure_layout4 = {
    'width': '400px',
    'height': '300px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}
fig4 = gmaps.figure(layout=figure_layout4)


# In[29]:


# Assign the marker layer to a variable
markers4 = gmaps.marker_layer(coordinates4)
# Add the layer to the map
fig.add_layer(markers4)
#fig


# In[30]:


fig = gmaps.figure()

fig.add_layer(heat_layer)
fig.add_layer(markers4)

fig


# ### AAR Education vs Death Rate

# In[31]:


aareducation = 'datafiles/Death_Rate_by_AAR_by_Education.csv'
aareducation_df = pd.read_csv(aareducation, encoding="ISO-8859-1")


# In[32]:


aareducation_sorted =aareducation_df.sort_values(["Death Rate"],ascending=False)


# In[33]:


exclude_unknown_aar = aareducation_sorted.loc[aareducation_sorted['Education']!= "Unknown/Not on certificate"]
exclude_unknown_aar


# In[34]:


x_axis = exclude_unknown_aar['Education']
y_axis = exclude_unknown_aar['Death Rate']
plt.tight_layout()
plt.ylabel("Death Rate %")
plt.xlabel("Education level of African American Race")
plt.bar(x_axis, y_axis, color="b", align="center")
plt.xticks(exclude_unknown_aar['Education'], rotation="vertical")

plt.savefig("Images/Education_of_AAR.png")
plt.show()


# In[35]:


censusaareducation = 'datafiles/AAR_Education_2013_2017.csv'
censusaareducation_df = pd.read_csv(censusaareducation, encoding="ISO-8859-1")


# In[36]:


censusaareducation_df.dropna()


# ### Level of Education of African Americans 2013-2017

# In[37]:


x_axis = censusaareducation_df['Education']
y_axis = censusaareducation_df['Average']
plt.tight_layout()
plt.ylabel("Average %")
plt.xlabel("Education level of African American Race")
plt.bar(x_axis, y_axis, color="b", align="center")
plt.xticks(censusaareducation_df['Education'], rotation="vertical")

plt.savefig("Images/Census_Education_of_AAR.png")
plt.show()


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gmaps
from config import gkey
from scipy.stats import linregress


# In[2]:


#read census poverty data
poverty_df = pd.read_csv('datafiles/2007_2016_poverty.csv')


# In[3]:


poverty_df.head()


# In[4]:


#only keep needed columns
poverty_df = poverty_df[["Year","County ID","State / County Name","All Ages in Poverty Percent"]]


# In[5]:


poverty_df.head()


# In[6]:


#group by the County ID
poverty_group = poverty_df.groupby(["County ID"]).mean()


# In[7]:


poverty_group.head()


# In[8]:


#read table of lat/lng cooridnates for counties
location_df = pd.read_csv('datafiles/2017_counties.csv', encoding="ISO-8859-1")


# In[9]:


location_df = location_df.rename(columns={'GEOID': "County ID","INTPTLAT": "Lat","INTPTLONG": "Lng"})


# In[10]:


location_df.head()


# In[11]:


#combine poverty data with county location data
merge_table = pd.merge(poverty_df, location_df, on="County ID", how="left")


# In[12]:


merge_table.head()


# In[13]:


#group by County ID
merge_group = merge_table.groupby(["County ID"]).mean()


# In[14]:


merge_group.head()


# In[15]:


#remove rows with missing values
merge_group = merge_group.dropna(how="any")


# In[16]:


merge_group.head()


# In[17]:


#load API key
gmaps.configure(api_key=gkey)


# In[18]:


#construct heat map of poverty levels from 2007-2016
locations = merge_group[["Lat", "Lng"]].astype(float)
poverty_rate = merge_group["All Ages in Poverty Percent"].astype(float)
fig = gmaps.figure()
heat_layer = gmaps.heatmap_layer(locations, weights=poverty_rate, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = .6)


# In[19]:


fig.add_layer(heat_layer)

fig


# In[20]:


#read CDC data on top 15 states for infant death rates
death_rates_state_top_df = pd.read_csv('datafiles/death_rates_state_top.csv')


# In[21]:


death_rates_state_top_df


# In[22]:


#drop location markers on the 15 states
locations_state = death_rates_state_top_df[["Lat", "Lng"]].astype(float)
state_layer = gmaps.symbol_layer(
    locations_state, fill_color='rgba(0, 150, 0, 0.4)',
    stroke_color='rgba(0, 0, 150, 0.4)', scale=4)

#state_layer.markers[10].scale=20



fig = gmaps.figure()
fig.add_layer(state_layer)

fig


# In[23]:


#combine poverty heatmap with state location
fig = gmaps.figure()
fig.add_layer(heat_layer)
fig.add_layer(state_layer)
fig


# In[24]:


#read CDC data on death rates per county for 2006-2017
death_rates_county = pd.read_csv('datafiles/death_rates.csv')


# In[25]:


death_rates_county.head()


# In[26]:


death_rates_county = death_rates_county.rename(columns={"County Code": "County ID"})


# In[27]:


death_rates_county.head()


# In[204]:


#merge CDC data on death rates per county with poverty and county location data
regress_df = pd.merge(death_rates_county, merge_group, on="County ID", how="left")


# In[89]:


regress_df.head()


# In[205]:


#remove all rows with missing values
regress_df = regress_df.dropna(how="any")


# In[31]:


regress_df.head()


# In[32]:


#define x and y axis for regression analsys
x_axis = regress_df["All Ages in Poverty Percent"]
y_axis = regress_df["Death Rate"]


# In[33]:


(slope, intercept, _, _, _) = linregress(x_axis, y_axis)
fit = slope * x_axis + intercept


# In[34]:


#calculate statistical values
slope, intercept, r_value, p_value, std_err = linregress(x_axis, y_axis)


# In[35]:


#perform linear regression of death rate versus poverty
fig, ax = plt.subplots()

fig.suptitle("Death Rate v Poverty 2007-2016", fontsize=16, fontweight="bold")

ax.set_xlim(0,35)
ax.set_ylim(0,15)

ax.set_xlabel("Poverty Rate (%)")
ax.set_ylabel("Death Rate (per 1000)")

ax.plot(x_axis, y_axis, linewidth=0, marker='o')
ax.plot(x_axis, fit, 'b--')
plt.savefig("Images/deathrateVpoverty_linregress.png")
plt.show()


# In[36]:


p_value


# In[37]:


#start health insurance analysis
insurance_df = pd.read_csv("datafiles/insurance.csv")


# In[38]:


insurance_df.head()


# In[39]:


death_rates_state = pd.read_csv("datafiles/death_rates_state.txt", delimiter="\t")


# In[40]:


death_rates_state = death_rates_state[["State","Death Rate"]]


# In[41]:


death_rates_state = death_rates_state.dropna(how="any")


# In[42]:


death_rates_state.head()


# In[43]:


insurance_group = insurance_df.groupby("State").mean()


# In[44]:


insurance_group.head()


# In[45]:


insurance_merge = pd.merge(death_rates_state, insurance_group, on="State", how="left")


# In[46]:


insurance_merge.head()


# In[47]:


x_axis = insurance_merge["Total"]
y_axis = insurance_merge["Death Rate"]


# In[48]:


#graph the death rate versus total rate of insurance for all states
plt.scatter(x_axis, y_axis)
plt.ylabel("Death Rate (per 1000)")
plt.xlabel("Rate of Insurance Coverage (%)")
plt.title("Death Rate v Total Insurance Rate")
plt.savefig("Images/DeathRate_v_TotalInsurance.png")


# In[49]:


(slope, intercept, _, _, _) = linregress(x_axis, y_axis)
fit = slope * x_axis + intercept
slope, intercept, r_value, p_value, std_err = linregress(x_axis, y_axis)


# In[50]:


p_value


# In[51]:


x2_axis = insurance_merge["Public"]


# In[52]:


insurance_merge = insurance_merge.dropna(how="any")


# In[53]:


insurance_merge.dtypes


# In[54]:


#plot death rate versus rate of public insurance
(slope, intercept, _, _, _) = linregress(x2_axis, y_axis)
fit = slope * x2_axis + intercept
slope, intercept, r_value, p_value, std_err = linregress(x2_axis, y_axis)

fig, ax = plt.subplots()

fig.suptitle("", fontsize=16, fontweight="bold")

ax.set_xlim(15,55)
ax.set_ylim(4,10)

ax.plot(x2_axis, y_axis, linewidth=0, marker='o')
ax.plot(x2_axis, fit, 'b--')
plt.scatter(x2_axis, y_axis)
plt.ylabel("Death Rate (per 1000)")
plt.xlabel("Rate of Public Insurance Coverage (%)")
plt.title("Death Rate v Public Insurance Rate")
plt.savefig("Images/DeathRate_v_PublicInsurance.png")
plt.show()


# In[55]:


p_value


# In[56]:


x3_axis = insurance_merge["Private"]


# In[57]:


#plot death rate versus rate of private insurance
(slope, intercept, _, _, _) = linregress(x3_axis, y_axis)
fit = slope * x3_axis + intercept
slope, intercept, r_value, p_value, std_err = linregress(x3_axis, y_axis)

fig, ax = plt.subplots()

fig.suptitle("", fontsize=16, fontweight="bold")

ax.set_xlim(40,80)
ax.set_ylim(4,10)

ax.plot(x3_axis, y_axis, linewidth=0, marker='o')
ax.plot(x3_axis, fit, 'b--')
plt.scatter(x3_axis, y_axis)
plt.ylabel("Death Rate (per 1000)")
plt.xlabel("Rate of Private Insurance Coverage (%)")
plt.title("Death Rate v Private Insurance Rate")
plt.savefig("Images/DeathRate_v_PrivateInsurance")
plt.show()


# In[58]:


p_value


# In[59]:


#Start new analysis on top ten and bottom ten african american counties regarding death rate
AfricanAmerican20 = pd.read_csv("datafiles/AfricanAmerican20.csv")


# In[60]:


AfricanAmerican20


# In[61]:


AfricanAmerican20 = AfricanAmerican20.rename(columns={"County Code": "County ID"})


# In[62]:


african_merge = pd.merge(AfricanAmerican20, merge_group, on="County ID", how="left")


# In[63]:


african_merge = african_merge[["County ID","Death Rate","All Ages in Poverty Percent"]]


# In[64]:


african_merge


# In[65]:


x_axis = african_merge["All Ages in Poverty Percent"]
y_axis = african_merge["Death Rate"]


# In[66]:


african_merge.set_index("County ID").plot.bar("Death Rate")


# In[67]:


black_counties = pd.read_csv("datafiles/black_counties.csv")


# In[68]:


black_counties.head()


# In[69]:


black_merge = pd.merge(black_counties, merge_group, on="County ID", how="left")


# In[70]:


black_merge = black_merge.dropna(how="any")


# In[71]:


black_merge.head()


# In[72]:


x_axis = black_merge["All Ages in Poverty Percent"]
y_axis = black_merge["Death Rate"]
plt.scatter(x_axis, y_axis)


# In[73]:


#plot death rate versus poverty rate for African Americans
(slope, intercept, _, _, _) = linregress(x_axis, y_axis)
fit = slope * x_axis + intercept
slope, intercept, r_value, p_value, std_err = linregress(x_axis, y_axis)

fig, ax = plt.subplots()

fig.suptitle("", fontsize=16, fontweight="bold")

ax.set_xlim(4,31)
ax.set_ylim(5,18)

# ax.set_xlabel("Poverty Rate (%)")
# ax.set_ylabel("Death Rate (%)")

ax.plot(x_axis, y_axis, linewidth=0, marker='o')
ax.plot(x_axis, fit, 'b--')
plt.scatter(x_axis, y_axis)
plt.ylabel("Death Rate (per 1000)")
plt.xlabel("Poverty Rate (%)")
plt.title("Death Rate v Poverty Rate for African Americans")
plt.savefig("Images/DeathRate_v_AfricanAmericanPoverty.png")
plt.show()


# In[74]:


p_value


# In[75]:


white_counties = pd.read_csv("datafiles/white_counties.csv")


# In[76]:


white_counties.head()


# In[77]:


white_merge = pd.merge(white_counties, merge_group, on="County ID", how="left")


# In[78]:


white_merge = white_merge.dropna(how="any")


# In[79]:


#plot death rate versus poverty rate for Whites
x_axis = white_merge["All Ages in Poverty Percent"]
y_axis = white_merge["Death Rate"]

(slope, intercept, _, _, _) = linregress(x_axis, y_axis)
fit = slope * x_axis + intercept
slope, intercept, r_value, p_value, std_err = linregress(x_axis, y_axis)

fig, ax = plt.subplots()

fig.suptitle("", fontsize=16, fontweight="bold")

ax.set_xlim(4,35)
ax.set_ylim(2,8)

ax.plot(x_axis, y_axis, linewidth=0, marker='o')
ax.plot(x_axis, fit, 'b--')
plt.scatter(x_axis, y_axis)
plt.ylabel("Death Rate (per 1000)")
plt.xlabel("Poverty Rate (%)")
plt.title("Death Rate v Poverty Rate for Whites")
plt.savefig("Images/DeathRate_v_PovertyRateWhites.png")
plt.show()


# In[80]:


p_value


# In[206]:


#Heatmap with poverty per county and top ten counties deathrate
regress_df = regress_df.sort_values(by=["Death Rate"], ascending=False)


# In[207]:


regress_df = regress_df.reset_index()


# In[208]:


regress_df.head()


# In[209]:


regress_df = regress_df.iloc[0:10]


# In[210]:


regress_df


# In[211]:


regress_df.to_csv("datafiles/low_IMR_county.csv")


# In[212]:


gmaps.configure(api_key=gkey)
#construct heat map of poverty levels from 2007-2016
locations = merge_group[["Lat", "Lng"]].astype(float)
poverty_rate = merge_group["All Ages in Poverty Percent"].astype(float)
fig = gmaps.figure()
heat_layer = gmaps.heatmap_layer(locations, weights=poverty_rate, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = .6)

#drop location markers on the 10 counties
locations_county = regress_df[["Lat", "Lng"]].astype(float)
county_layer = gmaps.symbol_layer(
    locations_county, fill_color='rgba(0, 150, 0, 0.4)',
    stroke_color='rgba(0, 0, 150, 0.4)', scale=4)

fig = gmaps.figure()
fig.add_layer(heat_layer)
fig.add_layer(county_layer)
fig


# In[ ]:





# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:21:15 2020

@author: khuze
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import geopandas as gpd
from shapely.geometry import Point

data = pd.read_csv('C:/Projects/US Pipeline Accidents/Accidents data.csv')

data_on = data[data['Pipeline Location'] == 'ONSHORE'] #sampling from just onshore pipeline accidents

############################### All Accidents on Map ################################

geometry = [Point(xy) for xy in zip(data_on["Accident Longitude"], data_on["Accident Latitude"])]
geo_data = gpd.GeoDataFrame(data_on,geometry=geometry)
us_map = gpd.read_file(r'C:\Projects\Covid 19\us_states\states.shp')
data_states = data_on.groupby('Accident State').agg({'Accident Date/Time':'count', 'All Costs':'sum'})
geo_data_states = pd.merge(us_map,data_states,'left', left_on = 'STATE_ABBR', right_index = True)

plt.style.use('seaborn')
mpl.rcParams['axes.titlesize'] = 25
fig = plt.subplots(figsize = (15,10))
plt.title('US PIPELINE ACCIDENTS 2010 - 2017', loc= 'center',fontdict = {'fontsize': mpl.rcParams['axes.titlesize']})
plt.axis('off')                                    
axes =plt.gca()
axes.set_xlim([-165,-60])
axes.set_ylim([17,75])


geo_data_states.plot(column = 'All Costs', label = 'Costs', ax = axes, alpha = 1, legend = True, cmap = 'Oranges', legend_kwds={'label': "Costs of Accidents",
                                                                                                                            'orientation' : 'horizontal'})
geo_data.plot(ax = axes, label = 'Accidents', markersize = 3, color = 'grey', marker = "o")
plt.show()
plt.close()

plt.savefig('accidents_map.png')
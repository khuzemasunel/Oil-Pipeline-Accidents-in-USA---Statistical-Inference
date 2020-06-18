# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:45:14 2020

@author: khuze
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import geopandas as gpd
from shapely.geometry import Point, Polygon
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
from util import Utility
#import geoplot

data = pd.read_csv('C:/Projects/US Pipeline Accidents/Accidents data.csv')
#cols_of_interest = ['Accident Date/Time','Accident State','Pipeline Location','Liquid Type','Cause Category','Net Loss (Barrels)','All Costs']
#data = data[cols_of_interest] #remove columns not needed for this analysis
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
####divider = make_axes_locatable(axes)
###cax = divider.append_axes("right", size="5%", pad=0.1)

geo_data_states.plot(column = 'All Costs', label = 'Costs', ax = axes, alpha = 1, legend = True, cmap = 'Oranges', legend_kwds={'label': "Costs of Accidents",
                                                                                                                            'orientation' : 'horizontal'})
geo_data.plot(ax = axes, label = 'Accidents', markersize = 3, color = 'grey', marker = "o")
plt.show()
plt.close()

plt.savefig('us_map.png')



#data_on['Accident Date/Time'] = pd.to_datetime(data_on['Accident Date/Time'])
#data_on.sort_values(by=['Accident Date/Time'], ascending = True, inplace = True) 
#data_on['timetoAccident'] = data_on['Accident Date/Time'].diff()
#data_on['timetoAccident_h'] = data_on.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#
#print(data_on['timetoAccident_h'].mean())
#
#sns.set(style="darkgrid")
##data_on = sns.load_dataset("data_on")
#ax = sns.boxplot(x=data_on["timetoAccident_h"], color = 'Red', linewidth = 3, data = data_on)
#plt.xlabel('Time To Accident (h)')
#plt.show()
#plt.close()

############################### Data analysis for liquid types ################################

#data_on_grouped_lt = data[data['Pipeline Location'] == 'ONSHORE']
#data_on_grouped_lt ['Accident Date/Time'] = pd.to_datetime(data_on_grouped_lt ['Accident Date/Time'])
#data_on_grouped_lt .sort_values(by=['Accident Date/Time'], ascending = True, inplace = True) 
#data_on_grouped_lt ['timetoAccident'] = data_on_grouped_lt .groupby('Liquid Type')['Accident Date/Time'].diff()
#data_on_grouped_lt['Liquid Type'] = data_on_grouped_lt['Liquid Type'].map({'HVL OR OTHER FLAMMABLE OR TOXIC FLUID, GAS':'HVL',
#                      'CRUDE OIL':'CRUDE OIL',
#                      'REFINED AND/OR PETROLEUM PRODUCT (NON-HVL), LIQUID' : 'NON-HVL',
#                      'CO2 (CARBON DIOXIDE)':'CO2',
#                      'BIOFUEL / ALTERNATIVE FUEL(INCLUDING ETHANOL BLENDS)':'BIOFUEL/ALTERNATIVE'})
#data_on_grouped_lt= data_on_grouped_lt[data_on_grouped_lt.timetoAccident.notnull()]
#data_on_grouped_lt['timetoAccident_h'] = data_on_grouped_lt.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#
#ax = sns.boxplot(x="Liquid Type", y=data_on_grouped_lt['timetoAccident_h'], data=data_on_grouped_lt[data_on_grouped_lt['Liquid Type'] != 'BIOFUEL/ALTERNATIVE' ])
#ax.set(yscale="log")
#plt.show()
#plt.close()
#
#print(data_on_grouped_lt.groupby('Liquid Type').count())
#print(data_on_grouped_lt['Liquid Type'].unique())


############################### Data analysis for Cause Category ################################

#data_on_grouped_cc = data[data['Pipeline Location'] == 'ONSHORE']
#data_on_grouped_cc['Accident Date/Time'] = pd.to_datetime(data_on_grouped_cc ['Accident Date/Time'])
#data_on_grouped_cc .sort_values(by=['Accident Date/Time'], ascending = True, inplace = True)
#data_on_grouped_cc ['timetoAccident'] = data_on_grouped_cc.groupby('Cause Category')['Accident Date/Time'].diff()
#data_on_grouped_cc['Cause Category'] = data_on_grouped_cc['Cause Category'].map({'MATERIAL/WELD/EQUIP FAILURE':'MAT/EQUIP FAIL',
#                      'CORROSION':'CORROSION',
#                      'EXCAVATION DAMAGE' : 'EXCAVATION DAMAGE',
#                      'INCORRECT OPERATION':'INCORRECT OPERATION',
#                      'NATURAL FORCE DAMAGE':'NATURAL FORCE',
#                      'ALL OTHER CAUSES':'OTHER',
#                      'OTHER OUTSIDE FORCE DAMAGE':'OTHER OUTSIDE FORCE'})
#data_on_grouped_cc= data_on_grouped_cc[data_on_grouped_cc.timetoAccident.notnull()]
#data_on_grouped_cc['timetoAccident_h'] = data_on_grouped_cc.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#
#ax = sns.boxplot(x="Cause Category", y=data_on_grouped_cc['timetoAccident_h'], data=data_on_grouped_cc)
#ax.set(yscale="log")
#plt.xticks(rotation=90)
#plt.show()
#plt.close()
#
#print(data_on_grouped_cc.groupby('Cause Category').count())
#print(data_on_grouped_cc['Cause Category'].unique()) 


############################### Data analysis for Material Equipment Failure groupeb by accident year ################################

#data_on_MEF = data_on[data_on['Cause Category'] == 'MATERIAL/WELD/EQUIP FAILURE']
#data_on_MEF['Accident Date/Time'] = pd.to_datetime(data_on_MEF ['Accident Date/Time'])
#data_on_MEF.sort_values(by=['Accident Date/Time'], ascending = True, inplace = True)
#data_on_MEF['timetoAccident'] = data_on_MEF.groupby('Accident Year')['Accident Date/Time'].diff()
#data_on_MEF['timetoAccident_h'] = data_on_MEF.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#ax = sns.boxplot(x="Accident Year", y=data_on_MEF['timetoAccident_h'], data=data_on_MEF)
#plt.show()
#plt.close()


############################### Data analysis for CO2 ################################

#data_on_CO2 = data_on[data_on['Liquid Type'] == 'CO2 (CARBON DIOXIDE)']
#data_on_CO2['Accident Date/Time'] = pd.to_datetime(data_on_CO2 ['Accident Date/Time'])
#data_on_CO2.sort_values(by=['Accident Date/Time'], ascending = True, inplace = True)
#data_on_CO2['timetoAccident'] = data_on_CO2['Accident Date/Time'].diff()
#data_on_CO2['timetoAccident_h'] = data_on_CO2.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#ax = sns.boxplot(x="Liquid Type", y=data_on_CO2['timetoAccident_h'], data=data_on_CO2)
#plt.show()
#plt.close()

############################### Statistical Inference - Poisson Distribution ################################

################ Bootstrap Samples #########################

#for a in range(100):
#    bs_sample = np.random.choice(data_on['timetoAccident_h'], size=len(data_on['timetoAccident_h']))
#    x, y = Utility.ecdf(bs_sample)
#    _ = plt.plot(x, y, marker='.', linestyle='none',
#                 color='gray', alpha=0.1)
#
#x, y = Utility.ecdf(data_on['timetoAccident_h'])
#_ = plt.plot(x, y, marker='.', color = 'blue', alpha = .01)
#
#plt.margins(0.02)
#_ = plt.xlabel('Hours between accidents')
#_ = plt.ylabel('ECDF')
#plt.show()
#
#plt.close()
#
################# Confidence Interval on mean time to accident #########################
#
#bs_replicates = Utility.draw_bs_reps(Utility,data_on['timetoAccident_h'], np.mean, size=10000)
#sem = np.std(data_on['timetoAccident_h']) / np.sqrt(len(data_on['timetoAccident_h']))
#print(sem)
#bs_std = np.std(bs_replicates)
#print(bs_std)
#_ = plt.hist(bs_replicates, bins=50, density=True, alpha = .8, color = 'red')
#_ = plt.xlabel('mean time to accident (h)')
#_ = plt.ylabel('PDF')
#plt.show()
#
#conf_int = np.percentile(bs_replicates,[2.5, 97.5])
#print('95% confidence interval =', conf_int, 'hours')


#data_on_MEF.sort_values(by=['Accident Date/Time'], ascending = True, inplace = True)
#data_on_MEF.sort_values(by=['Accident Date/Time'], ascending = True, inplace = True)
#data_on_MEF['timetoAccident'] = data_on_MEF.groupby('Accident Year')['Accident Date/Time'].diff()
#data_on_MEF= data_on_MEF[data_on_MEF.timetoAccident.notnull()]
#data_on_MEF['timetoAccident_h'] = data_on_MEF.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#
#x,y = Utility.ecdf(data_on_MEF['timetoAccident_h'])
#_ = plt.plot(x, y, marker='.', linestyle='none')
#_ = plt.xlabel('Time to Accident (h)')
#_ = plt.ylabel('ECDF')


## hypothesis testing ####

data_on ['Accident Date/Time'] = pd.to_datetime(data_on['Accident Date/Time'])
data_on .sort_values(by=['Accident Date/Time'], ascending = True, inplace = True) 
data_on ['timetoAccident'] = data_on['Accident Date/Time'].diff()
data_on['timetoAccident_h'] = data_on.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
data_on= data_on[data_on.timetoAccident.notnull()]

data_on_grouped = data_on.groupby('Accident State').agg({'timetoAccident':'count', 'timetoAccident_h':'mean','All Costs' : 'sum'})

#data_LA = data_on[data_on['Accident State'] == 'LA']
#data_LA ['Accident Date/Time'] = pd.to_datetime(data_LA['Accident Date/Time'])
#data_LA ['timetoAccident'] = data_LA['Accident Date/Time'].diff()
#data_LA['timetoAccident_h'] = data_LA.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#data_LA= data_LA[data_LA.timetoAccident.notnull()]
#
#print('La mean: {0}'.format(np.mean(data_LA['timetoAccident_h'])))
#
#data_KS = data_on[data_on['Accident State'] == 'KS']
#data_KS ['Accident Date/Time'] = pd.to_datetime(data_KS['Accident Date/Time'])
#data_KS ['timetoAccident'] = data_KS['Accident Date/Time'].diff()
#data_KS['timetoAccident_h'] = data_KS.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#data_KS= data_KS[data_KS.timetoAccident.notnull()]
#
#print('KS mean: {0}'.format(np.mean(data_KS['timetoAccident_h'])))
#
#
#data_CA = data_on[data_on['Accident State'] == 'CA']
#data_CA ['Accident Date/Time'] = pd.to_datetime(data_CA['Accident Date/Time'])
#data_CA ['timetoAccident'] = data_CA['Accident Date/Time'].diff()
#data_CA['timetoAccident_h'] = data_CA.apply(lambda x: x['timetoAccident'].days * 24 + x['timetoAccident'].seconds/3600, axis = 1)
#data_CA= data_CA[data_CA.timetoAccident.notnull()]
#
#print('CA mean: {0}'.format(np.mean(data_CA['timetoAccident_h'])))










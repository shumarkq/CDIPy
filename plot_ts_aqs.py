import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

for period in ['weekdays']:
    #read aqs data
    aqsdata = pd.read_csv('../data/unpair_aqs_%s.csv' % period).drop(columns=['Unnamed: 0'])
    #select sites
    lon = aqsdata.lon
    lat = aqsdata.lat
    latlon = list(zip(lat.unique(), lon.unique()))
    sites = dict()
    for index, v in enumerate(latlon):
        sites[index] = aqsdata[(lat==latlon[index][0])&(lon==latlon[index][1])].reset_index(drop=True)

    #get daily mean data
    dailymeans = dict()
    for k, v in sites.items():
        date = [v.time[i].split(' ')[0] for i in v.index]
        v['date'] = date
        dailymean = pd.DataFrame(v.date.unique(), columns=['date'])
        slices = np.arange(len(v)) // 20
        for spe in ['NO','NO2','NOx','rNO2dNOx','lat','lon']:
            dailymean[spe] = v.groupby([slices, 'date'], as_index=False)[spe].mean()[spe]
        dailymeans[k] = dailymean


    for spe in ['NOx','rNO2dNOx']:
        fig = plt.figure(figsize=(10,4))
        ax = fig.add_axes([.1,.15,.8,.8])
        ls = ['-','--',':']
        colors = ['green','blue','magenta']
        labels = ['Site3 (Near east Oakland city)', 'Site1 (Near west Oaqskland city)', 'Site2 (Near West Oakland highway)']
        for k, v in dailymeans.items():
            ax.plot(v.date, v[spe], lw='1', color=colors[k], label=labels[k], ls=ls[k])
        xticks = dailymeans[1].date[::30]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=20, fontsize=6)
        ax.legend()
        ax.set_xlabel('day')
        ax.set_ylabel('%s' % spe)
        fig.savefig('../figures/plt_ts_%s_%s.png' % (spe, period), dpi=300)

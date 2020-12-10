import matplotlib.pyplot as plt
import pandas as pd

for period in ['weekdays']:
    aqsdata = pd.read_csv('../data/unpair_aqs_%s.csv' % period)
    lon = aqsdata.lon
    lat = aqsdata.lat
    latlon = list(zip(lat.unique(), lon.unique()))
    print(latlon)

    sites = dict()
    for index, v in enumerate(latlon):
        sites[index] = aqsdata[(lat==latlon[index][0])&(lon==latlon[index][1])]


    fig = plt.figure(figsize=(6,6))
    ax = fig.add_axes([.15,.15,.75,.75])
    colors = ['green','blue','magenta']
    labels = ['Site3 (Near east Oakland city)', 'Site1 (Near west Oakland city)', 'Site2 (Near West Oakland highway)']
    markers = ['+','.','^']
    scales = [10, 2, 1]
    alphas = [1, 0.7, 0.5]
    for k, v in sites.items():
        ax.scatter(v.NOx, v.rNO2dNOx, color=colors[k], s=scales[k], marker=markers[k], label=labels[k], alpha=alphas[k])
    #ax.scatter(sites[2].NOx, sites[2].rNO2dNOx, s=2)
    ax.legend()
    ax.axhline(0.32, color='black')
    ax.set_xlabel('NOx (ppb)')
    ax.set_ylabel('NO2/NOx')

    fig.savefig('../figures/plt_scatter_%s.png' % period, dpi=300)
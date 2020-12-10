import matplotlib.pyplot as plt
import tilemapbase
import matplotlib as mpl
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
mbdata = pd.read_csv('../data/paired_mobile.csv')
aqsdata = pd.read_csv('../data/paired_aqs_weekdays.csv')

con1 = mbdata.lat >= np.percentile(mbdata.lat, 53)
con2 = mbdata.lat <= np.percentile(mbdata.lat, 99)
con3 = mbdata.lon >= np.percentile(mbdata.lon, 3)
con4 = mbdata.lon <= np.percentile(mbdata.lon, 43)
WO = mbdata[con1 & con2 & con3 & con4]


# create open street map
tilemapbase.init(create=True)
tile = tilemapbase.tiles.Carto_Light
extent = tilemapbase.Extent.from_lonlat(np.percentile(mbdata.lon, 3),\
                                        np.percentile(mbdata.lon, 43),\
                                        np.percentile(mbdata.lat, 53),\
                                        np.percentile(mbdata.lat, 99),\
                                        )

# plot scatter
def get_xy(data, spe=''):
    list_x = []
    list_y = []
    for index in data.index:
        x, y = tilemapbase.project(data.lon[index], data.lat[index])
        list_x.append(x)
        list_y.append(y)
        c = data[spe]
    return (list_x, list_y, c)

def plotcolorbar(spe, ax, cmap, norm):
    axins = inset_axes(ax, width='70%', height='2%', loc='lower left', bbox_to_anchor=(0.01,0.08,1,1), bbox_transform=ax.transAxes)
    cbar = mpl.colorbar.ColorbarBase(axins, cmap=cmap, norm=norm, extend='max', orientation='horizontal')
    cbar.ax.xaxis.set_ticks_position('bottom')
    cbar.ax.xaxis.set_label_position('bottom')
    cbar.ax.tick_params(direction='in')
    cbar.ax.set_xlabel('%s' % spe)

for spe in ['rNO2dNOx']:
#for spe in ['NO', 'NO2']:
    fig = plt.figure(figsize=(5, 6))
    ax = fig.add_axes([.05, .05, .9, .9])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    plotter = tilemapbase.Plotter(extent, tile, width=300)
    plotter.plot(ax, tile)
    mobile = get_xy(WO, spe)
    aqs = get_xy(aqsdata, spe)
    cmap = plt.cm.jet
    print(np.percentile(mobile[2],np.arange(0,110,10)))
    #norm = mpl.colors.Normalize(vmin=0, vmax=40)
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    ax.scatter(mobile[0], mobile[1], c=mobile[2], s=2, marker='s', cmap=cmap, norm=norm)
    ax.scatter(aqs[0], aqs[1], c=aqs[2], marker='*', s=100, edgecolor='black', cmap=cmap, norm=norm)
    ax.set_title('%s' % spe)
    plotcolorbar(spe, ax, cmap, norm)
    fig.savefig('../figures/plt_spatial_WO_%s.png' % spe, dpi=300)


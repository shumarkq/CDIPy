import pandas as pd
from datetime import datetime


#process to save mobile data
mbpath= '../data/Data_MedDriveMeans_EDF_Jan2018_ForDownload.csv'
mbdata = pd.read_csv(mbpath, sep=",", header=1, low_memory = False)
mbdata.rename(columns={'Longitude':'lon','Latitude':'lat','NO Value':'NO','NO2 Value':'NO2','BC Value':'BC'}, inplace=True)
mbdata.eval('NOx = NO + NO2', inplace=True)
mbdata.eval('rNOdNO2 = NO / NO2', inplace=True)
mbdata.eval('rNO2dNOx = NO2 / NOx', inplace=True)
#mbdata.to_csv('../data/paired_mobile.csv')

def get_data(year, spe='', period=''):
    aqspath = '../data/hourly_%s_%s.csv' % (spe, year)
    aqs = pd.read_csv(aqspath, sep=",", low_memory = False)
    data = aqs.filter(items=['Latitude','Longitude','Date Local', 'Time Local', 'State Name','County Name','Parameter Name','Sample Measurement'])

    #extract location
    con1 = data.Latitude >= mbdata.lat.min()
    con2 = data.Latitude <= mbdata.lat.max()
    con3 = data.Longitude >= mbdata.lon.min()
    con4 = data.Longitude <= mbdata.lon.max()
    data = data[con1&con2&con3&con4]

    #extract daytime
    daytime = (data['Time Local'] >= '09:00') & (data['Time Local'] <= '18:00')
    data = data[daytime]

    #extract project period
    if year == 2015:
        data = data[data['Date Local'] >= '2015-06-01']
    else:
        data = data[data['Date Local'] <= '2016-05-31']

    #select weekday and weekends
    weekday = [datetime.strptime(i, "%Y-%m-%d").isoweekday() for i in data['Date Local']]
    data['weekday'] = weekday
    if period == 'weekdays':
        data = data[data.weekday <= 5]
    elif period == 'weekends':
        data = data[data.weekday > 5]
    else:
        pass

    data = data.filter(items=['Latitude', 'Longitude', 'Date Local', 'Time Local', 'Parameter Name', 'Sample Measurement'])

    if spe == 'NO':
        data = data[data['Parameter Name'] == 'Nitric oxide (NO)']
    else:
        pass
    return(data)


#process aqs data to create and save annual mean data to pair with mobile data
for period in ['all','weekdays','weekends']:
    aqs = dict()
    for spe in ['NO','NO2']:
        data_2015 = get_data(2015, spe, period)
        data_2016 = get_data(2016, spe, period)
        frames = [data_2015, data_2016]
        merged = pd.concat(frames)
        merged = merged.groupby(['Latitude','Longitude'], as_index=False).mean()
        merged = merged.filter(items=['Latitude','Longitude','Sample Measurement'])
        merged.rename(columns={'Latitude':'lat','Longitude':'lon','Sample Measurement': spe}, inplace=True)
        aqs[spe] = merged
    paired = aqs['NO2']
    paired['NO'] = aqs['NO']['NO']
    paired.eval('NOx = NO + NO2', inplace = True)
    paired.eval('rNO2dNOx = NO2 / NOx', inplace=True)
    paired.to_csv('../data/paired_aqs_%s.csv' % period)


#process aqs data to create and save temporal data to do time series analysis
for period in ['all','weekdays','weekends']:
    aqs = dict()
    for spe in ['NO','NO2']:
        data_2015 = get_data(2015, spe, period)
        data_2016 = get_data(2016, spe, period)
        frames = [data_2015, data_2016]
        merged = pd.concat(frames).reset_index()
        strtime = [merged['Date Local'][i] + ':' + merged['Time Local'][i] for i in merged.index]
        merged['time'] = [datetime.strptime(i, '%Y-%m-%d:%H:%M') for i in strtime]
        merged = merged.filter(items=['time','Latitude','Longitude','Sample Measurement'])
        merged.rename(columns={'Latitude':'lat','Longitude':'lon','Sample Measurement': spe}, inplace=True)
        aqs[spe] = merged
    unpair = aqs['NO2']
    unpair['NO'] = aqs['NO']['NO']
    unpair.eval('NOx = NO + NO2', inplace = True)
    unpair.eval('rNO2dNOx = NO2 / NOx', inplace = True)
    unpair.to_csv('../data/unpair_aqs_%s.csv' % period)




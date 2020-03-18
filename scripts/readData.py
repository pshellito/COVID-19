# This script will read data from John's Hopkins about the death count in each country
# good site for basic map stuff: https://github.com/matplotlib/matplotlib/issues/11596
# Data source: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Directory holding daily reports
dailyDataDir = '../csse_covid_19_data/csse_covid_19_daily_reports/'
# Directory in which to place figures
figDir = '../figures/'

# Date to plot
dateToPlot = dt.date(2020,3,17)
dateStr = dateToPlot.strftime('%m-%d-%Y')
# Calculate change since
oldDate = dt.date(2020,3,16)
oldDateStr = oldDate.strftime('%m-%d-%Y')

# Current file name to plot
fnToPlot = dailyDataDir + dateStr + '.csv'
# Read in data to pandas dataframe
newDf = pd.read_csv(fnToPlot)
# Old file name to difference from
oldFn = dailyDataDir + oldDateStr + '.csv'
# Read in previous date's data to pandas dataframe
oldDf = pd.read_csv(oldFn)

# Add a field for combined Province/State and Country/Region
newDf['joinedLoc'] = ''
oldDf['joinedLoc'] = ''

for index, row in newDf.iterrows():
    newDf.loc[index, 'joinedLoc'] = (str(row['Province/State']) + row['Country/Region']).replace(' ','')
for index, row in oldDf.iterrows():
    oldDf.loc[index, 'joinedLoc'] = (str(row['Province/State']) + row['Country/Region']).replace(' ','') 
# Add a field for newDeaths
newDf['newDeaths'] = 0

# Select US locations
###idcsToPlot = newDf.index[newDf['Country/Region']=='US'].tolist()
# Select all locations
idcsToPlot = list(range(0,len(newDf)))

# Loop through locations
for ii in range(0,len(idcsToPlot)):
    # The unique location identifier of this row
    thisLoc = newDf.loc[idcsToPlot[ii],'joinedLoc']
    # The index of this location in the oldDf
    oldLocIdx = oldDf.index[oldDf['joinedLoc'] == thisLoc].tolist()
    if oldLocIdx:
        newDf.loc[idcsToPlot[ii],'newDeaths'] = newDf.loc[idcsToPlot[ii],'Deaths'] - oldDf.loc[oldLocIdx,'Deaths'].item()

# Scale markers by
markerScale = 0.1

# Create map
# Figure size
width = 21
height = 9
# Map extent
minLon = -125
maxLon = -67
minLat = 25
maxLat = 53
minLon = -168
maxLon = 180
minLat = -57
maxLat = 75
# Open figure
mapFig = plt.figure(figsize=(width, height))
# Open axis
ax = mapFig.gca()
# Set up map projection with coastlines
mm = Basemap(projection='cyl', llcrnrlat=minLat, urcrnrlat=maxLat, \
        llcrnrlon=minLon, urcrnrlon=maxLon, resolution='l', lon_0=0) # Available 'c','l','i','h','f'
# Add country lines
mm.drawcountries(color='darkgray', zorder=1)
# Add state lines
mm.drawstates(color='darkgray', zorder=1)
# Add coastlines
mm.drawcoastlines(color='darkgray', zorder=1)
# Fill continents
mm.fillcontinents(color='lightgray', lake_color='lightsteelblue', zorder=0)
# Fill oceans
mm.drawmapboundary(fill_color='lightsteelblue')
# Initialize Total deaths and Total new deaths
totDeaths = 0
totNewDeaths = 0
# Loop through locations to display
for ii in range(0,len(idcsToPlot)):
    lon = newDf.iloc[idcsToPlot[ii]]['Longitude']
    lat = newDf.iloc[idcsToPlot[ii]]['Latitude']
    deaths = newDf.iloc[idcsToPlot[ii]]['Deaths']
    newDeaths = newDf.loc[idcsToPlot[ii],'newDeaths']
    scaledVal = deaths*markerScale
    if deaths > 0:
        ax.scatter(lon, lat, s=deaths, marker='o', linewidth=2, facecolors='none', edgecolors='sienna', label='Deaths')
    if newDeaths > 0:
        ax.scatter(lon, lat, s=newDeaths, marker='o', facecolors='r', edgecolors='none', label='New deaths')
    if deaths > 0 and newDeaths > 0 and deaths!=newDeaths:
        textStr = str(deaths) + ' (' + str(newDeaths) + ')'
    elif newDeaths > 0:
        textStr = '(' + str(newDeaths) + ')'
    elif deaths > 0:
        textStr = str(deaths)
    else:
        textStr = ''
    ax.text(lon,lat, textStr)
    totDeaths += deaths
    totNewDeaths += newDeaths

plt.title(str(totDeaths) + ' COVID-19 deaths as of ' + dateStr + ' (' + str(totNewDeaths) + ' new since ' + oldDateStr +') Source: Johns Hopkins')
# Add legend
ss1 = ax.scatter(0, 20, s=100, marker='o', linewidth=2, facecolors='none', edgecolors='sienna', zorder=-1)
ss2 = ax.scatter(0, 20, s=50, marker='o', facecolors='r', edgecolors='none', zorder=-1)
ax.legend((ss1, ss2),('Deaths to-date', '(New deaths)'), loc='upper left')
# Print the figure
figName = figDir + dateStr + '_covid19deaths.png'
print('Printing ' + figName + '...')
plt.savefig(figName, bbox_inches='tight')


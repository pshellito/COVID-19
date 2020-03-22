# This script will read data from John's Hopkins about the death count in each country
# good site for basic map stuff: https://github.com/matplotlib/matplotlib/issues/11596
# Data source: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from deathPlotUtils import plotRegion


# Regions to plot
regionList = ['globe', 'northAmerica', 'europe', 'middleEast', 'eastAsia']
# Date to plot
dateToPlot = dt.date(2020,3,15)

for thisRegion in regionList:
    figName = plotRegion(dateToPlot, region=thisRegion)


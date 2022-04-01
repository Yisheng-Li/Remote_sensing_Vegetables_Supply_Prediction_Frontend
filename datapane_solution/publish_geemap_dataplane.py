
import ee

import rasterio
import geopandas as gpd
import geemap.eefolium as geemap
import datapane


# geemap.update_package()
# Authenticate the Google earth engine with google account
ee.Authenticate()
ee.Initialize()

lat, long = 44.201128, -78.556023
size = 0.06
cords = [[long-1.5*size, lat+size], [long-1.5*size, lat-size],
         [long+1.5*size, lat-size], [long+1.5*size, lat+size]]
aoi = ee.Geometry.Polygon(cords, None, False) #order is longitude then latitude.

dataset = ee.Image('USGS/SRTMGL1_003') # 30 m pixels, could not download the file.
elevation = dataset.select('elevation');
slope = ee.Terrain.slope(elevation);
aspect = ee.Terrain.aspect(elevation)
shade = ee.Terrain.hillshade(elevation)
clipped_elev = elevation.clip(aoi)
clipped_slope = slope.clip(aoi)
clipped_aspect = aspect.clip(aoi)

vis_elev = {'min': 200,'max': 350,'palette': ['blue', 'green', 'orange',  'red']}
vis_slope = {'min': 0,'max':10,'palette': ['blue', 'green', 'orange',  'red']}
sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR");
image = sentinel2.filterBounds(aoi).filterDate('2021-12-10' , '2021-12-15').mosaic().clip(aoi)

Map = geemap.Map(zoom= 12)
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'true color')
Map.addLayer(clipped_slope, vis_slope, 'slope')
Map.addLayer(clipped_elev, vis_elev, 'dem')
image = sentinel2.filterBounds(aoi).filterDate('2021-12-10' , '2021-12-15').mosaic().clip(aoi)
Map.addLayer((image.select('B8').subtract(image.select('B4')))\
             .divide(image.select('B4').add(image.select('B8'))),
             {'min': -0.3, 'max': 0.99, 'palette': ['red', 'orange', 'yellow', 'green']}, 'NDVI')
Map.setCenter(long, lat)


# publish the above built geemap to datapane
# the datapane module can be embedded into a webpage
# visibility: 
# 1.Default (unlisted): You have unlimited default reports, which allow anyone with the URL to access them, 
#   but they won't appear on your profile or in search results. This is not a truly private system, 
#   so make sure you aren't uploading very sensitive information.
# 2.Portfolio: You can also choose to add the report to your public portfolio (see example) which you can share with potential employers/readers. 
#   This is a great way to gain an audience and receive feedback on your reports! 
# 3.Private: Your Community account comes with a limited number of private reports if you need to share data confidentially within your organization. 
#   Private reports are shared through the Report Notifications mechanism. 

# details: https://www.youtube.com/watch?v=NNrrLBIqroY
Map.publish(name='gee folium map', headline='Terrain Visualization', visibility="PRIVATE")




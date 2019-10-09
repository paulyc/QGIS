#iface.newProject()
canvas=iface.mapCanvas()

project=QgsProject.instance()
crs=QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId)
project.setCrs(crs)
for layer in project.mapLayers().values():
    layer.setCrs(crs)


#url='https://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png'
#iface.addRasterLayer(url, layerName, providerKey)

providerKey='wms'
url='type=xyz&url=https://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0'
layerName='OpenStreetMap'
rasterLyr = QgsRasterLayer(url, layerName, providerKey)

project.addMapLayer(rasterLyr)
#EPSG:3857 - WGS 84 / Pseudo-Mercator - Projected

radar=iface.addRasterLayer('/home/paulyc/Development/QGIS/freetdwr/PHL_TR0_201910091007.png','radar')




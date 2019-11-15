#include "qgstdwrprovider.h"

QgsTdwrProvider::QgsTdwrProvider() :
    QgsGdalProvider(QString(BaseUri), QgsDataProvider::ProviderOptions())
{

}

QgsTdwrProvider::QgsTdwrProvider( const QString &uri, const QgsDataProvider::ProviderOptions &providerOptions, bool update, GDALDatasetH newDataset) :
    QgsGdalProvider(uri, providerOptions, update, newDataset)
{

}

QgsTdwrProvider::~QgsTdwrProvider()
{

}

QgsTdwrProvider *QgsTdwrProvider::clone() const
{
  return new QgsTdwrProvider;
}

QString QgsTdwrProvider::name() const
{
  return QString(ProviderKey);
}

QString QgsTdwrProvider::providerKey()
{
  return QString(ProviderKey);
};

QString QgsTdwrProvider::description() const
{
  return QString(ProviderDescription);
}

QgsTdwrProvider::Metadata::Metadata() :
    QgsProviderMetadata( QString(ProviderKey), QString(ProviderDescription) )
{
}

QVariantMap QgsTdwrProvider::Metadata::decodeUri( const QString &uri )
{
    return _gdalMetadata.decodeUri(uri);
}
QgsTdwrProvider *QgsTdwrProvider::Metadata::createProvider( const QString &uri, const QgsDataProvider::ProviderOptions &options )
{
    return new QgsTdwrProvider(uri, options);
}

QgsGdalProvider *QgsTdwrProvider::Metadata::createRasterDataProvider(
  const QString &uri,
  const QString &format,
  int nBands,
  Qgis::DataType type,
  int width,
  int height,
  double *geoTransform,
  const QgsCoordinateReferenceSystem &crs,
  const QStringList &createOptions )
{
    return _gdalMetadata.createRasterDataProvider(uri, format, nBands, type, width, height, geoTransform, crs, createOptions);
}
QString QgsTdwrProvider::Metadata::filters( FilterType type )
{
    return _gdalMetadata.filters(type);
}
QList< QgsDataItemProvider * > QgsTdwrProvider::Metadata::dataItemProviders() const
{
    return _gdalMetadata.dataItemProviders();
}

#ifndef QGSTDWRPROVIDER_H
#define QGSTDWRPROVIDER_H

#include "qgsgdalprovider.h"

class QgsTdwrProvider : public QgsGdalProvider
{
    Q_OBJECT

    static constexpr const char *BaseUri = "http://mesonet.agron.iastate.edu/archive/data/";
    // http://mesonet.agron.iastate.edu/archive/data/2019/10/27/GIS/ridge/PHL/TR0/PHL_TR0_201910271426.png
    static constexpr const char *ProviderKey = "tdwr";
    static constexpr const char *ProviderDescription = "TDWR Data Provider";
    static QgsCoordinateReferenceSystem makeCrs() {
        return QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem::EpsgCrsId);
    }

public:
    class Metadata : public QgsProviderMetadata
    {
    public:
        Metadata();
        QVariantMap decodeUri( const QString &uri ) override;
        QgsTdwrProvider *createProvider( const QString &uri, const QgsDataProvider::ProviderOptions &options ) override;
        QgsGdalProvider *createRasterDataProvider(
          const QString &uri,
          const QString &format,
          int nBands,
          Qgis::DataType type,
          int width,
          int height,
          double *geoTransform,
          const QgsCoordinateReferenceSystem &crs,
          const QStringList &createOptions ) override;
        QString filters( FilterType type ) override;
        QList< QgsDataItemProvider * > dataItemProviders() const override;
    private:
        QgsGdalProviderMetadata _gdalMetadata;
    };

    QgsTdwrProvider();
    QgsTdwrProvider( const QString &uri, const QgsDataProvider::ProviderOptions &providerOptions, bool update = false, GDALDatasetH newDataset = nullptr );
    virtual ~QgsTdwrProvider() override;

    /**
     * Clone the provider.
     *
     * The underlying GDAL dataset is shared among the main provider and its
     * clones.
     */
    QgsTdwrProvider *clone() const override;

    QString name() const override;

    /**
     * GDAL data provider key
     * \since QGIS 3.10
     */
    static QString providerKey();
    QString description() const override;

};

#endif // QGSTDWRPROVIDER_H

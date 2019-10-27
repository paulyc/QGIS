# -*- coding: utf-8 -*-
"""QGIS Unit tests for Postgres QgsAbastractProviderConnection API.

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

"""
__author__ = 'Alessandro Pasotti'
__date__ = '10/08/2019'
__copyright__ = 'Copyright 2019, The QGIS Project'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
from test_qgsproviderconnection_base import TestPyQgsProviderConnectionBase
from qgis.core import (
    QgsWkbTypes,
    QgsAbstractDatabaseProviderConnection,
    QgsProviderConnectionException,
    QgsVectorLayer,
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsRasterLayer,
)
from qgis.testing import unittest
from osgeo import gdal


class TestPyQgsProviderConnectionPostgres(unittest.TestCase, TestPyQgsProviderConnectionBase):

    # Provider test cases must define the string URI for the test
    uri = ''
    # Provider test cases must define the provider name (e.g. "postgres" or "ogr")
    providerKey = 'postgres'

    @classmethod
    def setUpClass(cls):
        """Run before all tests"""
        TestPyQgsProviderConnectionBase.setUpClass()
        cls.postgres_conn = 'dbname=\'qgis_test\''
        if 'QGIS_PGTEST_DB' in os.environ:
            cls.postgres_conn = os.environ['QGIS_PGTEST_DB']
        # Create test layers
        vl = QgsVectorLayer(cls.postgres_conn + ' sslmode=disable key=\'"key1","key2"\' srid=4326 type=POINT table="qgis_test"."someData" (geom) sql=', 'test', 'postgres')
        assert vl.isValid()
        cls.uri = cls.postgres_conn + ' port=5432 sslmode=disable '

    def test_postgis_connections(self):
        """Create some connections and retrieve them"""

        md = QgsProviderRegistry.instance().providerMetadata('postgres')

        conn = md.createConnection(self.uri, {})
        md.saveConnection(conn, 'qgis_test1')

        # Retrieve capabilities
        capabilities = conn.capabilities()
        self.assertTrue(bool(capabilities & QgsAbstractDatabaseProviderConnection.Tables))
        self.assertTrue(bool(capabilities & QgsAbstractDatabaseProviderConnection.Schemas))
        self.assertTrue(bool(capabilities & QgsAbstractDatabaseProviderConnection.CreateVectorTable))
        self.assertTrue(bool(capabilities & QgsAbstractDatabaseProviderConnection.DropVectorTable))
        self.assertTrue(bool(capabilities & QgsAbstractDatabaseProviderConnection.RenameVectorTable))
        self.assertTrue(bool(capabilities & QgsAbstractDatabaseProviderConnection.RenameRasterTable))

        # Check filters and special cases
        table_names = self._table_names(conn.tables('qgis_test', QgsAbstractDatabaseProviderConnection.Raster))
        self.assertTrue('Raster1' in table_names)
        self.assertFalse('geometryless_table' in table_names)
        self.assertFalse('geometries_table' in table_names)
        self.assertFalse('geometries_view' in table_names)

        table_names = self._table_names(conn.tables('qgis_test', QgsAbstractDatabaseProviderConnection.View))
        self.assertFalse('Raster1' in table_names)
        self.assertFalse('geometryless_table' in table_names)
        self.assertFalse('geometries_table' in table_names)
        self.assertTrue('geometries_view' in table_names)

        table_names = self._table_names(conn.tables('qgis_test', QgsAbstractDatabaseProviderConnection.Aspatial))
        self.assertFalse('Raster1' in table_names)
        self.assertTrue('geometryless_table' in table_names)
        self.assertFalse('geometries_table' in table_names)
        self.assertFalse('geometries_view' in table_names)

        geometries_table = self._table_by_name(conn.tables('qgis_test'), 'geometries_table')
        srids_and_types = [[t.crs.postgisSrid(), t.wkbType]
                           for t in geometries_table.geometryColumnTypes()]
        srids_and_types.sort()
        self.assertEqual(srids_and_types,
                         [[0, 1], [0, 2], [0, 3], [0, 7], [3857, 1], [4326, 1]])

    # error: ERROR: relation "qgis_test.raster1" does not exist
    @unittest.skipIf(gdal.VersionInfo() < '2040000', 'This test requires GDAL >= 2.4.0')
    def test_postgis_raster_rename(self):
        """Test raster rename"""

        md = QgsProviderRegistry.instance().providerMetadata('postgres')

        conn = md.createConnection(self.uri, {})
        md.saveConnection(conn, 'qgis_test1')

        table = self._table_by_name(conn.tables('qgis_test', QgsAbstractDatabaseProviderConnection.Raster), 'Raster1')
        self.assertTrue(QgsRasterLayer("PG: %s schema='qgis_test' column='%s' table='%s'" % (conn.uri(), table.geometryColumn(), table.tableName()), 'r1', 'gdal').isValid())
        conn.renameRasterTable('qgis_test', table.tableName(), 'Raster2')
        table = self._table_by_name(conn.tables('qgis_test', QgsAbstractDatabaseProviderConnection.Raster), 'Raster2')
        self.assertTrue(QgsRasterLayer("PG: %s schema='qgis_test' column='%s' table='%s'" % (conn.uri(), table.geometryColumn(), table.tableName()), 'r1', 'gdal').isValid())
        table_names = self._table_names(conn.tables('qgis_test', QgsAbstractDatabaseProviderConnection.Raster))
        self.assertFalse('Raster1' in table_names)
        self.assertTrue('Raster2' in table_names)
        conn.renameRasterTable('qgis_test', table.tableName(), 'Raster1')
        table_names = self._table_names(conn.tables('qgis_test', QgsAbstractDatabaseProviderConnection.Raster))
        self.assertFalse('Raster2' in table_names)
        self.assertTrue('Raster1' in table_names)


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ConcavemanQGIS
                                 A QGIS plugin
 Makes concave hull for points
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-04-17
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Alex Lipovka
        email                : alex.lipovka@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsLayerTreeGroup, QgsLayerTreeLayer
from qgis.core import *
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .concaveman_qgis_dialog import ConcavemanQGISDialog
import os.path

from shapely.geometry import Polygon, mapping
from .concaveman import concaveman2d, initFFI, unloadFFI
import numpy as np
from scipy.spatial import ConvexHull


class ConcavemanQGIS:
    """QGIS Plugin Implementation."""
    vector_list = []
    vector_layers = []
    layer_name = ''

    concavity = 1.8
    lenThreshold = 0.001

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ConcavemanQGIS_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Concaveman QGIS')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ConcavemanQGIS', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/concaveman_qgis/img/logo.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Concaveman'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    
    
    def get_group_layers(self, group, layersArray):
        # print('- group: ' + group.name())   
        for child in group.children():
            if isinstance(child, QgsLayerTreeGroup):
                # Recursive call to get nested groups
                self.get_group_layers(child, layersArray)
            else:
                layersArray.append(child.layer().type() + ' ' + child.name())
                # print('  - layer: ' + child.name())

    def loadVectors(self):
        # Получаем список всех слоев в проекте
        self.dlg.cbVectors.clear()        
        layers = QgsProject.instance().mapLayers().values()
        # Отфильтровываем только векторные слои
        vector_layers = [layer for layer in layers if layer.type() == QgsMapLayerType.VectorLayer]
        # Выводим названия векторных слоев
        for layer in vector_layers:
            # Получаем тип геометрии слоя
            geometry_type = layer.geometryType()
            # Определяем тип геометрии по константе QgsWkbTypes
            if geometry_type == QgsWkbTypes.PointGeometry:
                addToList = True
                for layeradded in self.vector_layers:
                    if layeradded.id() == layer.id() :
                        addToList = False
                if addToList :
                    self.vector_list.append(f'Points: {layer.name()}')            
                    self.vector_layers.append(layer)
                    self.layer_name = layer.name()
        self.dlg.cbVectors.addItems(self.vector_list)

    def getPoints(self, index):
        point_list = []
    
        for feature in self.vector_layers[index].getFeatures():
            geometry = feature.geometry().asPoint()
            point_list.append([geometry.x(), geometry.y()])
        return point_list

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Concaveman QGIS'),
                action)
            self.iface.removeToolBarIcon(action)

    def makeConcaveHull(self, points_list):
        pts = np.array(points_list)
        h = ConvexHull(pts)
        cc = concaveman2d(pts, h.vertices, self.concavity, self.lenThreshold)
        hull = Polygon(cc)
        return(hull)
    
    def makeHullLayer(self, hull):
        layer = QgsVectorLayer('Polygon', f'{self.layer_name} — Concave Hull', 'memory')

        field1 = QgsField('id', QVariant.Int)
        field2 = QgsField('name', QVariant.String)
        layer.addAttribute(field1)
        layer.addAttribute(field2)

        # Создаем объект для добавления функций в слой
        pr = layer.dataProvider()

        # Создаем объекты функций и добавляем их в слой
        feature1 = QgsFeature()
        feature1.setGeometry(QgsGeometry.fromWkt(hull.wkt))
        feature1.setAttributes([1, 'Polygon 1'])
        pr.addFeatures([feature1])

        # Добавляем слой на карту
        QgsProject.instance().addMapLayer(layer)

    def run(self):
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ConcavemanQGISDialog()

        initFFI()
        self.loadVectors()
        self.dlg.dsbConcavity.setValue(self.concavity)
        self.dlg.dsbLenThres.setValue(self.lenThreshold)

        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            points = self.getPoints(self.dlg.cbVectors.currentIndex())
            self.concavity = self.dlg.dsbConcavity.value()
            self.lenThreshold = self.dlg.dsbLenThres.value()
            hull = self.makeConcaveHull(points)
            self.makeHullLayer(hull)
            pass
        unloadFFI()

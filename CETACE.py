# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import object
from qgis.PyQt.QtCore import QSettings, QTranslator, Qt, QCoreApplication
from qgis.PyQt.QtWidgets import QToolButton, QAction, QMenu
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject, QgsVectorLayer, edit, QgsFeature, QgsGeometry
from .CETACE_tool import CETACE_tool
from .CETACE_poly import CETACE_poly
import os
# Initialize Qt resources from file resources.py

import os.path

class CETACE(object):
    """QGIS Plugin Implementation."""
    
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
            'CETACE_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

        self.actions = []
        self.menu = self.tr(u"Créateur d'Espaces de Travail À Caractère Éphémère")
        self.toolbar = self.iface.addToolBar(u'CETACE')
        self.toolbar.setObjectName(u"Créateur d'Espaces de Travail À Caractère Éphémère")
        self.actionList = []
        self.nom_zone = self.get_name()
        self.couche_zone = None
        self.get_layer()
        self.geoms = []
        self.temp = []

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SHREK', message)

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
            # Adds plugin icon to Plugins own toolbar
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def get_name(self):
        temp = []
        filename = (os.path.dirname(os.path.realpath(__file__)) + "\\nom_couche.txt")
        if os.path.isfile(filename):
            f = open(filename)
            for line in f:
                temp.append(line)
            f.close()
            return temp[0].replace("\n", "")
        else:
            return "zone_plugin_CETACE"
    
    def creerBouton(self, parent, text):
        button = QToolButton(parent)
        button.setObjectName(text)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button.setPopupMode(QToolButton.DelayedPopup)
        parent.addWidget(button)
        return button

    def creerAction(self, icon_path, text, callback, checkable=True):
        action = QAction(
            QIcon(icon_path),
            text,
            self.iface.mainWindow())
        # connect the action to the run method
        action.setCheckable(checkable)
        if checkable:
            action.toggled.connect(callback)
        else:
            action.triggered.connect(callback)
        self.iface.registerMainWindowAction(action, '')
        self.actionList.append(action)
        return action
 
    def initGui(self):
        # Create action that will start plugin configuration
        self.actionCriarRectangle = self.creerAction(os.path.dirname(os.path.realpath(__file__)) + "\\rect.svg",
                                                      u"Créer zones récangulaires",
                                                      self.runRectangle)
        self.toolRectangle = CETACE_tool(self.iface.mapCanvas(), self.actionCriarRectangle, self, self.iface) 
        self.selectionButton = self.creerBouton(self.toolbar, u'Créer des rectangles')
        self.selectionButton.addAction(self.actionCriarRectangle)
        self.selectionButton.setDefaultAction(self.actionCriarRectangle)

        self.actionPoly = self.creerAction(os.path.dirname(os.path.realpath(__file__)) + "\\poly.svg",
                                                      u"Créer zones polygonales",
                                                      self.runPoly)
        self.toolPoly = CETACE_poly(self.iface.mapCanvas(), self.actionPoly, self, self.iface) 
        self.polyBouton = self.creerBouton(self.toolbar, u'Créer des polygones')
        self.polyBouton.addAction(self.actionPoly)
        self.polyBouton.setDefaultAction(self.actionPoly)

        self.actionback = self.add_action(os.path.dirname(os.path.realpath(__file__)) + "\\icon_back.png",
                                            text=self.tr(u'Retour en arrière'),
                                            callback=self.back,
                                            parent=self.iface.mainWindow())
    
        self.actionfoward = self.add_action(os.path.dirname(os.path.realpath(__file__)) + "\\icon_forward.png",
                                    text=self.tr(u'Rétablir'),
                                    callback=self.forward,
                                    parent=self.iface.mainWindow())

        self.menuIGN = self.iface.mainWindow().findChild(QMenu, "IGN")
        menuBar = self.iface.mainWindow().menuBar()
        if self.menuIGN:
            self.menuIGN.setSeparatorsCollapsible(True)
            self.menuIGN.addSeparator()
            self.menuIGN.addAction(self.actionCriarRectangle)
            self.menuIGN.addAction(self.actionPoly)
            self.menuIGN.addAction(self.actionback)
            self.menuIGN.addAction(self.actionfoward)
            self.menuIGN.setSeparatorsCollapsible(False)
        else:
            self.menuIGN = QMenu(self.iface.mainWindow())
            self.menuIGN.setObjectName("IGN")
            self.menuIGN.setTitle("IGN")
            self.menuIGN.setSeparatorsCollapsible(True)
            self.menuIGN.addSeparator()
            self.menuIGN.addAction(self.actionCriarRectangle)
            self.menuIGN.addAction(self.actionPoly)
            self.menuIGN.addAction(self.actionback)
            self.menuIGN.addAction(self.actionfoward)
            self.menuIGN.setSeparatorsCollapsible(False)
            menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menuIGN)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.mainWindow().removeToolBar(self.toolbar)
        for action in self.actionList:
            try:
                self.iface.unregisterMainWindowAction(action)
            except:
                pass
        self.toolRectangle.deactivate()
    
    def create_zone_layer(self):
        self.couche_zone = QgsVectorLayer("Polygon?crs=" + str(self.iface.activeLayer().crs()), self.nom_zone, "memory")
        self.provider = self.couche_zone.dataProvider()
        self.couche_zone.updateFields()
        single_symbol_renderer = self.couche_zone.renderer()
        symbol = single_symbol_renderer.symbol()
        QgsProject.instance().addMapLayer(self.couche_zone)
    
    def get_layer(self):
        allLayers = QgsProject.instance().mapLayers().values()
        for layers in allLayers:
            if layers.name() == self.nom_zone:
                self.couche_zone = layers
                return
            else:
                self.couche_zone = None
        
    def forward(self):
        if (self.couche_zone != None and self.temp == []):
            return
        with edit(self.couche_zone):
            ctrl = QgsFeature()
            ctrl.setGeometry(QgsGeometry.fromWkt(self.temp[0][0]))
            ctrl.setId(self.temp[0][1])
            self.temp.pop(0)
            self.geoms.insert(0, ctrl)
            self.couche_zone.dataProvider().addFeature(ctrl)
            self.couche_zone.updateExtents()

    def back(self):
        if (self.couche_zone != None and self.geoms != []):
            with edit(self.couche_zone):
                self.temp.insert(0, [self.geoms[0].geometry().asWkt(), self.geoms[0].id()])
                self.couche_zone.deleteFeature(self.geoms[0].id())
                self.geoms.pop(0)
                self.couche_zone.updateExtents()

    def runRectangle(self, b):
        if b:
            self.iface.mapCanvas().setMapTool(self.toolRectangle)
        else:
            self.iface.mapCanvas().unsetMapTool(self.toolRectangle)
            
    def runPoly(self, b):
        if b:
            self.iface.mapCanvas().setMapTool(self.toolPoly)
        else:
            self.iface.mapCanvas().unsetMapTool(self.toolPoly)
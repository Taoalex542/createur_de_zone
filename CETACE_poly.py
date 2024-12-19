from qgis.core import QgsPointXY, QgsWkbTypes, edit, QgsFeature, QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.PyQt.QtGui import QColor

class CETACE_poly(QgsMapTool):

    def __init__(self, canvas, action, main, iface):
        self.canvas = canvas
        self.active = False
        self.main = main
        self.iface = iface
        self.ctrl = False
        self.y = False
        self.z = False
        QgsMapTool.__init__(self, self.canvas)
        self.setAction(action)
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        mFillColor = QColor( 254, 178, 76, 63 );
        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)
        self.points = []
        self.reset()
    
    def reset(self):
        self.points = []
        self.isEmittingPoint = False
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
    
    def keyPressEvent(self, e):
        if e.key() == 16777249:
            self.ctrl = True
        if e.key() == 90:
            self.z = True
        if e.key() == 89:
            self.y = True
        if self.ctrl == True and self.z == True:
            self.main.back()
        if self.ctrl == True and self.y == True:
            self.main.forward()

    def keyReleaseEvent(self, e):
        if e.key() == 16777249:
            self.ctrl = False
        if e.key() == 90:
            self.z = False
        if e.key() == 89:
            self.y = False
    
    def canvasPressEvent(self, e):
        self.points.append(self.toMapCoordinates(e.pos()))
        self.isEmittingPoint = True
        self.showPoly()
    
    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        p = self.polygon()
        if p == None:
            return
        self.main.get_layer()
        if self.main.couche_zone == None:
            self.main.create_zone_layer()
        with edit(self.main.couche_zone):
            ctrl = QgsFeature()
            ctrl.setGeometry(QgsGeometry.fromPolygonXY(p))
            self.main.couche_zone.dataProvider().addFeature(ctrl)
            self.main.couche_zone.updateExtents()
            self.main.geoms.insert(0, ctrl)
        self.rubberBand.hide()
        self.points = []
        self.main.temp = []
    
    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.points.append(self.toMapCoordinates( e.pos() ))
        self.showPoly()
    
    def showPoly(self):
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        lenp = len(self.points)
        i = 0
        for point in self.points:
            i += 1
            if i == lenp:
                self.rubberBand.addPoint(QgsPointXY(point[0], point[1]), True)
            else:
                self.rubberBand.addPoint(QgsPointXY(point[0], point[1]), False)
    
        self.rubberBand.show()
    
    def polygon(self):
        if (len(self.points) <= 2):
            return None
        array = []
        for point in self.points:
            array.append(QgsPointXY(point[0], point[1]))
        return [array]
    
    def deactivate(self):
        self.rubberBand.reset()
        try:
            if self is not None:
                QgsMapTool.deactivate(self)
        except:
            pass
        
    def activate(self):
        QgsMapTool.activate(self)

    def unload(self):
        self.deactivate()
    

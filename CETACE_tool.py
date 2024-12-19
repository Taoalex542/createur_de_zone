from qgis.core import QgsPointXY, QgsRectangle, QgsWkbTypes, edit, QgsFeature, QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.PyQt.QtGui import QColor

class CETACE_tool(QgsMapTool):

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
        self.reset()
    
    def reset(self):
        self.startPoint = self.endPoint = None
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
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)
    
    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        r = self.rectangle()
        if r == None:
            return
        self.main.get_layer()
        if self.main.couche_zone == None:
            self.main.create_zone_layer()
        with edit(self.main.couche_zone):
            ctrl = QgsFeature()
            ctrl.setGeometry(QgsGeometry.fromRect(r))
            self.main.couche_zone.dataProvider().addFeature(ctrl)
            self.main.couche_zone.updateExtents()
            self.main.geoms.insert(0, ctrl)
        self.rubberBand.hide()
        self.main.temp = []
    
    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates( e.pos() )
        self.showRect(self.startPoint, self.endPoint)
    
    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return
        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(startPoint.x(), endPoint.y())
        point3 = QgsPointXY(endPoint.x(), endPoint.y())
        point4 = QgsPointXY(endPoint.x(), startPoint.y())
    
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)    # true to update canvas
        self.rubberBand.show()
    
    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None
    
        return QgsRectangle(self.startPoint, self.endPoint)
    
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
    

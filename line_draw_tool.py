from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.core import QgsWkbTypes, QgsGeometry, QgsPointXY
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsPointXY, QgsGeometry, QgsFeature, QgsField, QgsVectorLayer
from qgis.core import QgsPoint
from qgis.gui import QgsMapTool
from qgis.core import QgsRasterLayer


class LineDrawTool(QgsMapToolEmitPoint):
    lineDrawnSignal = pyqtSignal(QgsGeometry)
    def __init__(self, canvas, dtm_layer):
        self.canvas = canvas
        self.dtm_layer = dtm_layer
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.line_geometry = None

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showLine()

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        self.endPoint = self.toMapCoordinates(e.pos())
        self.showLine()

        if self.line_geometry:
            self.lineDrawnSignal.emit(self.line_geometry)

    def showLine(self):
        self.rubberBand.reset()  # Reset the rubber band
        
        if self.startPoint and self.endPoint:
            points = [QgsPoint(pt) for pt in [self.startPoint, self.endPoint]]

            self.line_geometry = QgsGeometry.fromPolyline(points)

            if isinstance(self.dtm_layer, QgsVectorLayer):
                # For vector layers, set the rubber band geometry to the line geometry
                self.rubberBand.setToGeometry(self.line_geometry, None)
            elif isinstance(self.dtm_layer, QgsRasterLayer):
                # For raster layers, set the rubber band geometry to the line geometry
                self.rubberBand.setToGeometry(self.line_geometry, None)


    def drawLineOnRaster(self):
        # Calculate the bounding box of the line
        bbox = self.line_geometry.boundingBox()
        x_min, y_min, x_max, y_max = bbox.xMinimum(), bbox.yMinimum(), bbox.xMaximum(), bbox.yMaximum()

        # Extract the raster data within the bounding box
        raster_data = self.extractRasterData(x_min, y_min, x_max, y_max)

        # Process the raster data as needed
        # You can draw the line on the raster or perform other operations here

    def extractRasterData(self, x_min, y_min, x_max, y_max):
        # Extract the raster data within the specified bounding box
        pass
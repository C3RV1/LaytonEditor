from PySide6 import QtCore, QtGui, QtWidgets
from formats.place import Place


class PlaceAbstractTableModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(PlaceAbstractTableModel, self).__init__(*args, **kwargs)
        self.place: Place = None

    def set_place(self, place: Place):
        self.layoutAboutToBeChanged.emit()
        self.place = place
        self.layoutChanged.emit()

# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import relativesRelationshipsParams as pms
from relativesRelationshipsTexts import trans_RR
import relativesRelationshipsTexts as texts_RR
from client.cltgui.cltguidialogs import GuiHistorique
from client.cltgui.cltguiwidgets import WExplication, WRadio


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        # should be removed if one-shot game

        wexplanation = WExplication(
            text=texts_RR.get_text_explanation(),
            size=(450, 80), parent=self)
        layout.addWidget(wexplanation)

        grid = QtGui.QGridLayout()
        layout.addLayout(grid)
        grid.addWidget(QtGui.QLabel(u"Mère"), 0, 0)
        grid.addWidget(QtGui.QLabel(u"Père"), 0, 1)

        rowcount = 1
        self._mother = {}
        self._father = {}
        options = (u"Pas du tout\nd'accord", u"Pas d'accord",
                   u"Ni en\ndésaccord ni\nd'accord", u"D'accord",
                   u"Tout à fait\nd'accord")
        for k, v in sorted(texts_RR.RR_items.viewitems()):
            grid.addWidget(QtGui.QLabel(v), rowcount, 0, rowcount, 1,
                           QtCore.Qt.AlignCenter)
            rowcount += 1
            wrm = WRadio(label="", texts=options, parent=self,
                         automatique=self._automatique)
            grid.addWidget(wrm, rowcount, 0)
            self._mother[k] = wrm
            wrf = WRadio(label="", texts=options, parent=self,
                         automatique=self._automatique)
            grid.addWidget(wrf, rowcount, 1)
            self._father[k] = wrf
            rowcount += 1

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_RR(u"Title"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass

        mother = {}
        for k, v in self._mother.viewitems():
            mother[k] = v.get_checkedbutton()
        father = {}
        for k, v in self._father.viewitems():
            father[k] = v.get_checkedbutton()

        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {}, {}".format(mother, father))
        self.accept()
        self._defered.callback(mother, father)

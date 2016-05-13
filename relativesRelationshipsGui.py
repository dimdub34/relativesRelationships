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
        options = (u"Pas du tout\nd'accord", u"Pas d'accord",
                   u"Ni en\ndésaccord ni\nd'accord", u"D'accord",
                   u"Tout à fait\nd'accord")
        self._reponses_widgets = {}

        layout = QtGui.QVBoxLayout(self)

        # Explanation
        wexplanation = WExplication(
            text=texts_RR.get_text_explanation(),
            size=(450, 80), parent=self)
        layout.addWidget(wexplanation)

        # stacked widget: 5 questions max in each widget
        self._stacked_wid = QtGui.QStackedWidget()
        layout.addWidget(self._stacked_wid)

        for i in range(1, len(texts_RR.RR_items)+1, 5):
            wid = QtGui.QWidget()
            self._stacked_wid.addWidget(wid)
            grid = QtGui.QGridLayout()
            grid.setHorizontalSpacing(100)
            wid.setLayout(grid)
            grid.addWidget(QtGui.QLabel(u"<strong>Mère</strong>"), 0, 0)
            grid.addWidget(QtGui.QLabel(u"<strong>Père</strong>"), 0, 1)

            rowcount = 1
            questions = [(k, v) for k, v in sorted(texts_RR.RR_items.viewitems())
                     if i <= k < i+5]
            for quest in questions:
                grid.addWidget(QtGui.QLabel(
                    u"<strong>" + quest[1] + u"<strong>"), rowcount, 0, 1, 2,
                               QtCore.Qt.AlignCenter)
                rowcount += 1
                wrm = WRadio(label="", texts=options, parent=self,
                             automatique=self._automatique)
                grid.addWidget(wrm, rowcount, 0)
                wrf = WRadio(label="", texts=options, parent=self,
                             automatique=self._automatique)
                grid.addWidget(wrf, rowcount, 1)
                self._reponses_widgets[quest[0]] = (wrm, wrf)
                rowcount += 1

        # Back, Next and Ok buttons
        self._pushbutton_back = QtGui.QPushButton(u"<< " + trans_RR(u"Back"))
        self._pushbutton_back.clicked.connect(self._change_index)
        self._label_current = QtGui.QLabel(
            trans_RR(u"Page 1 of") + u" {}".format(self._stacked_wid.count()))
        self._pushbutton_next = QtGui.QPushButton(trans_RR(u"Next") + u" >>")
        self._pushbutton_next.clicked.connect(self._change_index)
        self._pushbutton_ok = QtGui.QPushButton(u"Ok")
        self._pushbutton_ok.clicked.connect(self._accept)
        buttons_layout = QtGui.QHBoxLayout()
        buttons_layout.addSpacerItem(
            QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding))
        buttons_layout.addWidget(self._pushbutton_back)
        buttons_layout.addWidget(self._label_current)
        buttons_layout.addWidget(self._pushbutton_next)
        buttons_layout.addWidget(self._pushbutton_ok)
        layout.addLayout(buttons_layout)

        self.setWindowTitle(trans_RR(u"Questionnaire"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(self._pushbutton_ok.click)
            self._timer_automatique.start(7000)

    def _change_index(self):
        ci = self._stacked_wid.currentIndex()
        if self.sender() == self._pushbutton_back:
            ci -= 1
        elif self.sender() == self._pushbutton_next:
            ci += 1
        self._stacked_wid.setCurrentIndex(ci)
        if 0 <= ci < self._stacked_wid.count():
            self._label_current.setText(u"Page {} sur {}".format(
                ci+1, self._stacked_wid.count()))
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass

        try:
            reponses = {}
            for k, v in self._reponses_widgets.viewitems():
                reponses[k] = (v[0].get_checkedbutton(),
                                      v[1].get_checkedbutton())
        except ValueError:
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                trans_RR(u"You must answer to all the questions"))
            return

        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choices?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {}".format(reponses))
        self.accept()
        self._defered.callback(reponses)

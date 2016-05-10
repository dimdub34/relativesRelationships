# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
import relativesRelationshipsParams as pms


logger = logging.getLogger("le2m")


class PartieRR(Partie):
    __tablename__ = "partie_relativesRelationships"
    __mapper_args__ = {'polymorphic_identity': 'relativesRelationships'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsRR')

    def __init__(self, le2mserv, joueur):
        super(PartieRR, self).__init__(
            nom="relativesRelationships", nom_court="RR",
            joueur=joueur, le2mserv=le2mserv)
        self.RR_gain_ecus = 0
        self.RR_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param periode:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsRR(period)
        self.le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        inputs = yield(self.remote.callRemote("display_decision"))
        self.currentperiod.RR_decisiontime = (datetime.now() - debut).seconds
        for k, v in inputs.viewitems():
            setattr(self.currentperiod, "RR_{}_moth".format(k), v[0])
            setattr(self.currentperiod, "RR_{}_fath".format(k), v[1])
        logger.info(u"{}: {}".format(self.joueur, inputs))
        self.joueur.info(u"Ok")
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.RR_periodpayoff = 0

        # cumulative payoff since the first period
        if self.currentperiod.RR_period < 2:
            self.currentperiod.RR_cumulativepayoff = \
                self.currentperiod.RR_periodpayoff
        else: 
            previousperiod = self.periods[self.currentperiod.RR_period - 1]
            self.currentperiod.RR_cumulativepayoff = \
                previousperiod.RR_cumulativepayoff + \
                self.currentperiod.RR_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.RR_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.RR_periodpayoff))

    # @defer.inlineCallbacks
    # def display_summary(self, *args):
    #     """
    #     Send a dictionary with the period content values to the remote.
    #     The remote creates the text and the history
    #     :param args:
    #     :return:
    #     """
    #     logger.debug(u"{} Summary".format(self.joueur))
    #     yield(self.remote.callRemote(
    #         "display_summary", self.currentperiod.todict()))
    #     self.joueur.info("Ok")
    #     self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        """
        Compute the payoff for the part and set it on the remote.
        The remote stores it and creates the corresponding text for display
        (if asked)
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))

        self.RR_gain_ecus = self.currentperiod.RR_cumulativepayoff
        self.RR_gain_euros = float(self.RR_gain_ecus) * float(pms.TAUX_CONVERSION)
        yield (self.remote.callRemote(
            "set_payoffs", self.RR_gain_euros, self.RR_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.RR_gain_ecus, self.RR_gain_euros))


class RepetitionsRR(Base):
    __tablename__ = 'partie_relativesRelationships_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_relativesRelationships.partie_id"))

    RR_period = Column(Integer)
    RR_treatment = Column(Integer)
    # RR_group = Column(Integer)
    # RR_decision = Column(Integer)
    RR_1_moth = Column(Integer)
    RR_2_moth = Column(Integer)
    RR_3_moth = Column(Integer)
    RR_4_moth = Column(Integer)
    RR_5_moth = Column(Integer)
    RR_6_moth = Column(Integer)
    RR_7_moth = Column(Integer)
    RR_8_moth = Column(Integer)
    RR_9_moth = Column(Integer)
    RR_10_moth = Column(Integer)
    RR_11_moth = Column(Integer)
    RR_12_moth = Column(Integer)
    RR_13_moth = Column(Integer)
    RR_14_moth = Column(Integer)
    RR_15_moth = Column(Integer)
    RR_16_moth = Column(Integer)
    RR_17_moth = Column(Integer)
    RR_18_moth = Column(Integer)
    RR_19_moth = Column(Integer)
    RR_20_moth = Column(Integer)
    RR_21_moth = Column(Integer)
    RR_22_moth = Column(Integer)
    RR_23_moth = Column(Integer)
    RR_24_moth = Column(Integer)
    RR_25_moth = Column(Integer)
    RR_26_moth = Column(Integer)
    RR_27_moth = Column(Integer)
    RR_28_moth = Column(Integer)
    RR_29_moth = Column(Integer)
    RR_30_moth = Column(Integer)
    RR_1_fath = Column(Integer)
    RR_2_fath = Column(Integer)
    RR_3_fath = Column(Integer)
    RR_4_fath = Column(Integer)
    RR_5_fath = Column(Integer)
    RR_6_fath = Column(Integer)
    RR_7_fath = Column(Integer)
    RR_8_fath = Column(Integer)
    RR_9_fath = Column(Integer)
    RR_10_fath = Column(Integer)
    RR_11_fath = Column(Integer)
    RR_12_fath = Column(Integer)
    RR_13_fath = Column(Integer)
    RR_14_fath = Column(Integer)
    RR_15_fath = Column(Integer)
    RR_16_fath = Column(Integer)
    RR_17_fath = Column(Integer)
    RR_18_fath = Column(Integer)
    RR_19_fath = Column(Integer)
    RR_20_fath = Column(Integer)
    RR_21_fath = Column(Integer)
    RR_22_fath = Column(Integer)
    RR_23_fath = Column(Integer)
    RR_24_fath = Column(Integer)
    RR_25_fath = Column(Integer)
    RR_26_fath = Column(Integer)
    RR_27_fath = Column(Integer)
    RR_28_fath = Column(Integer)
    RR_29_fath = Column(Integer)
    RR_30_fath = Column(Integer)
    RR_decisiontime = Column(Integer)
    RR_periodpayoff = Column(Float)
    RR_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.RR_treatment = pms.TREATMENT
        self.RR_period = period
        self.RR_decisiontime = 0
        self.RR_periodpayoff = 0
        self.RR_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp


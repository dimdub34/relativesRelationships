# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from twisted.spread import pb
from client.cltremote import IRemote
from client.cltgui.cltguidialogs import GuiRecapitulatif
import relativesRelationshipsParams as pms
from relativesRelationshipsGui import GuiDecision
import relativesRelationshipsTexts as texts_RR


logger = logging.getLogger("le2m")


class RemoteRR(IRemote):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        # self._histo_vars = [
        #     "RR_period", "RR_decision",
        #     "RR_periodpayoff", "RR_cumulativepayoff"]
        # self._histo.append(texts_RR.get_histo_head())

    def remote_configure(self, params):
        """
        Set the same parameters as in the server side
        :param params:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        """
        Set the current period and delete the history
        :param period: the current period
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period
        # if self.currentperiod == 1:
        #     del self.histo[1:]

    def remote_display_decision(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            inputs = {}
            for k in texts_RR.RR_items.viewkeys():
                inputs[k] = (random.randint(0, 4), random.randint(0, 4))
            # decision = \
            #     random.randrange(
            #         pms.DECISION_MIN,
            #         pms.DECISION_MAX + pms.DECISION_STEP,
            #         pms.DECISION_STEP)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, inputs))
            return inputs
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            ecran_decision.show()
            return defered

    # def remote_display_summary(self, period_content):
    #     """
    #     Display the summary screen
    #     :param period_content: dictionary with the content of the current period
    #     :return: deferred
    #     """
    #     logger.info(u"{} Summary".format(self._le2mclt.uid))
    #     self.histo.append([period_content.get(k) for k in self._histo_vars])
    #     if self._le2mclt.simulation:
    #         return 1
    #     else:
    #         defered = defer.Deferred()
    #         ecran_recap = GuiRecapitulatif(
    #             defered, self._le2mclt.automatique, self._le2mclt.screen,
    #             self.currentperiod, self.histo,
    #             texts_RR.get_text_summary(period_content))
    #         ecran_recap.show()
    #         return defered

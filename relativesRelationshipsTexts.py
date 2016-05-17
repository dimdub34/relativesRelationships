# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import relativesRelationshipsParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
localedir = os.path.join(params.getp("PARTSDIR"), "relativesRelationships", "locale")
try:
    trans_RR = gettext.translation(
      "relativesRelationships", localedir, languages=[params.getp("LANG")]).ugettext
except IOError:
    logger.critical(u"Translation file not found")
    trans_RR = lambda x: x  # if there is an error, no translation


def get_text_explanation():
    return trans_RR(u"Pour chacun des 30 énoncés (répartis sur 6 pages), "
                    u"veuillez cliquer sur le numéro de l'échelle "
                    u"(de 1=pas du tout d'accord à 5=tout à fait d'accord) "
                    u"qui décrit le mieux la façon dont l'énoncé s'applique "
                    u"à vous et votre mère (à gauche), à vous et à votre père "
                    u"(à droite) durant les années où vous avez grandi à la "
                    u"maison. Il n'y a pas de bonne ou de mauvaise réponse. "
                    u"Ne prenez pas trop de temps pour chaque énoncé, nous "
                    u"avons besoin de votre impression générale.")

RR_items = {
1: u"Durant mon enfance, ma mère/mon père pensait que les enfants devaient "
   u"avoir leur mot à dire autant que les parents.",
2: u"Même si les enfants étaient en désaccord avec elle/lui, ma mère/mon père "
   u"pensait que c’était dans notre intérêt d’être obligés de nous conformer "
   u"à ce qu’elle/il pensait être bien.",
3: u"Chaque fois qu'elle/il me disait de faire quelque chose, elle/il "
   u"attendait de moi que je le fasse immédiatement sans poser de questions.",
4: u"Ma mère/Mon père discutait avec les enfants des raisons qui motivaient "
   u"les règlements familiaux, une fois qu'ils étaient établis.",
5: u"Ma mère/Mon père favorisait les concessions mutuelles quand je trouvais "
   u"que les règlements familiaux n’étaient pas appropriés.",
6: u"Ma mère/Mon père pensait que les enfants devaient être libres de se faire "
   u"leur propre idée et de décider de ce qu'ils voulaient faire, même si les "
   u"parents étaient en désaccord.",
7: u"Ma mère/Mon père refusait que je remette en question les décisions "
   u"qu'elle/il prenait.",
8: u"Ma mère/Mon père dirigeait les activités et les décisions des enfants "
   u"de la famille au moyen de la raison et de la discipline.",
9: u"Ma mère/Mon père croyait que les parents devraient recourir davantage "
   u"à la force pour inciter les enfants à se comporter comme ils le devraient.",
10: u"Ma mère/Mon père ne pensait pas que je doive obéir aux règles de "
    u"comportement simplement parce que quelqu’un en position d’autorité "
    u"les avait établies.",
11: u"Je savais ce qu’elle/il attendait de moi dans la famille, mais je me "
    u"sentais aussi libre de discuter de ces attentes avec elle/lui lorsque "
    u"je les trouvais déraisonnables.",
12: u"Ma mère/Mon père pensait que les parents avisés devaient enseigner tôt à "
    u"leurs enfants qui était le patron dans la famille.",
13: u"Ma mère/Mon père était discrète/discret sur ses attentes concernant mon "
    u"comportement.",
14: u"Ma mère/Mon père faisait, la plupart du temps, ce que les enfants "
    u"voulaient quant aux décisions familiales.",
15: u"Ma mère/Mon père nous donnait régulièrement des directives et nous "
    u"guidait de manière rationnelle et objective.",
16: u"Ma mère/Mon père était vraiment contrarié(e) si je n’étais pas d'accord "
    u"avec elle/lui.",
17: u"Ma mère/Mon père pensait que la plupart des problèmes dans la société "
    u"se règleraient si les parents laissaient les enfants réaliser leurs "
    u"activités, leurs décisions et leurs désirs.",
18: u"Ma mère/Mon père me faisait savoir quels étaient les comportements "
    u"attendus et si je ne répondais pas à ses attentes, elle/il me punissait.",
19: u"Ma mère/Mon père me laissait décider la plupart des choses qui me "
    u"concernaient sans donner beaucoup de directives.",
20: u"Ma mère/Mon père acceptait nos opinions, mais quand venait le temps "
    u"de prendre des décisions familiales, c'est elle/lui qui avait le "
    u"dernier mot.",
21: u"Ma mère/Mon père déclinait la responsabilité de diriger et de guider "
    u"mon comportement.",
22: u"Ce qu’elle/il attendait des comportements des enfants était clair, "
    u"mais elle/il était prêt(e) à les ajuster aux besoins de chacun.",
23: u"Ma mère/Mon père donnait des directives et attendait de moi que je les "
    u"suive, tout en étant disposé(e) à m'écouter et à en discuter avec moi.",
24: u"Ma mère/Mon père me permettait de me former ma propre opinion quant "
    u"aux affaires familiales et me laissait généralement décider moi-même "
    u"de ce que je voulais faire.",
25: u"Ma mère/Mon père pensait que les problèmes de la société seraient "
    u"résolus si les parents étaient plus stricts avec les enfants qui ne "
    u"font pas ce qu'il faut.",
26: u"Ma mère/Mon père me disait exactement ce qu'elle/il voulait que je "
    u"fasse et comment elle/il s'attendait à ce que je le fasse.",
27: u"Ma mère/Mon père me donnait des directives claires sur mon comportement "
    u"et mes activités, mais comprenait quand j’étais en désaccord avec "
    u"elle/lui.",
28: u"Ma mère/Mon père laissait les enfants libres de leurs comportements, "
    u"activités et désirs.",
29: u"Je savais ce qu’elle/il attendait de moi dans la famille et "
    u"elle/il insistait pour que je m’y conforme simplement par respect pour "
    u"son autorité.",
30: u"Si elle/il prenait une décision qui me blessait, elle/il était disposée "
    u"à discuter cette décision avec moi et à admettre son erreur si tel "
    u"est le cas."
}

# def get_histo_head():
#     return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
#              le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]
#
#
# def get_text_summary(period_content):
#     txt = trans_RR(u"Summary text")
#     return txt



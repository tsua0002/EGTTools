"""
API reference documentation for the `games` submodule.
"""

from egttools.numerical.games import AbstractGame, NormalFormGame, CRDGame, CRDGameTU, OneShotCRD

from .pgg import PGG
from .informal_risk import InformalRiskGame
from .abstract_games import AbstractNPlayerGame, AbstractTwoPLayerGame
from .nonlinear_games import NPlayerStagHunt, CommonPoolResourceDilemma

# Author: Erin Eckerman
# Date: 2/8/21
# Description:

from player import *
from piece import *

class Chessgame:

    def __init__(self, player_1_name, player_2_name):
        self._finished = False
        self._board = [[None for space in range(8)] for row in range(8)]
        self._players = [player_1_name, player_2_name]
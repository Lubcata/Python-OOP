from typing import List

from project.divers.base_diver import BaseDiver

from project.fish.base_fish import BaseFish


class NauticalCatchChallengeApp:
    def __init__(self):
        self.divers: List[BaseDiver] = []
        self.fish_list: List[BaseFish] = []



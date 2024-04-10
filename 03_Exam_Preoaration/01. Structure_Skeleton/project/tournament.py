from typing import List

from project.equipment.base_equipment import BaseEquipment
from project.equipment.elbow_pad import ElbowPad
from project.equipment.knee_pad import KneePad
from project.teams.base_team import BaseTeam
from project.teams.indoor_team import IndoorTeam
from project.teams.outdoor_team import OutdoorTeam


class Tournament:
    equipment_mapper = {
        "KneePad": KneePad,
        "ElbowPad": ElbowPad,
    }

    teams_mapper = {
        "OutdoorTeam": OutdoorTeam,
        "IndoorTeam": IndoorTeam,
    }

    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.equipment: List[BaseEquipment] = []
        self.teams: List[BaseTeam] = []

    def equpment_element(self, equeipment_type):
        equipment = [eq for eq in self.equipment if eq.TYPE_ == equeipment_type]
        return equipment[-1] if equipment else None

    def team_element(self, team_name):
        team = [t for t in self.teams if t.name == team_name]
        return team[0] if team else None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value.isalnum():
            raise ValueError("Tournament name should contain letters and digits only!")
        self.__name = value

    def add_equipment(self, equipment_type: str):
        if equipment_type not in self.equipment_mapper:
            # TODO Check Validation
            raise ValueError("Invalid equipment type!")
        equipment = self.equipment_mapper[equipment_type]()
        self.equipment.append(equipment)
        return f"{equipment_type} was successfully added."

    def add_team(self, team_type: str, team_name: str, country: str, advantage: int):
        if team_type not in self.teams_mapper:
            # TODO Check Validation
            raise ValueError("Invalid team type!")
        if len(self.teams) >= self.capacity:
            return "Not enough tournament capacity."

        team = self.teams_mapper[team_type](team_name, country, advantage)

        self.teams.append(team)
        return f"{team_type} was successfully added."

    def sell_equipment(self, equipment_type: str, team_name: str):
        equipment = self.equpment_element(equipment_type)
        team = self.team_element(team_name)
        if team.budget < equipment.price:
            raise Exception("Budget is not enough!")
        team.equipment.append(equipment)
        team.budget -= equipment.price
        self.equipment.remove(equipment)
        return f"Successfully sold {equipment_type} to {team_name}."

    def remove_team(self, team_name: str):
        team = self.team_element(team_name)

        if team is None:
            raise Exception("No such team!")
        if team.wins:
            raise Exception(f"The team has {team.wins} wins! Removal is impossible!")
        self.teams.remove(team)
        return f"Successfully removed {team_name}."

    def increase_equipment_price(self, equipment_type: str):
        equipment = [e.increase_price() for e in self.equipment if e.TYPE_ == equipment_type]

        return f"Successfully changed {len(equipment)}pcs of equipment."

    def play(self, team_name1: str, team_name2: str):
        team1 = self.team_element(team_name1)
        team2 = self.team_element(team_name2)

        if not team1.TYPE_ == team2.TYPE_:
            raise Exception("Game cannot start! Team types mismatch!")
        team1_points = team1.sum_points()
        team2_points = team2.sum_points()

        if team1_points > team2_points:
            team1.win()
            return f"The winner is {team1.name}."
        elif team2_points > team1_points:
            team2.win()
            return f"The winner is {team2.name}."
        else:
            return f"No winner in this game."

    def get_statistics(self):
        sorted_teams = sorted(self.teams, key=lambda t: -t.wins)

        result = (f"Tournament: {self.name}\n"
                  f"Number of Teams: {len(self.teams)}\n"
                  f"Teams:\n")
        result += "\n".join(t.get_statistics() for t in sorted_teams)
        return result

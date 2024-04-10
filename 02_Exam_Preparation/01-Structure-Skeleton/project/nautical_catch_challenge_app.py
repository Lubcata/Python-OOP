from typing import List

from project.divers.base_diver import BaseDiver

from project.fish.base_fish import BaseFish

from project.divers.free_diver import FreeDiver

from project.divers.scuba_diver import ScubaDiver

from project.fish.predatory_fish import PredatoryFish

from project.fish.deep_sea_fish import DeepSeaFish


class NauticalCatchChallengeApp:
    divers_mapper = {
        "FreeDiver": FreeDiver,
        "ScubaDiver": ScubaDiver,
    }

    fish_mapper = {
        "PredatoryFish": PredatoryFish,
        "DeepSeaFish": DeepSeaFish,
    }

    def __init__(self):
        self.divers: List[BaseDiver] = []
        self.fish_list: List[BaseFish] = []

    def dive_into_competition(self, diver_type: str, diver_name: str):
        if diver_type not in self.divers_mapper:
            return f"{diver_type} is not allowed in our competition."
        try:
            diver = next(filter(lambda d: d.name == diver_name, self.divers))
            return f"{diver_name} is already a participant."
        except StopIteration:
            new_diver = self.divers_mapper[diver_type](diver_name)
            self.divers.append(new_diver)
            return f"{diver_name} is successfully registered for the competition as a {diver_type}."

    def swim_into_competition(self, fish_type: str, fish_name: str, points: float):
        if fish_type not in self.fish_mapper:
            return f"{fish_type} is forbidden for chasing in our competition."

        try:
            fish = next(filter(lambda f: f.name == fish_name, self.fish_list))
            return f"{fish_name} is already permitted."
        except StopIteration:
            new_fish = self.fish_mapper[fish_type](fish_name, points)
            self.fish_list.append(new_fish)
            return f"{fish_name} is allowed for chasing as a {fish_type}."

    def chase_fish(self, diver_name: str, fish_name: str, is_lucky: bool):
        try:
            diver = next(filter(lambda d: d.name == diver_name, self.divers))
        except StopIteration:
            return f"{diver_name} is not registered for the competition."

        try:
            fish = next(filter(lambda f: f.name == fish_name, self.fish_list))
        except StopIteration:
            return f"The {fish_name} is not allowed to be caught in this competition."

        if diver.has_health_issue:
            return f"{diver_name} will not be allowed to dive, due to health issues."

        if diver.oxygen_level < fish.time_to_catch:
            diver.miss(fish.time_to_catch)
            message = f"{diver_name} missed a good {fish_name}."
        elif diver.oxygen_level == fish.time_to_catch:
            if is_lucky:
                diver.hit(fish)
                message = f"{diver_name} hits a {fish.points}pt. {fish_name}."
            else:
                diver.miss(fish.time_to_catch)
                message = f"{diver_name} missed a good {fish_name}."
        elif diver.oxygen_level > fish.time_to_catch:
            diver.hit(fish)
            message = f"{diver_name} hits a {fish.points}pt. {fish_name}."

        if diver.oxygen_level == 0:
            diver.update_health_status()
        return message

    def health_recovery(self):
        divers_with_health_issues = [d for d in self.divers if d.has_health_issue]

        for diver in divers_with_health_issues:
            diver.has_health_issue = False
            diver.renew_oxy()

        return f"Divers recovered: {len(divers_with_health_issues)}"

    def diver_catch_report(self, diver_name: str):
        diver = [d for d in self.divers if d.name == diver_name][0]

        message = f"**{diver_name} Catch Report**\n"
        fish_details = "\n".join([fish.fish_details() for fish in diver.catch])

        message += fish_details
        return message

    def competition_statistics(self):
        healthy_diver = [d for d in self.divers if not d.has_health_issue]
        sorted_divers = sorted(healthy_diver, key=lambda d: (-d.competition_points, len(d.catch), d.name))

        message = "**Nautical Catch Challenge Statistics**\n"
        divers_details = "\n".join(str(d) for d in sorted_divers)

        message += divers_details
        return message



from project.equipment.base_equipment import BaseEquipment


class ElbowPad(BaseEquipment):
    PROTECTION = 90
    PRICE = 25.0
    TYPE_ = "ElbowPad"

    def __init__(self):
        super().__init__(ElbowPad.PROTECTION, ElbowPad.PRICE)

    def increase_price(self):
        self.price *= 1.1
        # self.price += self.price * 0.10
# weapon.py

class Weapon:
    def __init__(self, name, damage, weapon_type):
        self.name = name
        self.damage = damage
        self.type = weapon_type  # ex: "heavy", "fast", "ranged"
        self.level = 1
        self.enchant = None

    def upgrade(self):
        self.level += 1
        self.damage += 2

    def enchant_weapon(self, effect):
        self.enchant = effect

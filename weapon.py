class Weapon:
    def __init__(self, name, damage, range, range_type, cooldown=30):
        self.name = name
        self.damage = damage
        self.range = range
        self.range_type = range_type
        self.cooldown = cooldown

import random

class Field:
    def __init__(self,name):
        self.__name = name

    def change_filed(self):
        fileds = ["Toxic Wasteland", "Healing Meadows", "Castle Walls"]
        new_filed = random.choice(fileds)
        self.__name = new_filed
         
    def fieldEffects(self, combatant1, combatant2):
        if self.field.name == "Toxic Wasteland":
            combatant1.take_damage(5)
            combatant2.take_damage(5)
            print("Toxic Wasteland: Both combatants take 5 damage!")
        elif self.field.name == "Healing Meadows":
            combatant1.health = combatant1.health + 5
            combatant2.health = combatant2.health + 5
            print("Healing Meadows: Both combatants heal 5 health!")
        else:
            print('Castle Walls: no effects.')
        
    def getName(self):
        print(f'Filed changed to:{self.__name}')

class Arena:
    def __init__(self, name):
        self.name = name
        self.combatants = []
        self.field = Field("Castle Walls")  # Default field
    
    def addCombatant(self, combatant):
        if combatant not in self.combatants:
            self.combatants.append(combatant)
        else:
            print(f"{combatant.name} is already in the arena.")
    
    def removeCombatant(self, combatant):
        if combatant in self.combatants:
            self.combatants.remove(combatant)
        else:
            print(f"{combatant.name} is not in the arena.")
    
    def listCombatants(self):
        for combatant in self.combatants:
            print(combatant.details())
    
    def restoreCombatants(self):
        for combatant in self.combatants:
            combatant.reset()
    
    def checkVaildCombatants(self,combatant):
        if combatant in self.combatants and combatant.health > 0:
            return True
        else:
            return False
    
    def duel(self, combatant1, combatant2):
        if combatant1 in self.combatants and combatant2 in self.combatants and combatant1.health > 0 and combatant2.health > 0:
            print(f"Duel between {combatant1.name} and {combatant2.name} starts!")
            for _ in range(10):
                self.field.change_field()
                self.fieldEffects(combatant1, combatant2)
                combatant1.attack(combatant2)
                combatant2.attack(combatant1)
                if combatant1.health <= 0 or combatant2.health <= 0:
                    break
            if combatant1.health <= 0 and combatant2.health <= 0:
                print(f"Double KO! Both {combatant1.name} and {combatant2.name} are knocked out!")
            elif combatant1.health <= 0:
                print(f"{combatant2.name} wins! {combatant1.name} is knocked out!")
            elif combatant2.health <= 0: 
                print(f"{combatant1.name} wins! {combatant2.name} is knocked out!")
        else:
            print("Invalid duel: Ensure both combatants are in the arena and have health.")


class Combatant:
    def __init__(self, name, max_health, strength, defence, magic, ranged):
        self.name = name  # Public attribute
        self.__max_health = max_health
        self.__health = max_health
        self.__strength = strength
        self.__defence = defence
        self.__magic = magic
        self.__ranged = ranged
    
    def attack(self, enemy):
        pass  # To be overridden by subclasses
    
    def take_damage(self, damage):
        self.__health -= damage
        if self.__health <= 0:
            self.__health = 0
            return True  # Combatant is knocked out
        return False
    
    def reset(self):
        self.__health = self.__max_health
    
    def details(self):
        return f"{self.name} ({self.__class__.__name__}): Health={self.__health}/{self.__max_health}, Strength={self.__strength}, Defence={self.__defence}, Magic={self.__magic}, Ranged={self.__ranged}"
    
    def calculate_power(self):
        # Example calculation of power based on attributes
        return self.__strength + self.__magic + self.__ranged
    
    def reset_values(self, max_health, strength, defence, magic, ranged):
        self.__max_health = max_health
        self.__health = max_health
        self.__strength = strength
        self.__defence = defence
        self.__magic = magic
        self.__ranged = ranged
    
    def set_health(self, health):
        self.__health = health
    
    # Getter methods for private attributes
    def get_max_health(self):
        return self.__max_health
    
    def get_health(self):
        return self.__health
    
    def get_strength(self):
        return self.__strength
    
    def get_defence(self):
        return self.__defence
    
    def get_magic(self):
        return self.__magic
    
    def get_ranged(self):
        return self.__ranged

class Ranger(Combatant):
    def __init__(self, name, max_health, strength, defence, arrows):
        super().__init__(name, max_health, strength, defence)
        self.arrows = arrows
    
    def attack(self, enemy):
        if self.arrows > 0:
            damage = self.strength
            self.arrows -= 1
        else:
            damage = self.strength // 2  # Half damage without arrows
        return enemy.take_damage(max(0, damage - enemy.defence))
    
    def reset(self):
        super().reset()
        self.arrows = 3
    
    def details(self):
        return super().details() + f", Arrows={self.arrows}"


class Warrior(Combatant):
    def __init__(self, name, max_health, strength, defence, armour_value):
        super().__init__(name, max_health, strength, defence)
        self.armour_value = armour_value
        self.current_armour = 10
    
    def attack(self, enemy):
        return enemy.take_damage(max(0, self.strength - enemy.defence))
    
    def take_damage(self, damage):
        if self.current_armour > 0:
            damage -= self.armour_value
            if damage < 0:
                damage = 0
            self.current_armour -= 5
            if self.current_armour <= 0:
                print(f"{self.name}'s armour is shattered!")
        return super().take_damage(damage)
    
    def reset(self):
        super().reset()
        self.current_armour = 10
    
    def details(self):
        return super().details() + f", Armour={self.current_armour}"


class Dharok(Warrior):
    def attack(self, enemy):
        # Dharok's attack increases with lower health
        bonus_damage = (self.max_health - self.health) // 2
        return enemy.take_damage(max(0, self.strength + bonus_damage - enemy.defence))


class Guthans(Warrior):
    def attack(self, enemy):
        # Guthans heals each time it attacks
        heal_amount = self.strength // 5
        self.health = min(self.max_health, self.health + heal_amount)
        return enemy.take_damage(max(0, self.strength - enemy.defence))


class Mage(Combatant):
    def __init__(self, name, max_health, strength, defence, mana, regen_rate):
        super().__init__(name, max_health, strength, defence)
        self.mana = mana
        self.regen_rate = regen_rate
    
    def cast_spell(self, spell_name):
        pass  # To be overridden by subclasses
    
    def reset(self):
        super().reset()
        self.mana = 50  # Assuming default mana for generic mage
        self.regen_rate = 12.5  # Assuming default regen rate for generic mage
    
    def details(self):
        return super().details() + f", Mana={self.mana}, RegenRate={self.regen_rate}"


class PyroMage(Mage):
    def __init__(self, name, max_health, strength, defence, mana, regen_rate):
        super().__init__(name, max_health, strength, defence, mana, regen_rate)
        self.flame_boost = 1
    
    def cast_spell(self, spell_name):
        if spell_name == "SuperHeat" and self.mana >= 40:
            self.flame_boost += 1
            self.mana -= 40
            self.mana += self.regen_rate
            return True
        elif spell_name == "FireBlast" and 10 <= self.mana < 40:
            self.mana -= 10
            return True
        return False
    
    def attack(self, enemy):
        damage = (self.strength * self.flame_boost)
        return enemy.take_damage(max(0, damage - enemy.defence))


class FrostMage(Mage):
    def __init__(self, name, max_health, strength, defence, mana, regen_rate):
        super().__init__(name, max_health, strength, defence, mana, regen_rate)
        self.ice_block = False
    
    def cast_spell(self, spell_name):
        if spell_name == "IceBlock" and self.mana >= 50:
            self.ice_block = True
            self.mana -= 50
            return True
        elif spell_name == "IceBarrage" and 10 <= self.mana < 50:
            self.mana -= 10
            return True
        return False
    
    def attack(self, enemy):
        if self.ice_block:
            self.ice_block = False
            return 0  # Ice block absorbs damage
        damage = (self.strength // 4)
        return enemy.take_damage(max(0, damage - enemy.defence))


class Karil(Warrior):
    def attack(self, enemy):
        damage = self.strength + self.range_level
        return enemy.take_damage(max(0, damage - enemy.defence))


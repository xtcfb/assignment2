import random

# Combatant base class
class Combatant:
    def __init__(self, name, maxHealth, strength, defence):
        self.name = name
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.strength = strength
        self.defence = defence
    
    def attack(self, enemy):
        pass  # To be implemented in subclass
    
    def takeDamage(self, damage):
        if damage > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                return f"{self.name} has been knocked out!"
            else:
                return f"{self.name} took {damage} damage and has {self.health} health remaining"
        else:
            return f"{self.name} took no damage."
    
    def resetValues(self):
        self.health = self.maxHealth
    
    def details(self):
        return f"{self.name} is a {type(self).__name__} and has the following stats:\nHealth: {self.health}\nStrength: {self.strength}\nDefence: {self.defence}"

# Ranger class
class Ranger(Combatant):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, arrows):
        super().__init__(name, maxHealth, strength, defence)
        self.magic = magic
        self.ranged = ranged
        self.arrows = arrows
    
    def attack(self, enemy):
        if self.arrows > 0:
            damage = self.ranged
            self.arrows -= 1
        else:
            damage = self.strength
        
        return enemy.takeDamage(damage)
    
    def resetValues(self):
        super().resetValues()
        self.arrows = 3 if self.arrows == 0 else self.arrows
    
    def details(self):
        return super().details() + f"\nMagic: {self.magic}\nRanged: {self.ranged}\nArrows: {self.arrows}"

# Warrior class
class Warrior(Combatant):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, armourLevel):
        super().__init__(name, maxHealth, strength, defence)
        self.magic = magic
        self.ranged = ranged
        self.armourLevel = armourLevel
    
    def attack(self, enemy):
        damage = self.strength
        return enemy.takeDamage(damage)
    
    def resetValues(self):
        super().resetValues()
        self.armourLevel = 10
    
    def details(self):
        return super().details() + f"\nMagic: {self.magic}\nRanged: {self.ranged}\nArmour Level: {self.armourLevel}"

# Dharok class
class Dharok(Warrior):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, armourLevel):
        super().__init__(name, maxHealth, strength, defence, magic, ranged, armourLevel)
    
    def attack(self, enemy):
        missingHealth = self.maxHealth - self.health
        damage = self.strength + missingHealth
        return enemy.takeDamage(damage)

# Guthans class
class Guthans(Warrior):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, armourLevel):
        super().__init__(name, maxHealth, strength, defence, magic, ranged, armourLevel)
    
    def attack(self, enemy):
        self.heal()
        damage = self.strength
        return enemy.takeDamage(damage)
    
    def heal(self):
        self.health += self.strength // 5
        if self.health > self.maxHealth:
            self.health = self.maxHealth

# Karil class
class Karil(Warrior):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, armourLevel):
        super().__init__(name, maxHealth, strength, defence, magic, ranged, armourLevel)
    
    def attack(self, enemy):
        damage = self.strength + self.ranged
        return enemy.takeDamage(damage)

# Mage base class
class Mage(Combatant):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, mana):
        super().__init__(name, maxHealth, strength, defence)
        self.magic = magic
        self.ranged = ranged
        self.mana = mana
    
    def castSpell(self, enemy):
        pass  # To be implemented in subclass
    
    def resetValues(self):
        super().resetValues()
        self.mana = 100
    
    def details(self):
        return super().details() + f"\nMagic: {self.magic}\nRanged: {self.ranged}\nMana: {self.mana}"

# PyroMage class
class PyroMage(Mage):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, mana):
        super().__init__(name, maxHealth, strength, defence, magic, ranged, mana)
        self.regenRate = 10
    
    def castSpell(self, enemy):
        if self.mana >= 40:
            self.superHeat()
        elif self.mana > 10:
            self.fireBlast()
        else:
            return f"{self.name} has insufficient mana to cast a spell!"
        
        self.mana += self.regenRate
        return enemy.takeDamage(self.strength)
    
    def superHeat(self):
        self.strength += 10
        self.mana -= 40
    
    def fireBlast(self):
        self.mana -= 10

# FrostMage class
class FrostMage(Mage):
    def __init__(self, name, maxHealth, strength, defence, magic, ranged, mana):
        super().__init__(name, maxHealth, strength, defence, magic, ranged, mana)
        self.iceBlock = False
    
    def castSpell(self, enemy):
        if self.mana >= 50:
            self.iceBlock = True
            self.mana -= 50
        elif self.mana > 10:
            return enemy.takeDamage(self.strength // 4 + 30)
        else:
            return f"{self.name} has insufficient mana to cast a spell!"
        
        return ""
    
    def takeDamage(self, damage):
        if self.iceBlock:
            self.iceBlock = False
            return f"{self.name}'s ice block absorbs the attack!"
        else:
            return super().takeDamage(damage)
    
    def resetValues(self):
        super().resetValues()
        self.iceBlock = False

# Arena class
class Arena:
    def __init__(self, name):
        self.name = name
        self.combatants = []
    
    def addCombatant(self, combatant):
        self.combatants.append(combatant)
        print(f"{combatant.name} was added to {self.name}")
    
    def removeCombatant(self, combatant):
        if combatant in self.combatants:
            self.combatants.remove(combatant)
            print(f"{combatant.name} was removed from {self.name}")
        else:
            print(f"{combatant.name} cannot be removed as they were not found in the arena")
    
    def listCombatants(self):
        print(f"Combatants in Arena {self.name}:")
        for combatant in self.combatants:
            print(combatant.details())
        print()
    
    def restoreCombatants(self):
        for combatant in self.combatants:
            combatant.resetValues()
        print(f"----- RESTING -----")
        self.listCombatants()
    
    def duel(self, combatant1, combatant2):
        print(f"----- Battle has taken place in {self.name} on the Castle Walls between {combatant1.name} and {combatant2.name} -----")
        rounds = 1
        
        while rounds <= 10 and combatant1.health > 0 and combatant2.health > 0:
            # Combatant 1 attacks Combatant 2
            if combatant2.health > 0:
                attack_result = combatant1.attack(combatant2)
                print(f"Round {rounds}")
                print(attack_result)
            
            # Combatant 2 attacks Combatant 1
            if combatant1.health > 0:
                attack_result = combatant2.attack(combatant1)
                print(attack_result)
            
            rounds += 1
        
        if combatant1.health <= 0:
            print(f"{combatant1.name} has no health to battle")
        elif combatant2.health <= 0:
            print(f"{combatant2.name} has no health to battle")
        else:
            print(f"The battle ran out of time!")
        
        print(f"---------- END BATTLE ----------")
        print()

# Creating the different combatant objects
try:
    durial = Mage("Durial", 99, 99, 99, 99, 99, 99)
except TypeError:
    print("Mages must be specialized!")

tim = Ranger("Tim", 99, 10, 10, 1, 50, 3)
jay = Warrior("Jay", 99, 1, 99, 1, 1, 10)
kevin = Dharok("Kevin", 99, 45, 25, 25, 25, 10)
zac = Guthans("Zac", 99, 45, 30, 1, 1, 10)
jeff = Karil("Jeff", 99, 50, 40, 1, 10, 5)
jaina = FrostMage("Jaina", 99, 10, 20, 94, 10, 50)
zezima = PyroMage("Zezima", 99, 15, 20, 70, 1, 100)

# Setting up the first arena
falador = Arena("Falador")
falador.addCombatant(tim)
falador.addCombatant(jeff)
falador.listCombatants()
falador.duel(tim, jeff)
falador.duel(tim, jeff)  # To showcase incorrect duels
falador.duel(jeff, zezima)  # To showcase non-existent combatant

# Showcasing restoring combatants
falador.listCombatants()
falador.restoreCombatants()
falador.listCombatants()

# Showcasing removing from arena
falador.removeCombatant(jeff)
falador.removeCombatant(jeff)  # Attempting to remove again

# Setting up the second arena
varrock = Arena("Varrock")
varrock.addCombatant(kevin)
varrock.addCombatant(zac)
varrock.duel(kevin, zac)

# Setting up the third arena
wilderness = Arena("Wilderness")
wilderness.addCombatant(jaina)
wilderness.addCombatant(zezima)
wilderness.duel(jaina, zezima)

# Setting up final arena
lumbridge = Arena("Lumbridge")
lumbridge.addCombatant(jaina)
lumbridge.addCombatant(jay)
lumbridge.addCombatant(tim)
lumbridge.duel(jaina, jay)
lumbridge.duel(jay, tim)  # Duel that takes too long



                

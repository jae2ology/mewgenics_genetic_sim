import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

# gene vs. genome vs. allele (trait)
# ALLELE or TRAIT: the variation of a specific gene. Basically causes the phenotype of the type of gene that is inherited.
# GENE: the DNA that provides instructions for a trait. Rulebook that will determine who gets what phenotype
# GENOME: Entire collection of genetic material. Map of cat's DNA.

# battle abilities and skills
@dataclass
class Ability:
    name: str
    description: str
    energy_cost: int
    element: str

ABILITY_LIBRARY = {
    # Fighter
    "Pounce": Ability("Pounce", "Leap onto target for 1.5x physical damage", 2, "Physical"),
    "Slash": Ability("Slash", "Quick claw strike with bleed chance", 1, "Physical"),
    # Hunter
    "Shadow Step": Ability("Shadow Step", "Teleport behind target, boosting Dodge", 3, "Stealth"),
    "Snipe": Ability("Snipe", "High critical-chance ranged arrow strike", 3, "Physical"),
    # Mage
    "Fireball": Ability("Fireball", "Launch a flaming projectile dealing AoE fire damage", 4, "Fire"),
    "Arcane Blast": Ability("Arcane Blast", "Pure magical force burst ignoring armor", 3, "Arcane"),
    # Tank
    "Taunt": Ability("Taunt", "Force all enemies to attack this cat for 2 turns", 2, "Control"),
    "Iron Shell": Ability("Iron Shell", "Gain massive temporary shield", 3, "Defense"),
    # Cleric
    "Purifying Light": Ability("Purifying Light", "Heal lowest HP ally and remove debuffs", 3, "Holy"),
    "Regen Aura": Ability("Regen Aura", "Apply passive healing over 3 turns to team", 2, "Holy"),
    # Wild / Stray
    "Feral Bite": Ability("Feral Bite", "Vicious unrefined bite dealing damage and healing self", 2, "Wild"),
}


# classes, skills, and archetypes

@dataclass
class ClassArchetype:
    name: str
    associated_color: str
    base_stat_modifiers: Dict[str, float]
    innate_abilities: List[Ability]

ALL_STATS = ["strength", "speed", "intelligence", "dexterity", "luck", "health"]

ARCHETYPES = {
    "Fighter": ClassArchetype(
        name="Fighter",
        associated_color="Red",
        base_stat_modifiers={"strength": 2.0, "speed": 1.0, "intelligence": -1.0, "dexterity": 0.0, "luck": 0.0, "health": 0.0},
        innate_abilities=[ABILITY_LIBRARY["Pounce"], ABILITY_LIBRARY["Slash"]]
    ),
    "Hunter": ClassArchetype(
        name="Hunter",
        associated_color="Green",
        base_stat_modifiers={"dexterity": 3.0, "luck": 2.0, "health": -1.0, "speed": -2.0, "strength": 0.0, "intelligence": 0.0},
        innate_abilities=[ABILITY_LIBRARY["Shadow Step"], ABILITY_LIBRARY["Snipe"]]
    ),
    "Mage": ClassArchetype(
        name="Mage",
        associated_color="Blue",
        base_stat_modifiers={"intelligence": 4.0, "health": -2.0, "strength": -1.0, "speed": 1.0, "dexterity": 0.0, "luck": 0.0},
        innate_abilities=[ABILITY_LIBRARY["Fireball"], ABILITY_LIBRARY["Arcane Blast"]]
    ),
    "Tank": ClassArchetype(
        name="Tank",
        associated_color="Orange",
        base_stat_modifiers={"health": 5.0, "strength": 1.0, "speed": -3.0, "dexterity": -1.0, "intelligence": 0.0, "luck": 0.0},
        innate_abilities=[ABILITY_LIBRARY["Taunt"], ABILITY_LIBRARY["Iron Shell"]]
    ),
    "Cleric": ClassArchetype(
        name="Cleric",
        associated_color="White",
        base_stat_modifiers={"intelligence": 2.0, "health": 2.0, "strength": -2.0, "speed": 0.0, "dexterity": 0.0, "luck": 1.0},
        innate_abilities=[ABILITY_LIBRARY["Purifying Light"], ABILITY_LIBRARY["Regen Aura"]]
    ),
    "Collarless": ClassArchetype(
        name="Collarless",
        associated_color="Brown",
        base_stat_modifiers={"strength": 0.5, "speed": 0.5, "intelligence": 0.0, "health": 0.5, "dexterity": 0.0, "luck": 0.0},
        innate_abilities=[]
    ),
    "Stray": ClassArchetype(
        name="Stray",
        associated_color="Grey",
        base_stat_modifiers={},  # dynamically generated when created from (0 to 4)
        innate_abilities=[ABILITY_LIBRARY["Feral Bite"]]
    ),
}

@dataclass
class BattleCollar:
    name: str
    unlocked_abilities: List[Ability] = field(default_factory=list)


@dataclass
class Cat:
    name: str
    coat_color: str
    archetypes: List[str]
    stats: Dict[str, float]
    inherited_abilities: List[Ability] = field(default_factory=list)
    equipped_collar: Optional[BattleCollar] = None
    is_stray: bool = False

    def get_all_abilities(self) -> List[Ability]:
        """Combines genetic abilities and collar abilities, strictly capped at MAX_SKILLS_PER_CAT (4)."""
        collar_skills = self.equipped_collar.unlocked_abilities if self.equipped_collar else []
        combined_dict = {a.name: a for a in (self.inherited_abilities + collar_skills)}
        all_skills = list(combined_dict.values())

        return all_skills[:4]


def generate_stray_stats() -> Dict[str, float]:
    """gnerates randomized stats between 0.0 and 4.0 for a stray cat."""
    # using random integers or 1-decimal floats between 0 and 4
    return {stat: float(random.randint(0, 4)) for stat in ALL_STATS}

def create_cat(name: str, class_key: str, collar_skill: Optional[str] = None) -> Cat:
    """factory function for creating Cats"""
    arch = ARCHETYPES[class_key]
    collar = BattleCollar(f"{class_key} Collar", [ABILITY_LIBRARY[collar_skill]]) if collar_skill else None
    is_stray = (class_key == "Stray")

    # if it's a Stray, assign randomized stats (0 to 4 in each stat)
    if is_stray:
        cat_stats = generate_stray_stats()
    else:
        cat_stats = dict(arch.base_stat_modifiers)

    return Cat(
        name=name,
        coat_color=arch.associated_color,
        archetypes=[arch.name],
        stats=cat_stats,
        inherited_abilities=list(arch.innate_abilities),
        equipped_collar=collar,
        is_stray=is_stray
    )
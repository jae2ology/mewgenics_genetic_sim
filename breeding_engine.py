import random
from typing import Dict, Tuple, List

from cat_information import create_cat, Cat, ABILITY_LIBRARY


class BreedingEngine:

    @staticmethod
    def calculate_offspring_stats(cat_a: Cat, cat_b: Cat) -> Dict[str, float]:
        all_stat_keys = set(cat_a.stats.keys()).union(set(cat_b.stats.keys()))
        offspring_stats = {}

        # variance if wild Stray DNA is involved
        variance_sigma = 1.2 if (cat_a.is_stray or cat_b.is_stray) else 0.5

        for stat in all_stat_keys:
            val_a = cat_a.stats.get(stat, 0.0)
            val_b = cat_b.stats.get(stat, 0.0)

            # avg stats between parents
            mean_stat = (val_a + val_b) / 2.0

            # add organic float variance (Gaussian drift)
            stat_drift = random.gauss(0, variance_sigma)
            offspring_stats[stat] = round(mean_stat + stat_drift, 1)

        return offspring_stats

    @staticmethod
    def inherit_color_and_archetypes(cat_a: Cat, cat_b: Cat) -> Tuple[str, List[str]]:
        combined_archetypes = list(set(cat_a.archetypes + cat_b.archetypes))

        if len(combined_archetypes) > 1:
            for neutral_tag in ["Stray", "Collarless"]:
                if neutral_tag in combined_archetypes:
                    combined_archetypes.remove(neutral_tag)

        colors = [cat_a.coat_color, cat_b.coat_color]
        specialized_colors = [c for c in colors if c not in ["Grey", "Brown"]]

        if len(specialized_colors) == 1:
            offspring_color = specialized_colors[0]
        elif len(specialized_colors) > 1:
            offspring_color = random.choice(specialized_colors)
        else:
            offspring_color = random.choice(colors)

        return offspring_color, combined_archetypes

    @classmethod
    def breed(cls, parent_a: Cat, parent_b: Cat, offspring_name: str) -> Cat:
        offspring_stats = cls.calculate_offspring_stats(parent_a, parent_b)
        offspring_color, offspring_archetypes = cls.inherit_color_and_archetypes(parent_a, parent_b)

        pool_a = parent_a.get_all_abilities()
        pool_b = parent_b.get_all_abilities()
        combined_pool = {a.name: a for a in (pool_a + pool_b)}
        inherited_skills = list(combined_pool.values())

        # if parents combined > 4, randomly sample 3 to leave room for mutations
        if len(inherited_skills) >= 4:
            inherited_skills = random.sample(inherited_skills, 3)

        base_mutation_rate = 0.25 if (parent_a.is_stray or parent_b.is_stray) else 0.08

        if random.random() < base_mutation_rate:
            available_mutations = [a for a in ABILITY_LIBRARY.values() if a not in inherited_skills]
            if available_mutations:
                mutated_skill = random.choice(available_mutations)
                inherited_skills.append(mutated_skill)
                print(f"  GENETIC MUTATION! [{offspring_name}] unlocked rare skill: {mutated_skill.name}!")

        if len(inherited_skills) > 4:
            inherited_skills = inherited_skills[:4]

        return Cat(
            name=offspring_name,
            coat_color=offspring_color,
            archetypes=offspring_archetypes,
            stats=offspring_stats,
            inherited_abilities=inherited_skills,
            is_stray=False
        )

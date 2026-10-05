from breeding_engine import BreedingEngine
from cat_information import create_cat

if __name__ == "__main__":
    print("BREEDING!")

    # Create parents with 2 skills each + 1 collar skill each (total 3 skills each)
    fighter = create_cat("Ignis", "Fighter", collar_skill="Fireball")
    hunter = create_cat("Artemis", "Hunter", collar_skill="Feral Bite")

    print(f"{fighter.name} Abilities: {[a.name for a in fighter.get_all_abilities()]}")
    print(f"{hunter.name} Abilities:  {[a.name for a in hunter.get_all_abilities()]}")

    print("\nBreeding offspring across 3 generations...")
    current_parent_a = fighter
    current_parent_b = hunter

    for gen in range(1, 4):
        offspring = BreedingEngine.breed(current_parent_a, current_parent_b, f"Gen_{gen}_Kitten")
        active_skills = offspring.get_all_abilities()

        print(f"\n> Generation {gen} - {offspring.name}:")
        print(f"  Skill Count: {len(active_skills)} / {4}")
        print(f"  Active Skills: {[a.name for a in active_skills]}")

        current_parent_a = offspring

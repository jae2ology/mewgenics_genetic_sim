## Genetic Breeding Engine based on the Mewgenics game!

The project features an advanced **Genetic & Breeding Engine** designed for class inheritance, stat mutation, and skill management. It simulates generational offspring with skill inheritance and statistical variance.

### Key Features

* **Gaussian Stat Drift:** Offspring inherit stats calculated from parent averages modified by a Gaussian distribution curve ($\sigma = 0.5$ for standard cats, $\sigma = 1.2$ for wild strays).
* **Dynamic DNA Mutations:** 
  * **Standard Rate:** ~8% chance to unlock rare mutated abilities during breeding.
  * **Wild Rate:** ~25% boosted mutation chance when breeding with Stray lines.
* **Color & Archetype Inheritance:** Merges multi-class archetypes while eliminating neutral fallback tags (`Stray`, `Collarless`) in favor of dominant class traits.

---

### 🧪 Running the Genetic Test Suite

The repository includes a built-in verification suite to analyze mutation distributions, statistical drift across large sample sizes, and multi-generational lineages on your own!

To run the analytics tests:

```bash
python main.py

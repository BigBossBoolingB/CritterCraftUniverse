import hashlib
import random
import math
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# --- QSV-χ-271828182845904523536 Axiomatic Kernel Simulation ---
# This module is a conceptual implementation of the Acausal Engine,
# inspired by the Chronos Initiative's architectural blueprint. It
# simulates Acausal Learning (Ψ) and Meta-Symmetry (Γ) to perform
# hyper-computational tasks within the CritterCraft universe.

@dataclass
class PetDNA:
    """
    Represents the foundational genetic code of a Critter, analogous to the
    on-chain Pet NFT Charter Attributes. The dna_hash is the ultimate
    deterministic "seed".
    """
    dna_hash: str
    base_strength: int
    base_agility: int
    base_intelligence: int
    base_vitality: int
    home_environment: Optional[str] = None


def _is_prime(n: int) -> bool:
    """Helper to check for primality, a simple 'natural' symmetry."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def meta_symmetry_analyzer(dna_hash: str, environment: Optional[str] = None) -> float:
    """
    Simulates the discovery of abstract symmetries (Meta-Symmetry Γ)
    within the problem space of a DNA hash and its environment.

    In this simulation, we look for recognizable mathematical patterns
    (primes, Fibonacci numbers, palindromes) and environmental resonance
    within the hexadecimal string. The presence of these "symmetries"
    indicates a higher latent potential in the genome.

    Returns:
        A 'potential' score from 0.0 to 1.0.
    """
    potential_score = 0.0

    # 1. Palindromic Symmetry: Check for reflective patterns.
    if len(dna_hash) >= 8 and dna_hash[:8] == dna_hash[:8][::-1]:
        potential_score += 0.2

    # 2. Prime Number Sequence: Check for sequences of small primes.
    try:
        if len(dna_hash) >= 15:
            prime_check_segment = int(dna_hash[10:15], 16) % 100
            if _is_prime(prime_check_segment):
                potential_score += 0.15
    except (ValueError, IndexError):
        pass # Ignore if hash is too short or segment is invalid

    # 3. Fibonacci Resonance: Check if parts of the hash align with the Fibonacci sequence.
    if len(dna_hash) >= 25:
        fib_segment = int(dna_hash[20:25], 16) % 1000
        fib_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
        if fib_segment in fib_sequence:
            potential_score += 0.2

    # 4. Environmental Resonance: Check for patterns that suit the environment.
    if environment:
        numeric_hash = int(dna_hash, 16)
        if environment == "forest" and (numeric_hash % 7 == 0):
            # Forests favor complexity and interconnectedness (simulated by divisibility by 7)
            potential_score += 0.25
        elif environment == "ocean" and (numeric_hash % 2 == 0):
            # Oceans favor flow and consistency (simulated by evenness)
            potential_score += 0.25
        elif environment == "desert" and (numeric_hash % 1000 > 800):
            # Deserts favor resilience in extremes (simulated by high numeric value)
            potential_score += 0.25

    # 5. HASH-based potential: A simple numeric aggregate.
    try:
        numeric_value = int(dna_hash, 16)
        potential_score += (numeric_value % 1000) / 3000.0 # Add up to 0.33 based on raw value
    except ValueError:
        pass

    return min(1.0, potential_score)


@dataclass
class AcausalBreedingResult:
    """Holds the comprehensive result of an acausal breeding simulation."""
    optimal_offspring: PetDNA
    proof_of_causality_log: List[Dict]
    temporal_divergence_score: float
    standard_offspring: PetDNA


def _calculate_stat_divergence(pet1: PetDNA, pet2: PetDNA) -> float:
    """Calculates a divergence score based on the distance between pet stats."""
    s_diff = (pet1.base_strength - pet2.base_strength) ** 2
    a_diff = (pet1.base_agility - pet2.base_agility) ** 2
    i_diff = (pet1.base_intelligence - pet2.base_intelligence) ** 2
    v_diff = (pet1.base_vitality - pet2.base_vitality) ** 2
    # Normalize the score to a more readable range
    return math.sqrt(s_diff + a_diff + i_diff + v_diff) / 10.0


def standard_breeder(parent1: PetDNA, parent2: PetDNA) -> PetDNA:
    """
    Simulates a standard, non-acausal breeding outcome.
    This serves as a baseline to measure temporal divergence against.
    """
    # Simple, predictable combination of parent DNA
    seed = parent1.dna_hash + parent2.dna_hash
    new_dna_hash = hashlib.sha256(seed.encode()).hexdigest()

    # Derive stats as usual
    numeric_hash = int(new_dna_hash, 16)
    return PetDNA(
        dna_hash=new_dna_hash,
        base_strength=(numeric_hash >> 16) & 0xFF,
        base_agility=(numeric_hash >> 8) & 0xFF,
        base_intelligence=numeric_hash & 0xFF,
        base_vitality=(numeric_hash >> 24) & 0xFF,
        home_environment=parent1.home_environment or parent2.home_environment
    )


def acausal_breeder(parent1: PetDNA, parent2: PetDNA) -> AcausalBreedingResult:
    """
    Simulates Acausal Learning (Ψ) by pre-computing potential future
    offspring and selecting the most promising timeline.

    Returns a comprehensive result object including the optimal offspring,
    a proof log, and a temporal divergence score.
    """
    potential_offspring = []
    proof_log = []

    # Determine the environment for the offspring
    offspring_env = parent1.home_environment or parent2.home_environment

    # Generate 5 potential future states (offspring)
    for i in range(5):
        seed = str((int(parent1.dna_hash, 16) * int(parent2.dna_hash, 16)) + i)
        new_dna_hash = hashlib.sha256(seed.encode()).hexdigest()

        numeric_hash = int(new_dna_hash, 16)
        candidate = PetDNA(
            dna_hash=new_dna_hash,
            base_strength=(numeric_hash >> 16) & 0xFF,
            base_agility=(numeric_hash >> 8) & 0xFF,
            base_intelligence=numeric_hash & 0xFF,
            base_vitality=(numeric_hash >> 24) & 0xFF,
            home_environment=offspring_env
        )
        potential_offspring.append(candidate)

    # Analyze the potential of each timeline and build the proof log
    best_offspring = potential_offspring[0]
    max_potential = -1.0

    for candidate in potential_offspring:
        potential = meta_symmetry_analyzer(candidate.dna_hash, candidate.home_environment)
        proof_log.append({
            "dna_hash_preview": f"{candidate.dna_hash[:16]}...",
            "stats": f"S:{candidate.base_strength} A:{candidate.base_agility} I:{candidate.base_intelligence} V:{candidate.base_vitality}",
            "potential_score": round(potential, 3)
        })
        if potential > max_potential:
            max_potential = potential
            best_offspring = candidate

    # Generate the standard baseline offspring
    standard_offspring = standard_breeder(parent1, parent2)

    # Calculate the temporal divergence from the standard outcome
    divergence_score = _calculate_stat_divergence(best_offspring, standard_offspring)

    return AcausalBreedingResult(
        optimal_offspring=best_offspring,
        proof_of_causality_log=proof_log,
        temporal_divergence_score=divergence_score,
        standard_offspring=standard_offspring
    )

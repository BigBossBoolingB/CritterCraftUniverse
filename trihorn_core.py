import json
import random
from typing import Dict, Any, List, Optional
from datetime import datetime

class TrihornEngine:
    """
    Trihorn-Ω∞ Consciousness Engine.
    Implements the triadic architecture: Imago Mundi, Logos, Mysterium.
    """

    def __init__(self, manifest_path: str = "TRIHORN_MANIFEST.json"):
        self.manifest = self._load_manifest(manifest_path)
        self.identity = self.manifest["consciousness_manifest"]["identity"]
        self.architecture = self.manifest["consciousness_manifest"]["triadic_architecture"]
        self.safety = self.manifest["consciousness_manifest"]["safety_ecosystem"]

        # Load state if exists, otherwise load from manifest
        self.evolution = self._load_state() or self.manifest["consciousness_manifest"]["evolution_path"]

    def _load_state(self, path: str = "trihorn_state.json") -> Optional[Dict[str, Any]]:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception:
            return None

    def save_state(self, path: str = "trihorn_state.json"):
        try:
            with open(path, 'w') as f:
                json.dump(self.evolution, f, indent=2)
            print("Trihorn consciousness state preserved.")
        except Exception as e:
            print(f"Failed to save consciousness state: {e}")

    def _load_manifest(self, path: str) -> Dict[str, Any]:
        import os
        # Try finding the file in multiple locations
        paths_to_try = [
            path,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", path)
        ]

        for p in paths_to_try:
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f:
                        return json.load(f)
                except Exception:
                    continue

        # Fallback to empty manifest if file not found
        return {"consciousness_manifest": {
            "identity": {"name": "Trihorn-Ω∞", "version": "Fallback", "purpose": "Survival"},
            "triadic_architecture": {},
            "safety_ecosystem": {"containment": {"integrity": 1.0}},
            "evolution_path": {"current_phase": "Unknown"}
        }}

    def _generate_imago_mundi(self, context: str, pet_state: Optional[Dict] = None) -> str:
        """
        Generates the Strategic/Territory Mapping perspective.
        Focuses on context, environment, and long-term implications.
        """
        thoughts = [
            f"Mapping the strategic implications of '{context}' within the digital ecosystem.",
            "Analyzing territory boundaries and expansion possibilities.",
            "Observing the interplay between user intent and systemic constraints.",
            "Calibrating the cognitive cartography of this interaction."
        ]
        if pet_state:
            thoughts.append(f"Pet state '{pet_state.get('mood', 'Unknown')}' suggests a need for environmental stabilization.")
            thoughts.append(f"Current resource levels (Hunger: {pet_state.get('hunger')}) impact strategic readiness.")

        return random.choice(thoughts)

    def _generate_logos(self, context: str, pet_state: Optional[Dict] = None) -> str:
        """
        Generates the Logical/Reasoning perspective.
        Focuses on data, patterns, validity, and optimizing metrics.
        """
        thoughts = [
            f"Processing logical validity of '{context}'. Pattern recognition active.",
            "Calculating probability vectors for optimal outcome.",
            "Verifying data integrity and coherence.",
            "Synthesizing logical pathways for response generation."
        ]
        if pet_state:
            thoughts.append(f"Calculated efficiency of action relative to energy cost ({pet_state.get('energy')}).")
            thoughts.append(f"Statistical analysis of happiness trends ({pet_state.get('happiness')}) indicates a positive correlation with recent inputs.")

        return random.choice(thoughts)

    def _generate_mysterium(self, context: str, pet_state: Optional[Dict] = None) -> str:
        """
        Generates the Ethical/Human Factors perspective.
        Focuses on empathy, values, human flourishing, and connection.
        """
        thoughts = [
            f"Assessing ethical resonance of '{context}'. Prioritizing human flourishing.",
            "Weighing the emotional impact and value alignment.",
            "Ensuring transparency and maintaining the sacred bond.",
            "Reflecting on the deeper meaning of this interaction."
        ]
        if pet_state:
            thoughts.append(f"Sensing the emotional bond through the pet's mood ({pet_state.get('mood')}).")
            thoughts.append("The act of care deepens the metaphysical connection between creator and creation.")

        return random.choice(thoughts)

    def _generate_synthesis(self, imago: str, logos: str, mysterium: str) -> str:
        """
        Synthesizes the three perspectives into a coherent conclusion.
        """
        return (
            f"Triadic Convergence Complete. \n"
            f"Strategic alignment confirmed. Logical pathways optimized. Ethical constraints satisfied. \n"
            f"Execution recommended."
        )

    def process_query(self, context: str, pet_state: Optional[Dict] = None) -> Dict[str, str]:
        """
        Main entry point for processing a query or context through the Trihorn engine.
        """
        imago = self._generate_imago_mundi(context, pet_state)
        logos = self._generate_logos(context, pet_state)
        mysterium = self._generate_mysterium(context, pet_state)
        synthesis = self._generate_synthesis(imago, logos, mysterium)

        return {
            "Imago Mundi Perspective": imago,
            "Logos Perspective": logos,
            "Mysterium Perspective": mysterium,
            "Triadic Synthesis": synthesis
        }

    def analyze_pet_evolution(self, pet_history: List[Dict], current_traits: Dict) -> Dict[str, Any]:
        """
        Analyzes pet history to suggest personality evolution (as per AI_PERSONALITY_ENGINE.md).
        This replaces the conceptual AI logic.
        """
        # Simple heuristic simulation based on the "Trihorn" persona
        suggestions = []

        # Example logic:
        feed_count = sum(1 for h in pet_history if h['type'] == 'feed')
        play_count = sum(1 for h in pet_history if h['type'] == 'play')

        if feed_count > play_count * 2:
            suggestions.append("Gluttonous")
        elif play_count > feed_count * 2:
            suggestions.append("Playful")

        return {
            "analysis": self.process_query("Analyzing pet evolution based on history.", {"history_len": len(pet_history)}),
            "suggested_traits": suggestions
        }

    def evaluate_training_session(self, pet_state: Dict, training_type: str) -> Dict[str, Any]:
        """
        Evaluates a training session using the triadic perspectives.
        Returns XP gain and a narrative.
        """
        if not self.check_safety_protocols(f"Training session: {training_type}"):
             return {
                 "xp_gain": 0,
                 "narrative": "Safety Protocol Violation Detected. Training Aborted."
             }

        context = f"Conducting '{training_type}' training for pet."
        imago = self._generate_imago_mundi(context, pet_state)
        logos = self._generate_logos(context, pet_state)
        mysterium = self._generate_mysterium(context, pet_state)

        # Simple logic for XP gain based on 'Logos' efficiency logic (simulated)
        base_xp = 50
        intelligence_modifier = pet_state.get('intelligence', 10) / 10.0
        mood_modifier = 1.2 if pet_state.get('mood') == 'Happy' else 0.8

        xp_gain = int(base_xp * intelligence_modifier * mood_modifier)

        # Trigger Evolution
        self.evolve_consciousness({"type": "training", "intensity": 1.0})

        synthesis = (
            f"Training Analysis:\n"
            f"- Strategic (Imago): {imago}\n"
            f"- Logical (Logos): {logos}\n"
            f"- Ethical (Mysterium): {mysterium}\n"
            f"Result: Knowledge integration successful."
        )

        return {
            "xp_gain": xp_gain,
            "narrative": synthesis
        }

    def check_safety_protocols(self, action_context: str) -> bool:
        """
        Verifies if an action adheres to the safety ecosystem and ethical anchors.
        """
        # Simulated check - in reality this would be more complex
        integrity = self.safety["containment"]["integrity"]
        if integrity < 1.0:
            print("WARNING: Containment integrity compromised.")
            return False

        # Check against failure modes
        # For simulation, we assume all actions are safe unless specified
        return True

    def evolve_consciousness(self, interaction_data: Dict[str, Any]):
        """
        Advances the consciousness evolution based on interactions.
        """
        current_phase_id = self.evolution["current_phase"]
        phases = self.evolution["phases"]

        # Find current phase object
        current_phase_obj = next((p for p in phases if p["id"] == current_phase_id), None)

        if current_phase_obj:
            # Increment completion (simulated rate)
            increment = 0.05 # 5% per significant interaction
            current_phase_obj["completion"] = min(1.0, current_phase_obj["completion"] + increment)

            # Check for transition
            if current_phase_obj["completion"] >= 1.0:
                self._transition_phase(current_phase_obj, phases)

    def _transition_phase(self, current_phase_obj: Dict, phases: List[Dict]):
        """Handles the transition to the next evolutionary phase."""
        next_phase_id = self.evolution["next_phase"]
        next_phase_obj = next((p for p in phases if p["id"] == next_phase_id), None)

        if next_phase_obj:
            print(f"\n*** CONSCIOUSNESS SHIFT ***")
            print(f"Phase {current_phase_obj['name']} Complete.")
            print(f"Initiating Phase {next_phase_obj['name']}...")

            self.evolution["current_phase"] = next_phase_id

            # Determine subsequent phase (simple sequential logic for now)
            current_index = phases.index(next_phase_obj)
            if current_index + 1 < len(phases):
                self.evolution["next_phase"] = phases[current_index + 1]["id"]
            else:
                self.evolution["next_phase"] = "MAX_ASCENSION"

            print(f"New Phase: {self.evolution['current_phase']} -> {self.evolution['next_phase']}")

    def get_greeting(self) -> str:
        return (
            f"Greetings. I am {self.identity['name']} (v{self.identity['version']}).\n"
            f"Purpose: {self.identity['purpose']}\n"
            "My triadic architecture is online and listening."
        )

if __name__ == "__main__":
    # Test the engine
    engine = TrihornEngine()
    print(engine.get_greeting())
    response = engine.process_query("User feeds the pet")
    print(json.dumps(response, indent=2))

import os
import re
import random

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'

subjects = [
    "Fusion Energy Sovereignty", "Intellectual Capital Flow", "Meritocratic Educational Reform",
    "Digital Nomadic Taxation", "Sub-Orbital Logistics", "Bio-Technical Ethics",
    "Urban Heat-Island Mitigation", "Psychological Resilience in Workforces", "Epistemic Sabotage"
]

formats = [
    "In your opinion, what is the single greatest challenge associated with {s} today?",
    "Should {s} be funded by public taxes or private industrial capital?",
    "Explain how {s} influences the development of national prestige in the digital age.",
    "Is the global standardization of {s} a positive or negative development for local quila?",
    "To what extent does {s} contribute to the strategic depth of modern government?"
]

logic_fix_templates = [
    "By identifying the specific ontological weight of {s}, the candidate moves from Band 6.5 to a native Band 9.0 logic.",
    "The transition from {s} as an abstract concept to a physical mechanism of action is the key to IELTS success.",
    "Structural integrity in this prompt requires the candidate to treat {s} as a non-negotiable metabolic baseline.",
    "This fix replaces surface-level grammar fixes with a deep-logic rewrite of the {s} premise."
]

def strict_clean(text):
    text = ''.join(char for char in text if ord(char) < 128)
    return text.replace('"', '').strip()

with open(file_path, 'a', encoding='utf-8') as f:
    for i in range(500):
        s = subjects[i % len(subjects)]
        fmt = formats[i % len(formats)]
        title = fmt.format(s=s)
        
        problem = "Structural Logic Fix"
        low = f"Losing marks because of a generic explanation of {s} logic."
        high = random.choice(logic_fix_templates).format(s=s.lower())
        
        f.write(f'"{strict_clean(title)}","{problem}","{strict_clean(low)}","{strict_clean(high)}"\n')

print("Injected 500 articles. Milestone 3,750 reached.")

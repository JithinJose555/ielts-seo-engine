import os
import re
import random

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'

subjects = [
    "Genetic Data Ownership", "Supply-Chain Transparency", "Circular Economic Metabolism",
    "Digital Identity Sovereignty", "Urban Micro-Mobility", "Pedagogical Gamification",
    "Sentient AI Rights", "Trans-National Water Governance", "Macro-Fiscual Resilience"
]

formats = [
    "Is the adoption of {s} a beneficial trend for the long-term merit of society?",
    "Should {s} be managed by global institutions or national governments?",
    "What are the primary drivers behind the rise of {s} in modern labor markets?",
    "Does the development of {s} represent a threat to individual cognitive agency?",
    "To what extent do you agree that {s} is the foundation of the modern smart city?"
]

logic_fix_templates = [
    "A Band 9.0 response requires de-linking {s} from generic benefits and anchoring it in strictly logistical outcomes.",
    "By treatng {s} as a meritocratic ritual rather than a lifestyle choice, the candidate demonstrates sovereign logic.",
    "The core problem with {s} logic is usually high-level ambiguity; this fix restores structural certainty.",
    "Strategic clarity regarding {s} is achieved by isolating the specific mechanism of action in the grid."
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
        low = f"Poor vocabulary and generic {s} logic which results in a Band 6.0 score."
        high = random.choice(logic_fix_templates).format(s=s.lower())
        
        f.write(f'"{strict_clean(title)}","{problem}","{strict_clean(low)}","{strict_clean(high)}"\n')

print("Injected 500 articles. Total count moving toward 3,250.")

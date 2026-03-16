import os
import re
import random

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'

# Frontier Subjects Matrix
frontier_subjects = [
    "Deep-Sea Resource Extraction", "Neural Link Privacy", "Algorithmic Wealth Redistribution",
    "Orbital Debris Management", "Somatic Bio-Hacking", "Cognitive Labor Automation",
    "Synthetic Biological Integrity", "Sub-Surface Urbanism", "Atmospheric Governance"
]

# Diverse Question Types
formats = [
    "To what extent should governments regulate {s} to protect individual sovereignty?",
    "Is the global transition toward {s} a positive or negative development for human merit?",
    "Do you agree or disagree that {s} will define the strategic stability of the next century?",
    "Discuss the advantages and disadvantages of {s} for modern high-status cities.",
    "Should educational systems prioritize {s} over traditional theoretical study?"
]

# Logic Matrix for Band 9 fixes
logic_fix_templates = [
    "By treating {s} as a structural governor rather than a secondary utility, the candidate accesses a higher-status band score.",
    "The merit of {s} logic is found in the calibrated link between territorial rights and civilizational survival.",
    "Substituting generic emotional filler with a strict metabolic analysis of {s} ensures a native-level authoritative tone.",
    "Strategic depth in this essay is achieved by isolating the specific mechanism of action inherent in {s}."
]

def strict_clean(text):
    text = ''.join(char for char in text if ord(char) < 128)
    return text.replace('"', '').strip()

with open(file_path, 'a', encoding='utf-8') as f:
    for i in range(250):
        s = frontier_subjects[i % len(frontier_subjects)]
        fmt = formats[i % len(formats)]
        title = fmt.format(s=s)
        
        problem = "Structural Logic Fix"
        low = f"Losing points because of poor {s} logic and generic vocabulary."
        high = random.choice(logic_fix_templates).format(s=s.lower())
        
        f.write(f'"{strict_clean(title)}","{problem}","{strict_clean(low)}","{strict_clean(high)}"\n')

print("Injected 250 Frontier Series articles. Total count moving toward 2,750.")

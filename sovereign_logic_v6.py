import csv
import random
import re

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'

# Significantly expanded Pillars to ensure 5,000+ unique titles
pillars = {
    "EDUCATION": [
        "Academic Inflation", "Vocational Alignment", "Pedagogical Gamification", "Standardized Testing Bias", 
        "University Autonomy", "Lifelong Learning", "Digital Literacy", "Early Childhood Pedagogy", 
        "Tertiary Education Equity", "STEM Prioritization", "Liberal Arts Sovereignty", "School Decentralization",
        "Home-schooling Efficacy", "Adult Education Funding", "Teacher Performance Metrics", "Classroom Diversity",
        "Inclusive Education Laws", "Private School Vouchers", "Academic Research Funding", "Student Exchange Programs",
        "Language Immersion", "Distance Learning Challenges", "Preschool Quality", "Educational Meritocracy"
    ],
    "ECONOMICS": [
        "Macro-Economic Stability", "Wealth Distribution", "Labor Market Automation", "Supply-Chain Integrity", 
        "Monetary Sovereignty", "Fiscal Transparency", "Universal Basic Income", "Circular Metabolism", 
        "Consumerist Satiety", "National Debt Logic", "Gig Economy Ethics", "Trade Protectionism",
        "Foreign Direct Investment", "Cryptocurrency Regulation", "Minimum Wage Laws", "Tax Haven Elimination",
        "Sovereign Wealth Funds", "Rural Economic Revitalization", "Housing Market Stability", "Consumer Rights Protection",
        "Inflationary Control Measures", "Global Commodity Prices", "Micro-finance Development", "Economic Sanctions Efficacy"
    ],
    "TECHNOLOGY": [
        "Artificial Intelligence", "Algorithmic Governance", "Neural Surveillance", "Digital Sovereignty", 
        "Data Monopoly", "Cyber Resilience", "Quantum Ethics", "Technological Paternalism", 
        "Smart City Surveillance", "Automation Displacement", "Internet Neutrality", "Biometric Identification",
        "Cloud Data Security", "Open Source Software", "Virtual Reality Training", "E-waste Recycling Tech",
        "Telemedicine Accessibility", "Autonomous Vehicle Liability", "Nano-technology Health", "5G Network Sovereignty",
        "Digital Divide Mitigation", "Online Censorship Laws", "Satellite Internet Privacy", "Blockchain Governance"
    ],
    "GOVERNANCE": [
        "Maritime Jurisprudence", "Judicial Independence", "Legislative Transparency", "Space Resource Rights", 
        "Border Infrastructure", "Diplomatic Reciprocity", "Public Health Mandates", "Anti-Corruption Measures", 
        "Electoral Sovereignty", "Administrative Integrity", "Civic Social Contracts", "Regulatory Oversight",
        "Municipal Auto-nomity", "Federalism vs Centralization", "Peace-keeping Missions", "Constitutional Reform",
        "Lobbying Transparency", "Whistle-blower Protection", "State-owned Enterprises", "Public Procurement Integrity",
        "Emergency Power Limits", "Immigration Quota Ethics", "Privacy Commission Power", "Direct Democracy Models"
    ],
    "ENVIRONMENT": [
        "Ecological Bio-Diversity", "Carbon Sequestration", "Renewable Infrastructure", "Deep-Sea Mining", 
        "Genetic Modification", "Urban Heat Mitigation", "Biodiversity Atrophy", "Sustainable Metabolisms", 
        "Atmospheric Governance", "Water Scarcity Management", "Waste Liquidation", "Nuclear Fusion Safety",
        "Reforestation Strategies", "Plastic Ban Efficacy", "Renewable Energy Subsidies", "Wildlife Habitat Corridors",
        "Desertification Reversal", "Ocean Acidification Mitigation", "Sustainable Urban Sprawl", "Eco-tourism Regulations",
        "Chemical Fertilizer Bans", "Methane Emission Control", "Arctic Resource Protection", "Green Building Codes"
    ],
    "SOCIETY": [
        "Cultural Homogenization", "Demographic Fluidity", "Urban Migration", "Meritocratic Mobility", 
        "Linguistic Sovereignty", "Somatic Privacy", "Social Cohesion Rituals", "Intergenerational Wealth", 
        "Housing Affordability", "Public Infrastructure Ethics", "Media Objectivity", "National Identity Logic",
        "Gender Equality Laws", "Social Welfare Support", "Youth Political Engagement", "Elderly Care Systems",
        "Community Policing Models", "Rural Outmigration", "Religious Tolerance Policy", "Labor Union Strength",
        "Social Mobility Barriers", "Work-Life Balance Ethics", "Public Museum Funding", "Volunteerism Culture"
    ]
}

audit_hooks = [
    "The primary diagnostic failure here is the reliance on simplistic utilitarian outcomes.",
    "The mistake lies in treating {s} as an isolated variable rather than a systemic driver.",
    "This logic is contaminated by a short-term bias that ignores structural stability.",
    "The fundamental error is the attempt to solve {s} issues with surface-level vocabulary.",
    "The flaw detected is a failure to bridge the gap between abstract promise and physical mechanism.",
    "The candidate's reasoning lacks the required friction of a complex analytical framework.",
    "The logic atrophies because it prioritizes emotional appeal over industrial-grade reasoning.",
    "There is a significant logic gap where a correlation is mistaken for a causal mechanism.",
    "The diagnostic indicates a failure to perceive {s} as an ontological baseline for the grid.",
    "A Band 6.5 logic typically treats {s} as a commodity rather than a civilizational ritual."
]

mechanisms = {
    "EDUCATION": [
        "One must argue that {s} is a strategic calibration of human capital.",
        "Precision in {s} logic requires indexing academic output to sovereign demand.",
        "The merit of {s} is found in its capacity to prevent the systemic thinning of the mind.",
        "True depth is achieved by treatng {s} as a required cognitive baseline.",
        "By de-linking {s} from the job-market loop and re-anchoring it in intellectual grit..."
    ],
    "ECONOMICS": [
        "The metabolic health of the trade-grid is predicated upon unique {s} frameworks.",
        "Prioritizing fiscal resilience in {s} allows the state to maintain strategic mobility.",
        "One must interrogate how {s} governs the flow of capital in the modern era.",
        "Substituting transactional velocity with the deep stability of {s} ensures longevity.",
        "The sovereign standard treats {s} as a non-negotiable metabolic baseline for growth."
    ],
    "TECHNOLOGY": [
        "Integrating {s} requires a sophisticated ethical framework to protect individual agency.",
        "The normalization of {s} necessitates a move away from simple tool-utility logic.",
        "We must interrogate how {s} erodes privacy while substituting authentic merit with compliance.",
        "Strategic depth in {s} is found in the balance between optimization and human autonomy.",
        "By identifying {s} as an accelerant of sociological entropy rather than a pure benefit..."
    ],
    "GOVERNANCE": [
        "Legislative oversight of {s} is a fundamental pillar of the existing social contract.",
        "The juridical logic of {s} requires a calibrated balance of power to prevent paralysis.",
        "By treating {s} as a vessel of civic trust, the state preserves its territorial agency.",
        "The merit of {s} logic is found in the separation between order and individual somatic rights.",
        "To reach Band 9, the candidate must justify {s} as a ritual of administrative integrity."
    ],
    "ENVIRONMENT": [
        "Maintaining the integrity of {s} is a prerequisite for long-term civilizational survival.",
        "Ecological resilience via {s} is not a trend, but a non-negotiable biological baseline.",
        "By indexing industrial growth to the metabolic capacity of {s}, stability is achieved.",
        "True depth requires treatng {s} as a foundation for all subsequent national merit.",
        "The liquidation of {s} for short-term gain is a symptom of systemic strategic atrophy."
    ],
    "SOCIETY": [
        "The preservation of {s} serves as a required friction against global homogenization.",
        "Cultural rituals like {s} are the ontological anchors of a resilient community.",
        "By re-anchoring identity in the structure of {s}, the social fabric prevents atrophy.",
        "Meritocratic mobility is inhibited when {s} is treated as a static ornament.",
        "A sophisticated analysis views {s} as a dynamic governor of social cohesion."
    ]
}

conclusions = [
    "This shift from passive observation to active interrogation signals a Band 9.0 linguistic reach.",
    "Consequently, the logic becomes undeniable, forcing the examiner to recognize authoritative command.",
    "Establishing this link is the only way to routinely surpass the Band 7.5 plateau.",
    "This avoids the 'logical traps' that typically prevent high-status scores in writing task 2.",
    "The resulting structure possesses the calibrated depth found in premium academic publications.",
    "This level of analytical rigor demonstrates a native-level grasp of systemic macro-logic.",
    "It is this precise mechanism of action that defines the Sovereign Standard of writing.",
    "Without this pivot, the essay remains a collection of generic sentiments rather than an audit."
]

modifiers = [
    "Global", "Strategic", "Contemporary", "Advanced", "The Ethics of", "National", "Developing", 
    "Sustainable", "Effective", "The Role of", "Individual", "Macro-level", "Micro-level", "Systemic", 
    "Historical", "International", "Universal", "Collaborative", "Mandatory", "Voluntary"
]

def generate_logic(pillar, subject):
    hook = random.choice(audit_hooks).format(s=subject.lower())
    mech = random.choice(mechanisms.get(pillar, mechanisms["ECONOMICS"])).format(s=subject.lower())
    conc = random.choice(conclusions)
    return f"{hook} {mech} {conc}"

def generate_mistake(pillar, subject):
    bank = [
        "I think that {s} is very good and helpful today because it makes everything fast. People like to have {s} to save money and find jobs for their family in the city. It is a positive thing for everyone.",
        "If the government doesn't prioritize {s}, there will be problems and people will be sad. It is the job of the state to make sure {s} is high-status and winning for the common people hoje oggi.",
        "Most people agree that {s} is important for our merit and wealth today. We should use technology to make {s} better so we don't have to work hard anymore in the modern world."
    ]
    return random.choice(bank).format(s=subject.lower())

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["keyword", "problem_name", "band_5_example", "audit_diagnostic", "band_9_fix"])
    
    unique_titles = set()
    total = 0
    # Possible combinations roughly 144 subjects * 20 modifiers * 4 prompts = 11,520
    while total < 5000:
        pillar = random.choice(list(pillars.keys()))
        subj = random.choice(pillars[pillar])
        mod = random.choice(modifiers)
        prompt = random.choice([
            "To what extent do you agree or disagree that {s} is beneficial for society?",
            "Do the advantages of {s} outweigh the disadvantages in the modern world?",
            "Many believe that {s} should be prioritized by governments. Discuss both views and give your opinion.",
            "What are the main causes of problems related to {s}, and how can they be solved?"
        ])
        
        full_subj = f"{mod} {subj}" if mod and mod not in subj else subj
        title = prompt.format(s=full_subj)
        
        if title in unique_titles: continue
        unique_titles.add(title)
        
        mistake = generate_mistake(pillar, full_subj)
        fix = generate_logic(pillar, full_subj)
        audit = random.choice(["Structural Logic Gap", "Causal Mechanism Failure", "Contaminated Premise", "Somatic Logic Atrophy", "Epistemic Sabotage Detection"])
        
        writer.writerow([title, audit, mistake, f"Diagnostic: {audit}.", fix])
        total += 1

print(f"Combinatorial Logic V6 (Final) Complete: {total} unique articles generated.")

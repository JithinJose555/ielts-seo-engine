import csv
import random
import re

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'

# Expanded Granular Topic Pillars for 5,000 Unique Combos
pillars = {
    "EDUCATION": [
        "Vocational Training", "Academic Inflation", "Remote Learning Ethics", "Early Childhood Pedagogy", 
        "Standardized Assessment", "University Funding Models", "Secondary School Curriculum", "Tertiary Education Access",
        "STEM Education Priority", "Liberal Arts Value", "Public vs Private Schooling", "Lifelong Learning Culture",
        "Teacher Salaries", "Digital Literacy", "Homeschooling Trends", "Student Debt Crisis"
    ],
    "ECONOMICS": [
        "Macro-Economic Resilience", "Wealth Redistribution Policies", "Universal Basic Income", "Cryptocurrency Sovereignty", 
        "Supply-Chain Diversification", "Consumerist Entropy", "Labor Market Automation", "National Debt Management",
        "Global Trade Barriers", "Minimum Wage Impacts", "Gig Economy Regulations", "Corporate Taxation Ethics",
        "Fiscal Transparency", "Inflationary Control", "Urban Poverty Mitigation", "Foreign Investment Policy"
    ],
    "TECHNOLOGY": [
        "Artificial Intelligence Ethics", "Digital Privacy Rights", "Algorithmic Bias", "Social Media Censorship", 
        "Quantum Computing Sovereignty", "Facial Recognition Surveillance", "Technological Paternalism", "Data Monopoly Legislation",
        "E-waste Management", "Cyber warfare Ethics", "Broadband Access Rights", "Automation in Medicine",
        "Virtual Reality Socializing", "Blockchain Transparency", "Space Technology Commercialization", "Smart Grid Efficiency"
    ],
    "GOVERNANCE": [
        "Maritime Jurisprudence", "Space Exploitation Rights", "Judicial Independence", "State-Sponsored Surveillance", 
        "Border Infrastructure", "Diplomatic Reciprocity", "Municipal Planning", "Legislative Transparency",
        "Immigration Quotas", "Freedom of Information", "Nuclear Disarmament Diplomacy", "Public Health Mandates",
        "Anti-Corruption Measures", "Electoral Integrity", "Lobbying Regulations", "Decentralized Governance"
    ],
    "ENVIRONMENT": [
        "Ecological Bio-Diversity", "Renewable Energy Transitions", "Circular Economic Metabolism", "Nuclear Fusion Safety", 
        "Genetic Modification Ethics", "Urban Heat-Island Mitigation", "Deep-Sea Mining Rights", "Atmospheric Carbon Sequestration",
        "Micro-plastic Pollution", "Sustainable Urbanism", "Water Scarcity Management", "Deforestation Penalties",
        "Wildlife Trafficking Laws", "Vertical Farming Investment", "Green Hydrogen Infrastructure", "Climate Refugee Policy"
    ],
    "SOCIETY": [
        "Cultural Homogenization", "Ageing Population Dynamics", "Urban Migration Patterns", "Digital Nomad Taxation", 
        "Somatic Personalization", "Meritocratic Mobility", "Linguistic Heritage Preservation", "Civic Social Contracts",
        "Gender Equality Workplace", "Mental Health Public Policy", "Journalism Ethics", "Intergenerational Wealth Gap",
        "Public Transport Subsidies", "Housing Affordability", "Religion in Secular States", "Sports and National Identity"
    ]
}

# Logic Matrix V4 (The Auditor + The Master) - Updated for clarity
logic_dna = {
    "EDUCATION": {
        "mistake": "I think that {s} is very good and helpful for students because it makes them learn many new skills. This is a very positive development for their future career because they need to find a high-paying job. If they don't have this, they will be poor and sad in the modern city today.",
        "audit": "The diagnostic failure here is the reliance on purely utilitarian outcomes without addressing the underlying structural shifts in the labor market.",
        "fix": "A Band 9.0 response must argue that {s} represents a strategic calibration of human capital. By indexing technical proficiency to industrial demand rather than mere caloric volume, society mitigates the risk of academic inflation and ensures long-term civilizational merit."
    },
    "ECONOMICS": {
        "mistake": "The government should definitely spend more money on {s} so the economy grows fast. This is important because everyone wants to be rich and have a good life. If the bank has more money, then business will be better for the high-status winning people today.",
        "audit": "This logic is contaminated by a short-term liquidity bias that ignores the systemic metabolic health of the trade-grid.",
        "fix": "To reach the Sovereign Standard, one must treat {s} as an ontological baseline for national stability. Prioritizing fiscal resilience over transactional velocity allows the state to preserve its strategic mobility against the volatility of the global market."
    },
    "TECHNOLOGY": {
        "mistake": "I believe that {s} is the best way to make the world modern and easy for us. It saves a lot of time and we can connect with everyone on the internet. Technology is always good because it helps us work faster and be more winning in our life today.",
        "audit": "The flaw lies in the blind acceptance of convenience as a metric of progress, which facilitates a state of psychological and cognitive enclosure.",
        "fix": "The normalization of {s} necessitates a sophisticated ethical framework that transcends simple utility. We must interrogate how these systems erode individual agency, substituting authentic merit with a theatrical facade of optimized digital throughput."
    },
    "GOVERNANCE": {
        "mistake": "Laws for {s} should be very strict and mandatory for every person. This will make the city safe and stop the bad people from doing crimes. It is the job of the government to make sure everyone is following the logic rules so that everything is safe today.",
        "audit": "This perspective relies on a primitive authoritarian logic that fails to account for the necessary friction within a functional social contract.",
        "fix": "Legislative oversight of {s} must be viewed as a ritual of civic trust. A Band 9.0 analysis would balance the state's requirement for logistical order with the individual's fundamental right to somatic and intellectual sovereignty."
    },
    "ENVIRONMENT": {
        "mistake": "We have to protect {s} because if the environment is destroyed then we will have no more air or water. This is a bad problem for the future and our children will suffer. Scientists should use technology to fix it so we don't have to worry anymore.",
        "audit": "The error is the treatment of the environment as an external ornament rather than the foundational metabolic baseline of human survival.",
        "fix": "Protecting the integrity of {s} is a non-negotiable strategic priority. Civilizational longevity is predicated on maintaining a stable ecosystem; to treat natural resources as mere commodities is to induce a state of biological and territorial atrophy."
    },
    "SOCIETY": {
        "mistake": "Traditional {s} is very important for our family and community because it makes us feel happy and together. We should keep these old ways because if we forget them, our culture will be lost and everything will be boring in the city today.",
        "audit": "This is a sentimentalist fallacy that ignores the role of culture as a mechanism of identitarian resilience and ritual coherence.",
        "fix": "The preservation of {s} serves as a required friction against the homogenization of the globalized corporate stream. By re-anchoring identity in these ancestral structures, a society maintains the divergent thinking required for authentic civilizational genius."
    }
}

prompts = [
    "To what extent do you agree or disagree that {s} is a positive development for society?",
    "Do the advantages of {s} outweigh the disadvantages in the modern world?",
    "Many believe that {s} should be prioritized by governments. Discuss both views and give your opinion.",
    "What are the main causes of problems related to {s}, and how can they be solved?"
]

# Modifiers to ensure uniqueness
modifiers = [
    "Global", "Strategic", "National", "Advanced", "The Ethics of", "The Future of", 
    "Sustainable", "Digital", "Modern", "Universal", "Individual", "Macro-level",
    "Micro-level", "Systemic", "Long-term", "Immediate", "Historical", "Contemporary"
]

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["keyword", "problem_name", "band_5_example", "audit_diagnostic", "band_9_fix"])
    
    unique_titles = set()
    total_generated = 0
    
    # We need 5000 unique titles
    while total_generated < 5000:
        pillar = random.choice(list(pillars.keys()))
        subject = random.choice(pillars[pillar])
        mod = random.choice(modifiers)
        prompt = random.choice(prompts)
        
        # Combine modifier and subject logic
        if mod and not subject.startswith(mod):
            s_clean = f"{mod} {subject}"
        else:
            s_clean = subject
            
        title = prompt.format(s=s_clean)
        
        if title in unique_titles:
            continue
            
        unique_titles.add(title)
        
        m_raw = logic_dna[pillar]["mistake"].format(s=s_clean.lower())
        audit = logic_dna[pillar]["audit"]
        fix_raw = logic_dna[pillar]["fix"].format(s=s_clean.lower())

        writer.writerow([title, f"{pillar} Structural Integrity", m_raw, audit, fix_raw])
        total_generated += 1

print(f"Total Unique Articles Generated: {total_generated}")

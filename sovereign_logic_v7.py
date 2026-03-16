import csv
import random
import re

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'

# Refined Pillars for maximum relevance
pillars = {
    "EDUCATION": ["Vocational Training", "Academic Rigor", "Early Childhood Education", "STEM Subjects", "Online Learning Platforms", "University Autonomy", "Secondary School Curricula", "Literacy Standards", "Teacher Training", "Lifelong Learning Culture"],
    "ECONOMICS": ["Macro-Economic Stability", "Wealth Distribution", "Universal Basic Income", "Global Trade Agreements", "Supply Chain Resilience", "Small Business Subsidies", "National Debt Management", "Income Inequality", "Labor Market Regulation", "Consumer Spending Habits"],
    "TECHNOLOGY": ["Artificial Intelligence", "Data Privacy Laws", "Cybersecurity Infrastructure", "Automation in Manufacturing", "Social Media Ethics", "Quantum Computing", "Digital Sovereignty", "Technological Innovation", "Internet Access Equity", "Algorithm Transparency"],
    "GOVERNANCE": ["Maritime Law", "Judicial Independence", "Legislative Transparency", "Space Exploration Policy", "Border Control Infrastructure", "Public Health Mandates", "Anti-Corruption Laws", "Diplomatic Relations", "Municipal Planning", "Electoral Integrity"],
    "ENVIRONMENT": ["Ecological Conservation", "Renewable Energy Transitions", "Carbon Neutrality Goals", "Biodiversity Protection", "Waste Management Systems", "Urban Green Spaces", "Climate Change Mitigation", "Sustainable Agriculture", "Deep-Sea Mining Ethics", "Forest Preservation"],
    "SOCIETY": ["Cultural Heritage Preservation", "Ageing Population Dynamics", "Urban Migration Patterns", "Digital Nomad Lifestyles", "Meritocratic Mobility", "Social Cohesion", "Gender Equality in Leadership", "Public Housing Policy", "Media Objectivity", "National Identity"]
}

# Logic DNA V7: Maximum Clarity and Quality
logic_dna = {
    "EDUCATION": {
        "mistake": "I think that {s} is very good and helpful for students because it makes them learn many new skills. This is a very positive development for their future career because they need to find a high-paying job. If they do not have this, they will have many problems in the future.",
        "diagnostic": "You have identified a benefit but failed to explain the actual mechanism. This is a 'Logical Gap' because you assume a job will automatically follow without explaining how the skills are actually applied.",
        "solution": "Prioritizing {s} serves as a critical calibration of a nation's human capital. By moving beyond rote memorization and focusing on strategic analytical depth, the academic system ensures that the workforce possesses the intellectual resilience required to navigate a shifting global economy. Consequently, this creates a sustainable cycle of innovation and economic stability that benefits society as a whole."
    },
    "ECONOMICS": {
        "mistake": "The government should spend more money on {s} so that everyone can be rich. This is important because the economy needs to grow fast so people can buy more things and have a better life today. If we do not do this, the country will stay poor.",
        "diagnostic": "This reasoning is too simplistic. You are stating that spending leads to wealth without explaining the underlying economic principle of fiscal stability or resource allocation.",
        "solution": "Strategic investment in {s} is an essential baseline for long-term national stability. Far from being a mere transactional expense, an optimized approach to this area ensures that the economy can withstand global market volatility while maintaining high levels of transactional velocity. By balancing fiscal prudence with social investment, a state can secure a high-status position in the international trade-grid."
    },
    "TECHNOLOGY": {
        "mistake": "Technology like {s} is the best way to make the world better. It saves a lot of time and we can do everything on our phones very fast. Everyone likes technology because it makes life easy and we can connect with people all over the world.",
        "diagnostic": "Your argument relies on 'convenience' rather than analytical significance. You need to address the ethical or structural impact of the technology on the individual or the community.",
        "solution": "The normalization of {s} necessitates a sophisticated ethical framework that goes beyond simple utility. To achieve a Band 9.0 standard, one must examine how these digital systems influence individual agency and the private commons. By integrating robust transparency and data sovereignty into the core design, we can ensure that technological progress does not come at the expense of authentic human merit and autonomy."
    },
    "GOVERNANCE": {
        "mistake": "Laws for {s} must be very strong so that people follow the rules. This is the only way to make the city safe and stop bad people from doing things. It is the job of the government to make sure everyone is safe and happy every day.",
        "diagnostic": "This is a basic authoritarian circular logic. You are saying the law works because it's strong, but you aren't explaining the balance between security and individual freedom.",
        "solution": "Effective legislative oversight of {s} must be viewed as a ritual of civic trust rather than a purely punitive mechanism. A sophisticated social contract balances the state’s requirement for logistical order with the individual’s fundamental right to somatic and intellectual sovereignty. When these rules are implemented with transparency and judicial independence, they provide the structural certainty required for civilizational expansion."
    },
    "ENVIRONMENT": {
        "mistake": "We must protect {s} because if the environment is dirty then we will have no more air or water. This is a big problem for the world and our children will have no food. We should use logic to fix this and stop the pollution.",
        "diagnostic": "You are making an emotional plea rather than a logical argument. You need to treat the environment as a foundational biological baseline that sustains the entire survival grid.",
        "solution": "Maintaining the integrity of {s} is a non-negotiable strategic priority for any society seeking long-term longevity. Rather than viewing the environment as an external aesthetic concern, it should be treated as the foundational metabolic baseline of human survival. By indexing industrial growth to the biological capacity of the territory, we prevent the metabolic atrophy that typically precedes civilizational collapse."
    },
    "SOCIETY": {
        "mistake": "Traditions and {s} are very important for our family and culture. We should keep these old ways because they make us feel together and happy. If we forget our culture, the world will be very boring and everyone will be the same.",
        "diagnostic": "This is a 'sentimentalist fallacy.' You are valuing tradition based on feelings rather than explaining its role as a mechanism for social cohesion or identity preservation.",
        "solution": "The preservation of {s} serves as a critical friction against the homogenization of the globalized corporate stream. By re-anchoring individual identity in these ancestral structures, a community maintains the divergent thinking and ritual coherence required for authentic creative genius. This cultural resilience ensures that the social fabric remains robust enough to navigate the pressures of modern migration and demographic fluidity."
    }
}

prompts = [
    "To what extent do you agree or disagree that {s} is a positive development for society?",
    "Do the advantages of {s} outweigh the disadvantages in the modern world?",
    "Many believe that {s} should be prioritized by governments. Discuss both views and give your opinion.",
    "What are the main causes of problems related to {s}, and how can they be solved?"
]

modifiers = [
    "The Role of", "Advanced", "Strategic", "Global", "National", "Developing", 
    "Sustainable", "The Ethics of", "Contemporary", "Individual", "Macro-level", "Systemic"
]

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["keyword", "problem_name", "band_5_example", "audit_diagnostic", "band_9_fix"])
    
    unique_titles = set()
    total = 0
    while total < 5000:
        pillar_name = random.choice(list(pillars.keys()))
        subj = random.choice(pillars[pillar_name])
        mod = random.choice(modifiers)
        prompt = random.choice(prompts)
        
        full_subj = f"{mod} {subj}" if mod and mod not in subj else subj
        title = prompt.format(s=full_subj)
        
        if title in unique_titles: continue
        unique_titles.add(title)
        
        dna = logic_dna[pillar_name]
        mistake = dna["mistake"].format(s=full_subj.lower())
        diagnostic = dna["diagnostic"]
        solution = dna["solution"].format(s=full_subj.lower())
        
        writer.writerow([title, f"{pillar_name.capitalize()} Logic Error", mistake, diagnostic, solution])
        total += 1

print(f"Sovereign Logic V7 (Final Human Polish) Complete: {total} unique articles generated.")

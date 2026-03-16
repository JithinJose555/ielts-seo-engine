import csv
import os
import re
import random

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'
temp_path = r'd:\Google AI\ielts-seo-engine\data_temp.csv'

# ELITE TEACHER MATRIX (Clear, High-Level English)
buckets = {
    "EDUCATION": {
        "keywords": ["education", "pedagogy", "school", "university", "learning", "student", "vocational", "theory"],
        "band_5": "I think {s} is very good because it helps students learn more skills and then they can find a high-paying job easily.",
        "band_9": "Providing universal access to {s} is a strategic investment in nation's human capital, as it ensures the workforce can adapt to a rapidly evolving global economy."
    },
    "ECONOMICS": {
        "keywords": ["monetary", "wealth", "fiscual", "economic", "finance", "debt", "taxation", "supply-chain", "trade", "investment"],
        "band_5": "Governments should spend more money on {s} so that the country becomes rich and people don't have to be poor anymore.",
        "band_9": "Prioritizing {s} is essential for national stability; it allows a country to build economic resilience and protects the citizens from global market fluctuations."
    },
    "TECHNOLOGY": {
        "keywords": ["digital", "algorithmic", "neural", "ai", "automation", "cyber", "technology", "software", "virtual", "internet"],
        "band_5": "Computers and {s} make our lives very fast and easy because we can find any information we want just by clicking a button.",
        "band_9": "The integration of {s} into our daily lives is not just about convenience; it is a fundamental shift that requires new ethical frameworks to protect individual privacy."
    },
    "GOVERNANCE": {
        "keywords": ["sovereignty", "judicial", "legal", "rights", "jurisprudence", "state", "government", "regulate", "law", "ethics", "security"],
        "band_5": "The government must make strict laws for {s} so that everyone follows the same rules and the city stays safe for everyone.",
        "band_9": "Legislative oversight of {s} is a necessary part of the social contract, balancing the need for public security with the fundamental right to individual freedom."
    },
    "ENVIRONMENT": {
        "keywords": ["biological", "genetic", "health", "environment", "ecological", "mining", "nature", "biodiversity", "nutritional", "pollution"],
        "band_5": "We should protect the {s} because if the earth is dirty, our health will become bad and our children will have no future.",
        "band_9": "Protecting the integrity of {s} is a critical responsibility for modern nations, as the long-term health of the population depends on a stable and diverse ecosystem."
    }
}

# Real IELTS Prompt Styles
prompts = [
    "To what extent do you agree or disagree that {s} is beneficial for society?",
    "Do the advantages of {s} outweigh the disadvantages in the modern world?",
    "Many believe that {s} should be prioritized by the state. Discuss both views and give your opinion.",
    "What are the main causes of problems related to {s}, and how can they be solved?"
]

def get_clean_subject(keyword):
    # Remove all the extra jargon to get the core noun
    s = re.sub(r'ielts (task 2|writing task 2|speaking part 3): ', '', keyword, flags=re.IGNORECASE)
    s = re.sub(r'(To what extent|Is the trend toward|Many believe that|Discuss the|What are the|Is the|Should|How has the|Many argue that|Does the)', '', s, flags=re.IGNORECASE)
    s = s.replace('?', '').split(' on ')[0].split(' for ')[0].split(' toward ')[0].strip()
    return s if s else "this issue"

with open(file_path, 'r', encoding='utf-8') as f_in, open(temp_path, 'w', encoding='utf-8', newline='') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out, quoting=csv.QUOTE_ALL)
    
    header = next(reader)
    writer.writerow(header)
    
    for row in reader:
        original_title = row[0]
        subject = get_clean_subject(original_title)
        
        # Determine Bucket
        b_name = "ECONOMICS" # default
        for name, data in buckets.items():
            if any(w in subject.lower() for w in data["keywords"]):
                b_name = name
                break
        
        # 1. Authentic Title
        new_title = random.choice(prompts).format(s=subject.capitalize())
        
        # 2. Believable Student Mistake
        mistake = buckets[b_name]["band_5"].format(s=subject.lower())
        
        # 3. Clear Expert Solution
        fix = buckets[b_name]["band_9"].format(s=subject.lower())
        
        writer.writerow([new_title, "Structural Logic Fix", mistake, fix])

os.replace(temp_path, file_path)
print("Surgical Reset complete. Titles are now authentic, and logic is clear and human-grade.")

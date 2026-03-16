import csv
import os
import re
import random

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'
temp_path = r'd:\Google AI\ielts-seo-engine\data_temp.csv'

# ELITE TEACHER MATRIX (Clear, High-Level English)
buckets = {
    "EDUCATION": {
        "keywords": ["education", "pedagogy", "school", "university", "learning", "student", "vocational", "theory", "teaching", "campus", "academic"],
        "band_5": "I think {s} is very good because it helps students learn more skills and then they can find a high-paying job easily.",
        "band_9": "Providing universal access to {s} is a strategic investment in a nation's human capital, as it ensures the workforce can adapt to a rapidly evolving global economy."
    },
    "ECONOMICS": {
        "keywords": ["monetary", "wealth", "fiscual", "economic", "finance", "debt", "taxation", "supply-chain", "trade", "investment", "money", "employment", "market", "resilience"],
        "band_5": "Governments should spend more money on {s} so that the country becomes rich and people don't have to be poor anymore.",
        "band_9": "Prioritizing {s} is essential for national stability; it allows a country to build economic resilience and protects the citizens from global market fluctuations."
    },
    "TECHNOLOGY": {
        "keywords": ["digital", "algorithmic", "neural", "ai", "automation", "cyber", "technology", "software", "virtual", "internet", "machine", "data", "compute"],
        "band_5": "Computers and {s} make our lives very fast and easy because we can find any information we want just by clicking a button.",
        "band_9": "The integration of {s} into our daily lives is not just about convenience; it is a fundamental shift that requires new ethical frameworks to protect individual privacy."
    },
    "GOVERNANCE": {
        "keywords": ["sovereignty", "judicial", "legal", "rights", "jurisprudence", "state", "government", "regulate", "law", "ethics", "security", "policy", "citizen"],
        "band_5": "The government must make strict laws for {s} so that everyone follows the same rules and the city stays safe for everyone.",
        "band_9": "Legislative oversight of {s} is a necessary part of the social contract, balancing the need for public security with the fundamental right to individual freedom."
    },
    "ENVIRONMENT": {
        "keywords": ["biological", "genetic", "health", "environment", "ecological", "mining", "nature", "biodiversity", "nutritional", "pollution", "solar", "energy", "climate", "island"],
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
    # Regex to extract the core noun phrase more aggressively
    # This list covers the topics we've been using
    s = keyword.lower()
    
    # 1. Strip common phrase connectors
    s = re.sub(r'.* related to ', '', s)
    s = re.sub(r'ielts (task 2|writing task 2|speaking part 3): ', '', s)
    s = re.sub(r'.* agree or disagree that ', '', s)
    s = re.sub(r'do the advantages of ', '', s)
    s = re.sub(r'is the trend toward ', '', s)
    s = re.sub(r'many believe that ', '', s)
    s = re.sub(r'how has the perception of ', '', s)
    s = re.sub(r'discuss the impacts of ', '', s)
    s = re.sub(r'is the adoption of ', '', s)
    s = re.sub(r'should the state prioritize ', '', s)
    
    # 2. Strip common phrase endings
    s = s.split(' a beneficial trend')[0]
    s = s.split(' be regulated by the state')[0]
    s = s.split(' evolved among the elite')[0]
    s = s.split(' outweigh the disadvantages')[0]
    s = s.split(' is beneficial for society')[0]
    s = s.split(' on modern labor markets')[0]
    s = s.split(' or strategic risk')[0]
    s = s.split(' for society')[0]
    s = s.split(' in modern high-status')[0]
    s = s.split(' over individual convenience')[0]
    s = s.split(' over traditional theoretical')[0]
    s = s.split(' should be capitalized')[0]
    s = s.split(' should be a fundamental right')[0]
    s = s.split(' should be managed by')[0]
    s = s.split(' should be funded by')[0]
    s = s.split(' influence the long-term')[0]
    s = s.split(' contribute to the strategic')[0]
    s = s.split(' define the strategic stability')[0]
    s = s.split(' define the merit of future')[0]
    s = s.split(' as a primary driver')[0]
    s = s.split(' for the foundational social')[0]
    
    # Clean up punctuation and whitespace
    s = re.sub(r'[^a-zA-Z\s-]', '', s).strip()
    
    # Limit length to avoid long sentences as subjects
    if len(s.split()) > 5:
        s = " ".join(s.split()[:4])
        
    return s.title() if s else "This Topic"

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
        new_title = random.choice(prompts).format(s=subject)
        
        # 2. Believable Student Mistake
        mistake = buckets[b_name]["band_5"].format(s=subject.lower())
        
        # 3. Clear Expert Solution
        fix = buckets[b_name]["band_9"].format(s=subject.lower())
        
        writer.writerow([new_title, "Structural Logic Fix", mistake, fix])

os.replace(temp_path, file_path)
print("Surgical Clean-up: Titles and logic boxes are now concisely related.")

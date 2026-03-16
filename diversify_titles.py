import os
import re
import random

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'
temp_path = r'd:\Google AI\ielts-seo-engine\data_temp.csv'

formats = [
    "To what extent do you agree or disagree with the following statement: {topic}?",
    "Is the trend toward {topic} a positive or negative development for society?",
    "Many believe that {topic}. Discuss both views and give your opinion.",
    "What are the primary causes of {topic}, and what measures can be taken to address it?",
    "In your opinion, does the merit of {topic} outweigh the strategic risks involved?",
    "IELTS Speaking Part 3: How has the role of {topic} evolved in modern high-status economies?",
    "Some argue that {topic} is a civilizational necessity. Others disagree. Discuss both sides."
]

def diversify_title(title):
    # If it contains "the impact of", rewrite it
    if "the impact of" in title.lower():
        # Extract the core subject
        subject = re.sub(r'ielts (task 2|writing task 2|speaking part 3): the impact of ', '', title, flags=re.IGNORECASE)
        subject = subject.replace(' on modern high-status society', '').strip()
        
        # Pick a random high-status format
        fmt = random.choice(formats)
        new_title = fmt.format(topic=subject)
        
        # Re-add the prefix
        prefix = "ielts writing task 2: " if "speaking" not in fmt.lower() else ""
        return prefix + new_title
    return title

with open(file_path, 'r', encoding='utf-8') as f_in, open(temp_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        parts = line.strip().split('","')
        if len(parts) >= 3:
            # Clean part 0 (the title)
            title = parts[0].replace('"', '')
            new_title = diversify_title(title)
            
            # Reconstruct the line
            f_out.write(f'"{new_title}","{parts[1]}","{parts[2]}"\n')

os.replace(temp_path, file_path)
print("Title diversification complete. Repetition liquidated.")

import re
import os

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'
temp_path = r'd:\Google AI\ielts-seo-engine\data_temp.csv'

noise_words = [
    'aujourd\'hui', 'heute', 'hoje', 'आज', 'oggi', 'bugun', 'bugün', 
    'hoy', 'dnes', 'hom nay', 'hodi', 'сегодня', '오늘', 'aujourd h', 'aujourd'
]

def strict_clean(text):
    # Remove specific noise words and fragments
    fragments = ['hui', 'aujourd', 'hodi', 'oggi', 'hoy', 'dnes', 'buğün', 'bugün', 'hôm nay', 'hm nay']
    for frag in fragments:
        text = re.sub(re.escape(frag), '', text, flags=re.IGNORECASE)
    
    # Remove any non-ASCII characters
    text = ''.join(char for char in text if ord(char) < 128)
    
    # Remove awkward apostrophes and quotes left over from cleaning
    text = text.replace("''", "").replace(" ' ' ", " ")
    
    # Clean up excess whitespace and leading/trailing quotes
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

with open(file_path, 'r', encoding='utf-8') as f_in, open(temp_path, 'w', encoding='utf-8', newline='') as f_out:
    for line in f_in:
        # Simple string-based cleaning to avoid CSV parsing errors with messy data
        cleaned_line = strict_clean(line)
        if cleaned_line:
            f_out.write(cleaned_line + '\n')

os.replace(temp_path, file_path)
print("Cleanup complete. File sanitized.")

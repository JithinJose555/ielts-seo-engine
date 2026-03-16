import csv
import os

file_path = r'd:\Google AI\ielts-seo-engine\data.csv'
temp_path = r'd:\Google AI\ielts-seo-engine\data_temp.csv'

with open(file_path, 'r', encoding='utf-8') as f_in, open(temp_path, 'w', encoding='utf-8', newline='') as f_out:
    # Read the header separately
    header = f_in.readline()
    f_out.write("keyword,problem_name,band_5_example,band_9_fix\n")
    
    # Process lines
    for line in f_in:
        # Simple split by custom separator or use csv for safer parsing
        parts = line.strip().split('","')
        # Remove leading/trailing quotes from the parts
        parts = [p.strip('"') for p in parts]
        
        if len(parts) == 3:
            # Missing problem_name, insert it
            keyword = parts[0]
            problem_name = "Structural Logic Fix"
            band_5 = parts[1]
            band_9 = parts[2]
            f_out.write(f'"{keyword}","{problem_name}","{band_5}","{band_9}"\n')
        elif len(parts) == 4:
            # Already correct
            f_out.write(f'"{parts[0]}","{parts[1]}","{parts[2]}","{parts[3]}"\n')

os.replace(temp_path, file_path)
print("CSV structure synchronized for the engine.")

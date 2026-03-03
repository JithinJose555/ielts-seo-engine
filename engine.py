import csv
import os
import re

# Configuration for Vercel environment
INPUT_CSV = 'data.csv'
TEMPLATE_HTML = 'template.html'
OUTPUT_DIR = 'public' # Vercel often uses 'public' for static output or root

def slugify(text):
    """Convert a string to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s\-]+', '-', text)
    return text.strip('-')

def main():
    # In Vercel, we can output to a folder or just the root if it's a static site
    # Let's use 'dist' as you currently have, but create it if missing
    dist_dir = 'dist'
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    # Read the master template
    try:
        with open(TEMPLATE_HTML, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{TEMPLATE_HTML}' not found.")
        return

    # Process the CSV data
    generated_count = 0
    try:
        with open(INPUT_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = row.get('keyword', '').strip()
                if not keyword:
                    continue
                
                problem_name = row.get('problem_name', '').strip()
                band_5_example = row.get('band_5_example', '').strip()
                band_9_fix = row.get('band_9_fix', '').strip()

                # Generate a clean filename for the URL
                slug = slugify(keyword)
                output_filename = f"{slug}.html"
                output_path = os.path.join(dist_dir, output_filename)

                # Inject variables into the HTML template
                page_html = template_content
                page_html = page_html.replace('{{keyword}}', keyword)
                page_html = page_html.replace('{{problem_name}}', problem_name)
                page_html = page_html.replace('{{band_5_example}}', band_5_example)
                page_html = page_html.replace('{{band_9_fix}}', band_9_fix)

                # Write the customized HTML
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(page_html)
                
                generated_count += 1
                
        print(f"✅ Successfully generated {generated_count} pages.")
        
    except FileNotFoundError:
        print(f"Error: Data file '{INPUT_CSV}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

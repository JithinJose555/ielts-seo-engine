import csv
import os
import re
import random

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
    pages = [] # Track generated pages for the index
    try:
        with open(INPUT_CSV, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = (row.get('keyword') or '').strip()
                if not keyword:
                    continue
                
                problem_name = (row.get('problem_name') or '').strip()
                band_5_example = (row.get('band_5_example') or '').strip()
                band_9_fix = (row.get('band_9_fix') or '').strip()

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
                
                pages.append({'title': keyword, 'url': output_filename, 'path': output_path})
                generated_count += 1
        
        # SEO Phase: Dynamic Interlinking
        print("Finalizing SEO Interlinking...")
        for i, page in enumerate(pages):
            related = random.sample(pages, min(5, len(pages)))
            links_html = "".join([f"<a href='{p['url']}' style='color: var(--burgundy); margin-right: 15px; text-decoration: none; font-weight: 600;'>&rarr; {p['title']}</a>" for p in related])
            
            with open(page['path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the placeholder in template
            content = content.replace('<a href="/index.html" style="color: var(--text-muted);">Back to Master Directory</a>', links_html)
            
            with open(page['path'], 'w', encoding='utf-8') as f:
                f.write(content)

        # Generate sitemap.xml for Google indexing
        print("Generating sitemap.xml...")
        sitemap_path = os.path.join(dist_dir, 'sitemap.xml')
        sitemap_header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        sitemap_footer = '</urlset>'
        
        # Replace base_url with your actual vercel domain later
        base_url = "https://ielts-seo-engine.vercel.app/" 
        
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_header)
            f.write(f'  <url><loc>{base_url}</loc><priority>1.0</priority></url>\n')
            for p in pages:
                f.write(f'  <url><loc>{base_url}{p["url"]}</loc><priority>0.8</priority></url>\n')
            f.write(sitemap_footer)
        
        # Generate Categorized index.html
        print("Generating Categorized index.html...")
        index_path = os.path.join(dist_dir, 'index.html')
        
        # Simple grouping by the first word of the title or keyword
        categories = {}
        for p in pages:
            cat = "General"
            for pillar in ["Education", "Economics", "Technology", "Governance", "Environment", "Society"]:
                if pillar in p['title']:
                    cat = pillar
                    break
            if cat not in categories: categories[cat] = []
            categories[cat].append(p)

        cat_html = ""
        for cat, items in categories.items():
            links = "".join([f"<li><a href='{p['url']}'>{p['title']}</a></li>" for p in items[:20]]) # Show top 20 per cat for speed
            cat_html += f"<h2>{cat} Fixes</h2><ul>{links}</ul>"

        index_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>IELTS Surgical Logic - 5,000 Band 9.0 Fixes</title>
            <style>
                body {{ font-family: 'Inter', sans-serif; padding: 50px; line-height: 1.6; background: #f5f7fa; color: #1a1a1a; }}
                h1 {{ color: #800020; border-bottom: 2px solid #800020; padding-bottom: 10px; }}
                h2 {{ margin-top: 40px; color: #5c0015; text-transform: uppercase; font-size: 1.2rem; letter-spacing: 1px; }}
                ul {{ list-style: none; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
                li a {{ text-decoration: none; color: #666; font-size: 0.95rem; }}
                li a:hover {{ color: #800020; text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>IELTS Surgical Logic: The 5,000 Master Directory</h1>
            <p>Access the highest-density logical audits for IELTS Writing Task 2. Select a category to begin your reset.</p>
            {cat_html}
            <div style="margin-top: 50px; padding: 20px; background: #fff; border: 1px solid #ddd;">
                <p><strong>Total Audits Live: 5,000+</strong> | Updated Daily for Maximum Visibility</p>
                <a href="/sitemap.xml">XML Sitemap for Search Engines</a>
            </div>
        </body>
        </html>
        """
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
                
        print(f"Successfully generated {generated_count} pages, sitemap.xml, and categorized index.")
        
    except FileNotFoundError:
        print(f"Error: Data file '{INPUT_CSV}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

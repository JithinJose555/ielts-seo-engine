import csv
import os
import re
import shutil
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

    # Copy verification files to dist
    for file in os.listdir('.'):
        if file.startswith('google') and file.endswith('.html'):
            shutil.copy(file, os.path.join(dist_dir, file))
            print(f"Copied verification file: {file}")

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
                audit_diagnostic = (row.get('audit_diagnostic') or '').strip()
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
                page_html = page_html.replace('{{audit_diagnostic}}', audit_diagnostic)
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
        print("Generating Comprehensive Categorized index.html...")
        index_path = os.path.join(dist_dir, 'index.html')
        
        # Robust grouping by Pillar
        categories = {
            "Education": [], "Economics": [], "Technology": [], 
            "Governance": [], "Environment": [], "Society": [], "General": []
        }
        
        for p in pages:
            found = False
            # Check p['title'] for keywords from our pillars
            for pillar in categories.keys():
                if pillar.lower() in p['title'].lower():
                    categories[pillar].append(p)
                    found = True
                    break
            if not found:
                categories["General"].append(p)

        cat_html = ""
        total_links = 0
        for cat, items in categories.items():
            if not items: continue
            links = "".join([f"<li><a href='{p['url']}'>{p['title']}</a></li>" for p in items])
            total_links += len(items)
            cat_html += f"""
            <section class="category-block">
                <h2>{cat} Logic Audits ({len(items)})</h2>
                <ul class="link-grid">{links}</ul>
            </section>
            """

        index_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="Master IELTS Writing Task 2 with our comprehensive directory of 5,000 surgical logic audits. Band 9.0 expert fixes for every topic.">
            <title>IELTS Surgical Logic - 5,000 Band 9.0 Fixes | Master Directory</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
            <style>
                :root {{ --burgundy: #800020; --text-main: #1a1a1a; --bg: #f5f7fa; }}
                body {{ font-family: 'Inter', sans-serif; padding: 2rem; background: var(--bg); color: var(--text-main); line-height: 1.6; max-width: 1200px; margin: 0 auto; }}
                header {{ text-align: center; margin-bottom: 4rem; padding: 3rem; background: #fff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                h1 {{ font-weight: 800; font-size: 2.5rem; color: var(--burgundy); margin-bottom: 1rem; }}
                .stats {{ font-weight: 600; color: #666; text-transform: uppercase; letter-spacing: 1px; }}
                .category-block {{ margin-bottom: 3rem; }}
                h2 {{ color: var(--burgundy); border-bottom: 2px solid var(--burgundy); padding-bottom: 10px; margin-bottom: 20px; font-size: 1.5rem; }}
                .link-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; list-style: none; padding: 0; }}
                li a {{ text-decoration: none; color: #444; font-size: 0.9rem; transition: color 0.2s; display: block; padding: 5px; border-radius: 4px; }}
                li a:hover {{ color: var(--burgundy); background: #eee; }}
                footer {{ margin-top: 5rem; text-align: center; padding: 2rem; border-top: 1px solid #ddd; color: #666; }}
            </style>
        </head>
        <body>
            <header>
                <h1>IELTS Surgical Logic</h1>
                <p class="stats">The Sovereign Standard: {total_links} Unique Logical Fixes Live</p>
                <p>Don't let Band 6.5 logic kill your score. Browse our 5,000+ expert audits to find your specific logic-fix.</p>
            </header>
            
            <main>
                {cat_html}
            </main>

            <footer>
                <p>&copy; 2026 Jithin Jose - IELTS Surgical Logic Auditor</p>
                <p><a href="/sitemap.xml" style="color: var(--burgundy);">XML Sitemap for Search Engines</a></p>
            </footer>
        </body>
        </html>
        """
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
                
        print(f"Successfully generated {generated_count} pages, sitemap.xml, and a comprehensive index with {total_links} unique links.")
        
    except FileNotFoundError:
        print(f"Error: Data file '{INPUT_CSV}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

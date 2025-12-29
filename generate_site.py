import os
import shutil
from markdown_it import MarkdownIt
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import frontmatter

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLISHED_DIR = os.path.join(BASE_DIR, 'published')
OUTPUT_DIR = os.path.join(BASE_DIR, 'docs')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

def pygments_highlighter(code, lang, attrs):
    """
    Custom highlighter function for markdown-it-py using Pygments.
    Handles Mermaid diagrams by not highlighting them.
    """
    if lang == 'mermaid':
        return f'<pre><code class="mermaid">{code}</code></pre>'

    if not lang:
        lang = 'text'  # Default to plain text if no language is specified

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except ClassNotFound:
        # Fallback to plain text if the language is not found
        lexer = get_lexer_by_name('text', stripall=True)

    formatter = HtmlFormatter(cssclass="highlight") # You can customize the CSS class
    return highlight(code, lexer, formatter)


def setup_markdown_parser():
    md = (MarkdownIt(
        "commonmark",
        {
            "highlight": pygments_highlighter,
            "html": True  # Ensure HTML rendering is enabled
        }
    )
          .enable('image')
          .enable('link')
          .enable('table')
          .enable('fence')
          .enable('code')
          .enable('list')
          .enable('backticks')
          .enable('emphasis')
          .enable('strikethrough')
          .enable('blockquote')
          .enable('hr')
          .enable('heading')
          .enable('paragraph')
          .enable('html_block')
          .enable('html_inline')
          .enable('autolink')
         )
    return md

def setup_jinja_environment():
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), extensions=['jinja2.ext.do'])
    return env

def clean_output_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'posts'), exist_ok=True)
    print(f"Cleaned and created output directory: {OUTPUT_DIR}")

def copy_static_assets():
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, 'static'), dirs_exist_ok=True)
        print(f"Copied static assets from {STATIC_DIR} to {os.path.join(OUTPUT_DIR, 'static')}")
    else:
        print(f"Warning: Static directory not found at {STATIC_DIR}")

def parse_markdown_file(filepath):
    """Parses a markdown file to extract title, date, and content using frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    title = post.metadata.get('title', os.path.basename(filepath).replace('.md', '').replace('-', ' ').title())
    date = post.metadata.get('date', datetime.now()) # Frontmatter should ideally provide a date
    
    # Ensure date is a datetime object for consistent handling
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            date = datetime.now() # Fallback if date string is not in expected format

    return {'title': title, 'date': date, 'content': post.content}


def generate_site():
    md = setup_markdown_parser()
    env = setup_jinja_environment()
    clean_output_dir()
    copy_static_assets()

    base_template = env.get_template('base.html')
    post_template = env.get_template('post.html')
    index_template = env.get_template('index.html')

    posts_metadata = []

    # First pass: gather all post metadata
    for post_dir in os.listdir(PUBLISHED_DIR):
        source_post_path = os.path.join(PUBLISHED_DIR, post_dir)
        if os.path.isdir(source_post_path):
            md_file = None
            for f in os.listdir(source_post_path):
                if f.endswith('.md'):
                    md_file = f
                    break
            
            if not md_file:
                continue

            filepath = os.path.join(source_post_path, md_file)
            post_data = parse_markdown_file(filepath)
            
            posts_metadata.append({
                'title': post_data['title'],
                'date': post_data['date'],
                'url': f'posts/{post_dir}/',
                'source_path': source_post_path,
                'md_file': md_file
            })

    # Sort posts by date, newest first
    posts_metadata.sort(key=lambda x: x['date'], reverse=True)

    # Second pass: generate all post pages
    for post_meta in posts_metadata:
        source_post_path = post_meta['source_path']
        md_file = post_meta['md_file']
        
        filepath = os.path.join(source_post_path, md_file)
        post_data = parse_markdown_file(filepath)
        
        html_content = md.render(post_data['content'])
        
        dest_post_path = os.path.join(OUTPUT_DIR, post_meta['url'])
        os.makedirs(dest_post_path, exist_ok=True)

        # Copy assets
        for item in os.listdir(source_post_path):
            if not item.endswith('.md'):
                s = os.path.join(source_post_path, item)
                d = os.path.join(dest_post_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

        output_filepath = os.path.join(dest_post_path, 'index.html')

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(post_template.render(
                title=post_data['title'],
                date=post_data['date'].strftime('%Y-%m-%d'),
                content=html_content,
                posts=posts_metadata, # Pass all posts for navigation
                root_path='../../' # Path to root from post page
            ))
        print(f"Generated post: {output_filepath}")

    # Read and convert about.md for the index page
    about_content = ""
    about_md_path = os.path.join(BASE_DIR, 'about.md')
    if os.path.exists(about_md_path):
        with open(about_md_path, 'r', encoding='utf-8') as f:
            about_content = md.render(f.read())
    else:
        print("Warning: about.md not found.")

    # Generate index page
    index_filepath = os.path.join(OUTPUT_DIR, 'index.html')
    with open(index_filepath, 'w', encoding='utf-8') as f:
        f.write(index_template.render(
            posts=posts_metadata,
            about_content=about_content,
            root_path='./' # Path to root from index page
        ))
    print(f"Generated index page: {index_filepath}")

if __name__ == '__main__':
    generate_site()

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
    """
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

    post_template = env.get_template('post.html')
    index_template = env.get_template('index.html')

    posts_metadata = []

    for md_file in os.listdir(PUBLISHED_DIR):
        if md_file.endswith('.md'):
            filepath = os.path.join(PUBLISHED_DIR, md_file)
            post_data = parse_markdown_file(filepath)
            
            html_content = md.render(post_data['content'])
            
            # post_data['date'] is already a datetime object
            post_date_obj = post_data['date']
            
            output_filename = md_file.replace('.md', '.html')
            output_filepath = os.path.join(OUTPUT_DIR, 'posts', output_filename)

            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(post_template.render(
                    title=post_data['title'],
                    date=post_data['date'].strftime('%Y-%m-%d'), # Format for display
                    content=html_content,
                    current_year=datetime.now().year
                ))
            print(f"Generated post: {output_filepath}")

            posts_metadata.append({
                'title': post_data['title'],
                'date': post_date_obj, # Store datetime object for sorting
                'url': f'posts/{output_filename}'
            })

    # Sort posts by date, newest first
    posts_metadata.sort(key=lambda x: x['date'], reverse=True)

    # Convert datetime objects back to string for rendering in index
    for post in posts_metadata:
        post['date'] = post['date'].strftime('%Y-%m-%d')

    # Generate index page
    index_filepath = os.path.join(OUTPUT_DIR, 'index.html')
    with open(index_filepath, 'w', encoding='utf-8') as f:
        f.write(index_template.render(posts=posts_metadata, current_year=datetime.now().year))
    print(f"Generated index page: {index_filepath}")

if __name__ == '__main__':
    generate_site()

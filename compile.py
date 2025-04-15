import markdown
import os
import re
from datetime import datetime

def extract_image_and_text(markdown_text):
    """
    Extracts the first image from the markdown and separates the rest.
    Returns (img_html, text_html)
    """
    img_pattern = r'!\[.*?\]\((.*?)\)'
    match = re.search(img_pattern, markdown_text)

    if not match:
        raise ValueError("Competition markdown must start with an image.")

    img_url = match.group(1)
    # Remove the image from the markdown
    text_md = re.sub(img_pattern, '', markdown_text, count=1).strip()

    # Convert markdown to HTML
    text_html = markdown.markdown(text_md, extensions=['extra', 'smarty'])

    img_html = f'<img src="{img_url}" alt="Competition Image">'
    return img_html, text_html

def compile_markdown(md_path, template_path, output_path, competitions_path):
    with open(md_path, 'r', encoding='utf-8') as md_file:
        main_content = markdown.markdown(md_file.read(), extensions=['extra', 'smarty'])

    competition_html = ""
    for comp_file in sorted(os.listdir(competitions_path)):
        if comp_file.endswith('.md'):
            with open(os.path.join(competitions_path, comp_file), 'r', encoding='utf-8') as f:
                comp_md = f.read()

            try:
                img_html, text_html = extract_image_and_text(comp_md)
                competition_html += f'''
                <div class="competition">
                    {img_html}
                    <div class="comp-text">
                        {text_html}
                    </div>
                </div>
                '''
            except ValueError as e:
                print(f"Skipping {comp_file}: {e}")

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template = template_file.read()

    final_html = (
        template.replace('{{content}}', main_content)
                .replace('{{portfolio}}', competition_html)
                .replace('{{last_updated}}', datetime.now().strftime("%Y-%m-%d"))
    )

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_html)

if __name__ == "__main__":
    compile_markdown('index.md', 'template.html', 'index.html', 'competitions')

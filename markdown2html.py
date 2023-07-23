import sys
import os
import markdown
import hashlib

def convert_markdown_to_html(md_file, output_file):
    if not os.path.exists(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    with open(md_file, 'r') as md:
        content = md.read()

    # Parse bold syntax and replace with HTML tags
    content = content.replace('**', '<b>', 1).replace('**', '</b>', 1)
    content = content.replace('__', '<em>', 1).replace('__', '</em>', 1)

    # Parse MD5 syntax and replace with MD5 hash (lowercase) if it exists
    if '[[' in content and ']]' in content:
        md5_parts = content.split('[[', 1)[1].split(']]', 1)
        md5_content = md5_parts[0]
        md5_hash = hashlib.md5(md5_content.encode()).hexdigest()
        content = content.replace("[[" + md5_content + "]]", md5_hash)

    # Parse content removal syntax and remove characters (case insensitive)
    content_parts = content.split('((')
    for i in range(1, len(content_parts)):
        remove_parts = content_parts[i].split('))', 1)
        content_to_remove = remove_parts[0]
        content_to_remove = content_to_remove.replace('c', '').replace('C', '')
        content_parts[i] = content_to_remove + remove_parts[1]
    content = "(".join(content_parts)

    # Parse paragraphs and replace with HTML tags
    paragraphs = content.split("\n\n")
    content = "\n".join(["<p>\n    " + p.replace('\n', '<br />\n    ') + "\n</p>" for p in paragraphs])

    # Parse ordered listing and replace with HTML tags
    content = content.replace("\n* ", "\n<li>")
    content = "<ol>\n<li>" + content + "\n</li>\n</ol>"

    # Parse unordered listing and replace with HTML tags
    content = content.replace("\n- ", "\n<li>")
    content = "<ul>\n<li>" + content + "\n</li>\n</ul>"

    html = markdown.markdown(content)

    # Parse headings and replace with HTML tags
    for level in range(1, 7):
        html = html.replace(f"<h{level}>", f"<h{level+1}>")

    with open(output_file, 'w') as html_file:
        html_file.write(html)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <Markdown_file> <Output_file>", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(md_file, output_file)

    sys.exit(0)


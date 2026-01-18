# 1. Iterate through all files inside the posts directory

# 2. For each HTML file, build an object for it, the object should
# contains the following properties:
#   a. the file name
#   b. the title
#   c. the creation time stamp, obtaining from the file name

# 3. For each objects, generate a HTML list entry with the following
# template:

# <li>[creation time stamp]<a href="[posts/filename.html]">[title]</a></li>

# 4. Then, these list entries should be put into the unordered list
# under the headline "All Posts" in index.html
import os
import re
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

script_dir = Path(__file__).parent.resolve()
os.chdir(script_dir)

posts_dir = Path('../posts/')

@dataclass
class Post:
    filename: str
    title: str
    create_time: object

posts: list[Post] = []

for file in posts_dir.iterdir():
    if file.is_file() and file.name.endswith("html"):
        with open(file, 'r', encoding='utf-8') as post:
            for line in post:
                match = re.search(r"<title>(.*?)</title>", line)
                if match:
                    title = match.group(1)
                    date = datetime.strptime(file.stem, "%Y%m%d%H%M%S").date()
                    p = Post(file.name, title, date)
                    posts.append(p)
                    break

posts.reverse()

html_list = ""

for post in posts:
    html_list += f"<li>{post.create_time} <a href=\"posts/{post.filename}\">{post.title}</a></li>\n"

with open("../index.html", "r", encoding="utf-8") as file:
    content = file.read()
    # NOTE: this step works depends on the existing structure of the
    # index file. Maybe I should write another script that generate
    # the whole index file.
    update = re.sub(r"(<h1> All Posts </h1>\n\s*<ul>\n).*?(</ul>\n)",
                   r"\1" + html_list + r"\2",
                   content,
                   flags = re.DOTALL)

with open("../index.html", "w", encoding="utf-8") as file:
    file.write(update)

print("All posts list updated!")

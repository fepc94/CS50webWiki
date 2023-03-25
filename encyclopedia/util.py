import re
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def save_to_disk(title, content):
    """
    Saves a new entry into the entries directory as a markdown file.
    """

    filename = os.path.join('entries' , f"{title}.md")
    with open(filename, 'w') as file:
        file.write(f"# {title}\n\n")
        file.write(content)

def retrieve_entry(title):
    """
    Retrieves the actual content to the form before editing it.
    """
    try:
        entry_path = os.path.join('entries', f"{title}.md")
        with open(entry_path, "r") as file:
            content = file.read()
            return content 
    except FileNotFoundError():
        return None

def update_entry(title, updated_title, updated_content):
    """ 
    Updates the entry once edited. 
    """
    old_entry_path = os.path.join('entries', f"{title}.md")
    new_entry_path = os.path.join('entries', f"{updated_title}.md")
    if os.path.exists(old_entry_path):
        os.rename(old_entry_path, new_entry_path)
        with open(new_entry_path, "w") as file:
            file.write(updated_content)
    return None
        
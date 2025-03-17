from pybtex.database import parse_file
from config import BIBTEX_FILE

def load_references():
    return parse_file(BIBTEX_FILE)

def format_citation(key, bib_data):
    entry = bib_data.entries[key]
    return f"({entry.persons['author'][0].last()}, {entry.fields['year']})"

if __name__ == "__main__":
    bib_data = load_references()
    print(format_citation("Smith2022", bib_data))

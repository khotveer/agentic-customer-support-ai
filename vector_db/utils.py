# vector_db/utils.py

import re
import pickle


def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def chunk_text_by_size(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
        if start < 0:
            start = 0

    return chunks


def get_sections(full_text: str):
    SECTION_PATTERN = re.compile(
        r"\n(?P<section_no>\d{1,2})\.\s+(?P<title>[A-Z][A-Za-z &/,()-]+)\n"
    )

    sections = []
    matches = list(SECTION_PATTERN.finditer(full_text))

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        section_text = full_text[start:end].strip()

        sections.append({
            "section_number": match.group("section_no"),
            "section_title": match.group("title").strip(),
            "content": section_text,
        })

    return sections


def save_pickle(filename, data):
    with open(filename, "wb") as f:
        pickle.dump(data, f)
    return filename


def load_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)
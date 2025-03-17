from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

prompt_template = """
You are an AI assistant specialized in extracting structured information from academic articles. 
Analyze the provided text and summarize it in this structured format:

**Title**:  
**Authors**:  
**Year**:  
**Research Question**:  
**Methodology**:  
**Main Findings**:  
**Limitations**:  
**Relevance to the topic**:  

Ensure clarity, accuracy, and conciseness. Do not add personal opinions or omit key details.
"""

def extract_relevant_sections(text):
    """
    Extracts only the most relevant sections from the text.
    - Stops when the next major section appears.
    - Prevents extracting unrelated content (e.g., acknowledgments, references).
    """
    sections = ["abstract", "introduction", "methodology", "conclusion", "summary"]
    extracted = []
    lines = text.split("\n")

    capturing = False
    for line in lines:
        clean_line = line.strip().lower()

        if any(sec in clean_line for sec in sections):
            capturing = True  # Start capturing when a section is found
            extracted.append(line)  # Include the section title
            continue

        if capturing:
            # Stop capturing if we hit a new major section
            if any(sec in clean_line for sec in sections) and line not in extracted:
                capturing = False
                continue

            extracted.append(line)

    return "\n".join(extracted)

def split_text(text, max_tokens=4000):
    """
    Splits text into smaller chunks that fit within OpenAI's token limit.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def extract_key_info(article_text):
    """
    Uses OpenAI API to extract structured information from a research article.
    - Splits text if it's too long to avoid exceeding token limits.
    """
    relevant_text = extract_relevant_sections(article_text)
    text_chunks = split_text(relevant_text, max_tokens=4000)

    summaries = []
    for chunk in text_chunks:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_template + chunk}]
        )

        # ✅ Correct way to access the response
        response_text = response.choices[0].message.content  # <-- FIXED
        summaries.append(response_text)

    return "\n\n".join(summaries)


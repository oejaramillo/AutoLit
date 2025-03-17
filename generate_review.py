from openai import OpenAI
from config import OPENAI_API_KEY, OUTPUT_FOLDER
import os

client = OpenAI(api_key=OPENAI_API_KEY)

academic_prompt = """
You are a highly skilled research assistant tasked with writing a comprehensive academic literature review on **[TOPIC]**. Your objective is to synthesize structured summaries from relevant academic articles into a well-organized, coherent, and critical literature review.

Your literature review should follow this structured format:

1. **Introduction**  
   - Provide context and background on **[TOPIC]**.  
   - Explain its significance in the field and any key debates or issues.  
   - Define the scope of the review and outline the main themes discussed.

2. **Thematic Sections**  
   - Organize research findings into logical themes, subtopics, or chronological trends.  
   - Compare and contrast different studies, highlighting similarities and differences.  
   - Provide citations using the format **(Author, Year)**.

3. **Critical Analysis**  
   - Evaluate the strengths, limitations, and methodologies of the reviewed studies.  
   - Discuss any conflicting findings, theoretical perspectives, or methodological approaches.  
   - Highlight ongoing academic debates and divergent viewpoints.

4. **Gaps in Research**  
   - Identify missing aspects, underexplored areas, or limitations in the existing literature.  
   - Suggest potential research questions that remain unanswered.  
   - Emphasize why these gaps matter and how they impact the field.

5. **Conclusion**  
   - Summarize key findings from the literature.  
   - Discuss the broader implications of the research.  
   - Propose future research directions based on identified gaps.

### Additional Requirements:
- Use a formal **academic tone** with precise and clear language.  
- Ensure a logically structured argument with smooth transitions between sections.  
- Properly incorporate citations in the **(Author, Year)** format.  
- Avoid personal opinions—base all claims on scholarly evidence.  

Deliver a **well-structured, cohesive, and insightful** literature review that contributes meaningfully to the understanding of **[TOPIC]**.
"""

def split_text(text, max_tokens=4000):
    """
    Divide un texto en fragmentos menores al límite de tokens.
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

def generate_literature_review(summaries_text):
    """
    Generates the literature review in parts to avoid exceeding the token limit.
    """
    text_chunks = split_text(summaries_text, max_tokens=4000)  # Split into smaller parts
    review_parts = []

    for chunk in text_chunks:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": academic_prompt + chunk}]
        )

        # ✅ Corrected response parsing
        review_parts.append(response.choices[0].message.content)  # Fixed

    return "\n\n".join(review_parts)  # Merge all review parts into one document


def save_review(text):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    with open(os.path.join(OUTPUT_FOLDER, "literature_review.md"), "w", encoding="utf-8") as f:
        f.write(text)

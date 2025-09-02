import os

from openai import OpenAI
from openai.types.chat import ChatCompletion

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

with open("README.md", "r") as f:
    readme_content: str = f.read()

languages: list[str] = ["mandarin chinese", "spanish", "hindi", "russian", "bengali"]

for lang in languages:
    response: ChatCompletion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"""You are a skilled translator. Your task is to convert the following markdown file into {lang} while following these strict instructions:

1. Preserve the EXACT markdown layout and formatting:
   - Keep all headers (#, ##, ###) unchanged in level
   - Preserve all code blocks (```) and their language tags
   - Do not modify any links [text](url)
   - Maintain lists (ordered/unordered) and indentation exactly
   - Keep all tables with their same column/row structure
   - Do not alter inline code (`code`)
   - Keep blockquotes (>) intact
   - Preserve horizontal rules (---)

2. Translation rules:
   - Translate only the written content, not the markdown symbols
   - Leave URLs untouched
   - Keep code examples exactly as they are
   - Retain technical terms in English if commonly used in {lang}
   - Match line breaks and paragraph spacing to the original
   - Do not add, remove, or rearrange any sections
   - Never alter the structure of the document

3. Output requirements:
   - Return ONLY the translated markdown
   - Do not include commentary or notes
   - Ensure the final output is valid markdown and renders identically to the original""",
            },
            {"role": "user", "content": readme_content},
        ],
    )

    translated_content: str = response.choices[0].message.content

    with open(f"docs/readmes/{lang}.md", "w") as f:
        _ = f.write(translated_content)

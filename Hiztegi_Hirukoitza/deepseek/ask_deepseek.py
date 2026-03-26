from config_private import ds_api_key
import os
import re
from openai import OpenAI

output_path = None

# Initialize the client
client = OpenAI(
    api_key=ds_api_key,
    base_url="https://api.deepseek.com"
)


def split_into_chunks(content, chunk_size=100):
    """
    Split the dictionary content into chunks by entries.
    Each chunk will contain approximately chunk_size entries.
    """
    # Split by entry pattern {{sarrera|...}}
    entries = re.split(r'(?={{sarrera\|)', content)

    # Remove any empty strings
    entries = [e for e in entries if e.strip()]

    # Group entries into chunks
    chunks = []
    for i in range(0, len(entries), chunk_size):
        chunk = ''.join(entries[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def process_chunk(chunk, chunk_num, total_chunks):
    """Process a single chunk with the API."""
    with open('training_set.txt') as f:
        training_chunk = f.read()
    global output_path

    prompt = f"""You are processing a historical Spanish-Basque-Latin dictionary (circa 1745) in wikitext format. This is chunk {chunk_num} of {total_chunks}.

Your task is to transform each dictionary entry by:

1. **Joining hyphenated words**: Remove end-of-line hyphens and join the broken words (e.g., "macha-" followed on next line by "tu" becomes "machatu").

2. **Applying XML tags** to specific content within each entry:
   - `<head>`: The Spanish headword(s) at the beginning of the entry. This is the word or phrase that appears immediately after the {{sarrera|...}} template, up to the first comma or colon that begins the definition.
   - `<xref>`: Cross-references to other Spanish entries. These appear in very short entries, together with phrases like "vease [word]" or "lo mismo que [word]". The cross-referenced Spanish words should be tagged as <xref> individually.
   - `<def>`: The Spanish definition or explanatory text, excluding the headword, and the final Basque/Latin equivalents. Many entries do not contain any definition text.
   - `<note>`: Some entries contain a long note appendix preceded by the word "NOTA.". This appendix will be enclosed in <note>.
   - `<eu>`: Basque translation equivalents (in italics, marked with single quotes like ''word'').
   - `<la>`: Latin translation equivalents (preceded by "Lat." or "L.").

3. **Punctuation placement**: Keep punctuation marks outside the XML tags except when part of the tagged content.

4. **Preserve all other formatting**: Keep the {{sarrera|...}} templates and any `<es>` tags already present.

In the following a chunk of the dictionary with annotations, as training set for the task, and the chunk to process.

Here is the training chunk:

{training_chunk}

Here is the chunk to process:

{chunk}

Output only the processed text for this chunk with no additional commentary."""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "You are a meticulous historical dictionary processor. Output only the processed text with no additional commentary."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=8192  # Maximum allowed
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing chunk {chunk_num}: {e}")
        return None


def process_dictionary_fragment(file_path, entries_per_chunk=50):
    """Process the dictionary file in chunks."""

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into chunks
    chunks = split_into_chunks(content, entries_per_chunk)
    total_chunks = len(chunks)
    print(f"Split into {total_chunks} chunks (approximately {entries_per_chunk} entries each)")

    # Process each chunk
    processed_chunks = []
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}/{total_chunks}...")

        # Check chunk size
        chunk_tokens = len(chunk) // 4  # Rough estimate
        print(f"  Chunk size: ~{chunk_tokens} tokens")

        result = process_chunk(chunk, i, total_chunks)
        if result:
            processed_chunks.append(result)
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(result)
        else:
            print(f"  Warning: Chunk {i} failed, skipping...")

    # Combine results
    return '\n'.join(processed_chunks)


def main():
    # Configuration
    global output_path
    file_path = "wikisource_text_source.txt"  # Path to your input file
    output_path = "processed_output.xml"  # Path for the output file

    # Adjust this based on your file size
    entries_per_chunk = 30  # Start with 30 entries per chunk

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Get total entries count for reference
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    entries_count = len(re.findall(r'{{sarrera\|', content))
    print(f"Total entries found: {entries_count}")

    # Estimate chunks needed
    estimated_chunks = (entries_count + entries_per_chunk - 1) // entries_per_chunk
    print(f"Estimated chunks: {estimated_chunks}")

    # Process the file
    print(f"\nProcessing {file_path}...")
    try:
        result = process_dictionary_fragment(file_path, entries_per_chunk)

        if result:
            # Save the result
            # with open(output_path, 'w', encoding='utf-8') as f:
            #     f.write(result)

            print(f"\nProcessing complete. Output saved to {output_path}")
            print(f"Output size: {len(result)} characters")

            # Preview first 500 characters
            print("\n--- Preview ---")
            print(result[:500] + "...\n")
        else:
            print("No output generated.")

    except Exception as e:
        print(f"Error during processing: {e}")


if __name__ == "__main__":
    main()
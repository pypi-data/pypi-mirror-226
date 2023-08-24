import os
import faiss
import time
from dotenv import load_dotenv

from llmutils import AOAIChat, AOAIEmbedding
from llmutils import FAISSIndex

CHUNK_SIZE = 512 * 5 # in character count, since English word has 4.7 characters on average this is about 256 words
CHUNK_OVERLAP = 16 * 5 # about 16 words
MAX_TOKENS_FOR_SUMMARIZATION_BEFORE_EMBEDDING = 128

def combine_reviews(directory):
    # Create an empty list to store the contents of each text file
    file_contents = []

    # Loop through each file in the directory tree
    for root, _, files in os.walk(directory):
        for filename in files:
            # Check if the file is a text file
            if filename.endswith('.txt'):
                # Open the file and read its contents
                with open(os.path.join(root, filename), 'r') as file:
                    file_contents.append(file.read())

    # Combine the contents of all text files into a single string
    return ''.join(file_contents)

def build_index(text: str, output_directory: str, max_chunk: int = None):
    chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

    print(f"Number of chunks: {len(chunks)}")

    chat = AOAIChat()
    index = FAISSIndex(index=faiss.IndexFlatL2(1536), embedding=AOAIEmbedding())

    # Summarize chunks with English
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i}... ")
        start = time.time()
        try:
            summary = chat.generate(messages=[
                {"role": "user", "content": "Please summarize the paragraph with a few sentences to capture the key points."},
                {"role": "user", "content": chunk}], 
                max_tokens=MAX_TOKENS_FOR_SUMMARIZATION_BEFORE_EMBEDDING)
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
            continue

        # print("\033[92m" + summary + "\033[0m")
        end = time.time()
        print(f"\033[92m {end-start} seconds\033[0m")
        translated_chunks.append(summary)
        if max_chunk is not None and i >= max_chunk:
            break

    index.insert_batch(translated_chunks)
    index.save(output_directory)

# Split the text into chunks with CHUNK_SIZE and CHUNK_OVERLAP as character count
def split_text(text, chunk_size, chunk_overlap):
    # Calculate the number of chunks
    num_chunks = (len(text) - chunk_overlap) // (chunk_size - chunk_overlap)

    # Split the text into chunks
    chunks = []
    for i in range(num_chunks):
        start = i * (chunk_size - chunk_overlap)
        end = start + chunk_size
        chunks.append(text[start:end])

    # Add the last chunk
    chunks.append(text[num_chunks * (chunk_size - chunk_overlap):])

    return chunks

if __name__ == '__main__':
    load_dotenv()

    directory = '../../data/steam-reviews/some-game'
    text = combine_reviews(directory)
    build_index(text, directory, max_chunk=1000)
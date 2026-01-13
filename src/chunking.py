def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    """
    Splits text into overlapping chunks.

    :param text: Full document text
    :param chunk_size: Max characters per chunk
    :param overlap: Number of characters shared between chunks
    :return: List of text chunks
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap
        if start < 0:
            start = 0

    return chunks

def create_chunk_objects(chunks, source: str):
    """
    Converts raw text chunks into structured chunk objects.

    :param chunks: List of text chunks
    :param source: Document identifier or filename
    :return: List of chunk dictionaries
    """

    chunk_objects = []

    for index, chunk in enumerate(chunks):
        chunk_obj = {
            "chunk_id": f"{source}_{index:04d}",
            "text": chunk,
            "source": source,
            "chunk_index": index
        }
        chunk_objects.append(chunk_obj)

    return chunk_objects


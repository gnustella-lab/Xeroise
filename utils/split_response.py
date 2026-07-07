def split_response(response, max_length=1900):
    lines = response.splitlines()
    chunks = []
    current_chunk = ""
    for line in lines:
        # If a single line is longer than max_length, split it into pieces.
        if len(line) > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            for i in range(0, len(line), max_length):
                chunks.append(line[i:i + max_length].strip())
            continue

        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            current_chunk += "\n" + line if current_chunk else line
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

import re

def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if not text or not text.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    # Separar en bloques lógicos por múltiples saltos de línea (párrafos/ecuaciones)
    blocks = [b.strip() for b in re.split(r'\n\s*\n', text) if b.strip()]
    
    if not blocks:
        return []

    chunks: list[str] = []
    current_chunk_blocks: list[str] = []
    current_length = 0
    
    i = 0
    while i < len(blocks):
        block = blocks[i]
        block_len = len(block)
        
        # Si un solo bloque excede el chunk_size, forzar fragmentación estricta (fallback)
        if block_len > chunk_size:
            if current_chunk_blocks:
                chunks.append("\n\n".join(current_chunk_blocks))
                current_chunk_blocks = []
                current_length = 0
                
            start = 0
            step = chunk_size - chunk_overlap
            while start < block_len:
                piece = block[start : start + chunk_size].strip()
                if piece:
                    chunks.append(piece)
                start += step
            i += 1
            continue
            
        separator_len = 2 if current_length > 0 else 0
        
        # Si agregar este bloque excede el tamaño máximo permitido
        if current_length + block_len + separator_len > chunk_size and current_chunk_blocks:
            chunks.append("\n\n".join(current_chunk_blocks))
            
            # Preparar el siguiente chunk calculando el overlap por bloques
            overlap_length = 0
            overlap_blocks = []
            
            for b in reversed(current_chunk_blocks):
                sep_len = 2 if overlap_length > 0 else 0
                if overlap_length + len(b) + sep_len > chunk_overlap:
                    break
                # Prevenir bucle infinito asegurando que el chunk avance
                if len(overlap_blocks) + 1 == len(current_chunk_blocks):
                    break
                overlap_blocks.insert(0, b)
                overlap_length += len(b) + sep_len
                
            current_chunk_blocks = overlap_blocks
            current_length = overlap_length
        else:
            current_chunk_blocks.append(block)
            current_length += block_len + separator_len
            i += 1

    if current_chunk_blocks:
        chunks.append("\n\n".join(current_chunk_blocks))
        
    return chunks

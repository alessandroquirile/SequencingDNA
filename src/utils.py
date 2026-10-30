def get_kmers(sequence: str, k: int = 6) -> str:
    """Extract overlapping k-mers of length k, filtering out any with non-canonical bases."""
    valid_bases = {'A', 'T', 'C', 'G'}
    seq = sequence.upper()
    kmers = [
        seq[i:i + k]
        for i in range(len(seq) - k + 1)
        if set(seq[i:i + k]).issubset(valid_bases)
    ]
    return ' '.join(kmers)

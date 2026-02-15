#!/usr/bin/env python3
"""DNA sequence analysis script.

Analyzes FASTA-format DNA sequences and reports:
- Nucleotide composition (A, T, G, C counts and percentages)
- GC content
- Sequence length
- Codon usage
- CpG island detection
- Open reading frame (ORF) identification
"""

import os
import sys
from collections import Counter


def parse_fasta(filepath):
    """Parse a FASTA file and return a dict of {header: sequence}."""
    sequences = {}
    current_header = None
    current_seq = []

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_header is not None:
                    sequences[current_header] = "".join(current_seq)
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line.upper())

    if current_header is not None:
        sequences[current_header] = "".join(current_seq)

    return sequences


def nucleotide_composition(seq):
    """Return nucleotide counts and percentages."""
    counts = Counter(seq)
    total = len(seq)
    composition = {}
    for base in "ATGC":
        count = counts.get(base, 0)
        pct = (count / total * 100) if total > 0 else 0
        composition[base] = {"count": count, "percent": round(pct, 2)}
    return composition


def gc_content(seq):
    """Calculate GC content as a percentage."""
    if not seq:
        return 0.0
    gc = sum(1 for base in seq if base in "GC")
    return round(gc / len(seq) * 100, 2)


def codon_usage(seq):
    """Count codon frequencies from the reading frame starting at position 0."""
    codons = [seq[i:i+3] for i in range(0, len(seq) - 2, 3)]
    return Counter(codons)


CODON_TABLE = {
    "TTT": "Phe", "TTC": "Phe", "TTA": "Leu", "TTG": "Leu",
    "CTT": "Leu", "CTC": "Leu", "CTA": "Leu", "CTG": "Leu",
    "ATT": "Ile", "ATC": "Ile", "ATA": "Ile", "ATG": "Met",
    "GTT": "Val", "GTC": "Val", "GTA": "Val", "GTG": "Val",
    "TCT": "Ser", "TCC": "Ser", "TCA": "Ser", "TCG": "Ser",
    "CCT": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "ACT": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "GCT": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "TAT": "Tyr", "TAC": "Tyr", "TAA": "***", "TAG": "***",
    "CAT": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "AAT": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
    "GAT": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "TGT": "Cys", "TGC": "Cys", "TGA": "***", "TGG": "Trp",
    "CGT": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "AGT": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
    "GGT": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
}

STOP_CODONS = {"TAA", "TAG", "TGA"}


def find_orfs(seq, min_length=30):
    """Find open reading frames (start codon ATG to stop codon) in all 3 frames."""
    orfs = []
    for frame in range(3):
        i = frame
        while i < len(seq) - 2:
            codon = seq[i:i+3]
            if codon == "ATG":
                start = i
                j = i + 3
                while j < len(seq) - 2:
                    c = seq[j:j+3]
                    if c in STOP_CODONS:
                        length = j + 3 - start
                        if length >= min_length:
                            orfs.append({
                                "frame": frame + 1,
                                "start": start + 1,
                                "end": j + 3,
                                "length_nt": length,
                                "length_aa": length // 3 - 1,
                            })
                        i = j + 3
                        break
                    j += 3
                else:
                    # No stop codon found — partial ORF
                    length = len(seq) - start
                    if length >= min_length:
                        orfs.append({
                            "frame": frame + 1,
                            "start": start + 1,
                            "end": len(seq),
                            "length_nt": length,
                            "length_aa": length // 3,
                            "partial": True,
                        })
                    break
                continue
            i += 3
    return orfs


def detect_cpg_islands(seq, window=200, step=50, gc_thresh=50, obs_exp_thresh=0.6):
    """Detect CpG islands using a sliding window approach."""
    islands = []
    for start in range(0, len(seq) - window + 1, step):
        segment = seq[start:start + window]
        gc = sum(1 for b in segment if b in "GC") / len(segment) * 100
        c_count = segment.count("C")
        g_count = segment.count("G")
        cg_count = sum(1 for i in range(len(segment) - 1) if segment[i:i+2] == "CG")
        expected = (c_count * g_count) / len(segment) if len(segment) > 0 else 0
        obs_exp = cg_count / expected if expected > 0 else 0

        if gc >= gc_thresh and obs_exp >= obs_exp_thresh:
            islands.append({
                "start": start + 1,
                "end": start + window,
                "gc_percent": round(gc, 2),
                "obs_exp_cpg": round(obs_exp, 2),
            })

    # Merge overlapping islands
    if not islands:
        return []
    merged = [islands[0]]
    for island in islands[1:]:
        if island["start"] <= merged[-1]["end"]:
            merged[-1]["end"] = max(merged[-1]["end"], island["end"])
            merged[-1]["gc_percent"] = max(merged[-1]["gc_percent"], island["gc_percent"])
            merged[-1]["obs_exp_cpg"] = max(merged[-1]["obs_exp_cpg"], island["obs_exp_cpg"])
        else:
            merged.append(island)
    return merged


def translate(seq):
    """Translate a DNA sequence to amino acids (single reading frame)."""
    protein = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        aa = CODON_TABLE.get(codon, "?")
        if aa == "***":
            break
        protein.append(aa)
    return "-".join(protein)


def dinucleotide_freq(seq):
    """Calculate dinucleotide frequencies."""
    dinucs = [seq[i:i+2] for i in range(len(seq) - 1)]
    counts = Counter(dinucs)
    total = len(dinucs)
    freq = {}
    for dinuc, count in sorted(counts.items()):
        freq[dinuc] = round(count / total * 100, 2)
    return freq


def analyze_sequence(header, seq):
    """Run all analyses on a single sequence."""
    print(f"\n{'='*70}")
    print(f"  {header}")
    print(f"{'='*70}")

    # Basic stats
    print(f"\n  Sequence Length: {len(seq)} bp")

    # Nucleotide composition
    comp = nucleotide_composition(seq)
    print("\n  Nucleotide Composition:")
    print(f"    {'Base':<6} {'Count':>8} {'Percent':>10}")
    print(f"    {'-'*28}")
    for base in "ATGC":
        c = comp[base]
        bar = "#" * int(c["percent"] / 2)
        print(f"    {base:<6} {c['count']:>8} {c['percent']:>9}%  {bar}")

    # GC content
    gc = gc_content(seq)
    print(f"\n  GC Content: {gc}%")
    if gc > 60:
        print("    -> HIGH GC content (may indicate CpG islands or thermophilic origin)")
    elif gc < 40:
        print("    -> LOW GC content (AT-rich region)")
    else:
        print("    -> Moderate GC content")

    # AT/GC ratio
    at = comp["A"]["count"] + comp["T"]["count"]
    gc_count = comp["G"]["count"] + comp["C"]["count"]
    ratio = round(at / gc_count, 3) if gc_count > 0 else float("inf")
    print(f"  AT/GC Ratio: {ratio}")

    # Codon usage (top 10)
    codons = codon_usage(seq)
    print("\n  Top 10 Codons:")
    print(f"    {'Codon':<8} {'AA':<6} {'Count':>6} {'Freq%':>8}")
    print(f"    {'-'*32}")
    total_codons = sum(codons.values())
    for codon, count in codons.most_common(10):
        aa = CODON_TABLE.get(codon, "?")
        freq = round(count / total_codons * 100, 2)
        print(f"    {codon:<8} {aa:<6} {count:>6} {freq:>7}%")

    # ORFs
    orfs = find_orfs(seq)
    print(f"\n  Open Reading Frames (ORFs >= 30 nt): {len(orfs)} found")
    for i, orf in enumerate(orfs[:5], 1):
        partial = " (partial - no stop codon)" if orf.get("partial") else ""
        print(f"    ORF {i}: Frame +{orf['frame']}, pos {orf['start']}-{orf['end']}, "
              f"{orf['length_nt']} nt / {orf['length_aa']} aa{partial}")

    # CpG islands
    islands = detect_cpg_islands(seq)
    print(f"\n  CpG Islands Detected: {len(islands)}")
    for i, island in enumerate(islands, 1):
        print(f"    Island {i}: pos {island['start']}-{island['end']}, "
              f"GC={island['gc_percent']}%, Obs/Exp CpG={island['obs_exp_cpg']}")

    # First 10 amino acids
    protein = translate(seq)
    aas = protein.split("-")
    preview = "-".join(aas[:15]) + ("..." if len(aas) > 15 else "")
    print(f"\n  Protein Preview (first 15 AA): {preview}")

    return {
        "length": len(seq),
        "gc_content": gc,
        "composition": comp,
        "orf_count": len(orfs),
        "cpg_islands": len(islands),
    }


def comparative_summary(results):
    """Print a comparative summary across all sequences."""
    print(f"\n\n{'='*70}")
    print("  COMPARATIVE SUMMARY")
    print(f"{'='*70}")

    # Summary table
    print(f"\n  {'Gene':<20} {'Length':>8} {'GC%':>8} {'ORFs':>6} {'CpG':>6}")
    print(f"  {'-'*52}")
    for name, stats in sorted(results.items(), key=lambda x: x[1]["gc_content"], reverse=True):
        short_name = name.split()[0]
        print(f"  {short_name:<20} {stats['length']:>8} {stats['gc_content']:>7}% {stats['orf_count']:>6} {stats['cpg_islands']:>6}")

    # Highest/lowest GC
    highest_gc = max(results.items(), key=lambda x: x[1]["gc_content"])
    lowest_gc = min(results.items(), key=lambda x: x[1]["gc_content"])
    longest = max(results.items(), key=lambda x: x[1]["length"])
    shortest = min(results.items(), key=lambda x: x[1]["length"])

    print(f"\n  Highest GC Content: {highest_gc[0].split()[0]} ({highest_gc[1]['gc_content']}%)")
    print(f"  Lowest GC Content:  {lowest_gc[0].split()[0]} ({lowest_gc[1]['gc_content']}%)")
    print(f"  Longest Sequence:   {longest[0].split()[0]} ({longest[1]['length']} bp)")
    print(f"  Shortest Sequence:  {shortest[0].split()[0]} ({shortest[1]['length']} bp)")

    avg_gc = round(sum(s["gc_content"] for s in results.values()) / len(results), 2)
    avg_len = round(sum(s["length"] for s in results.values()) / len(results), 1)
    print(f"\n  Average GC Content: {avg_gc}%")
    print(f"  Average Length:     {avg_len} bp")
    print(f"  Total Sequences:    {len(results)}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fasta_file = os.path.join(script_dir, "sample_sequences.fasta")

    if not os.path.exists(fasta_file):
        print(f"Error: FASTA file not found at {fasta_file}")
        sys.exit(1)

    print("=" * 70)
    print("  DNA SEQUENCE ANALYSIS REPORT")
    print(f"  Input: {os.path.basename(fasta_file)}")
    print("=" * 70)

    sequences = parse_fasta(fasta_file)
    print(f"\n  Loaded {len(sequences)} sequences from FASTA file.")

    results = {}
    for header, seq in sequences.items():
        results[header] = analyze_sequence(header, seq)

    comparative_summary(results)
    print()


if __name__ == "__main__":
    main()

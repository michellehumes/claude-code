#!/usr/bin/env python3
"""Family genetic inheritance analysis.

Compares two parent DNA profiles and predicts trait probabilities
for their children using Mendelian genetics, incomplete dominance,
codominance, and X-linked inheritance models.
"""

import json
import os

DIVIDER = "=" * 70
THIN_DIV = "-" * 70
SECTION = "-" * 50


def load_profile(filepath):
    with open(filepath) as f:
        return json.load(f)


def print_banner(text, char="=", width=70):
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}")


def print_parent_profile(profile):
    """Display a parent's full DNA profile."""
    name = profile["name"]
    print_banner(f"{name.upper()}'S DNA PROFILE", "=")

    print(f"\n  Name: {name}")
    print(f"  Sex:  {profile['sex']}")

    print(f"\n  {'TRAIT':<22} {'PHENOTYPE':<22} {'GENOTYPE':<12} {'TYPE'}")
    print(f"  {SECTION}")

    for trait_name, trait in profile["traits"].items():
        display = trait_name.replace("_", " ").title()
        geno = "/".join(trait["genotype"])
        a1, a2 = trait["genotype"]

        if a1 == a2:
            zygosity = "Homozygous"
        elif trait_name == "blood_type":
            zygosity = "Codominant" if a1 != "O" and a2 != "O" else "Heterozygous"
        else:
            zygosity = "Heterozygous"

        print(f"  {display:<22} {trait['phenotype']:<22} {geno:<12} {zygosity}")

    # Genetic markers
    markers = profile["genetic_markers"]
    print(f"\n  HEALTH MARKERS:")
    print(f"  {SECTION}")
    for marker, value in markers.items():
        if marker == "ancestry_composition":
            continue
        print(f"    {marker:<12} {value}")

    # Ancestry
    ancestry = markers["ancestry_composition"]
    print(f"\n  ANCESTRY COMPOSITION:")
    print(f"  {SECTION}")
    for region, pct in sorted(ancestry.items(), key=lambda x: -x[1]):
        bar = "#" * (pct // 2)
        print(f"    {region.replace('_', ' '):<20} {pct:>3}%  {bar}")


def punnett_simple(parent1_alleles, parent2_alleles):
    """Standard Punnett square for two alleles."""
    outcomes = []
    for a1 in parent1_alleles:
        for a2 in parent2_alleles:
            outcomes.append(tuple(sorted([a1, a2], key=lambda x: (x.lower(), x.islower()))))
    return outcomes


def analyze_eye_color(gray_geno, michelle_geno):
    """Eye color uses a simplified multi-gene model.
    B (brown) > G (green) > b (blue).
    """
    alleles_dad = gray_geno       # ["B", "b"]
    alleles_mom = michelle_geno   # ["G", "b"]

    combos = []
    for a1 in alleles_dad:
        for a2 in alleles_mom:
            combos.append((a1, a2))

    results = {"Brown": 0, "Green": 0, "Blue": 0, "Hazel": 0}
    for c in combos:
        if "B" in c and "G" in c:
            results["Hazel"] += 1  # B + G interaction
        elif "B" in c:
            results["Brown"] += 1
        elif "G" in c:
            results["Green"] += 1
        else:
            results["Blue"] += 1

    total = len(combos)
    return {k: round(v / total * 100) for k, v in results.items() if v > 0}


def analyze_hair_color(gray_geno, michelle_geno):
    """Hair color: B (dark) > b (light)."""
    combos = punnett_simple(gray_geno, michelle_geno)
    results = {"Dark Brown": 0, "Medium Brown": 0, "Light Brown/Blonde": 0}
    for c in combos:
        if c[0].isupper() and c[1].isupper():
            results["Dark Brown"] += 1
        elif c[0].isupper() or c[1].isupper():
            results["Medium Brown"] += 1
        else:
            results["Light Brown/Blonde"] += 1
    total = len(combos)
    return {k: round(v / total * 100) for k, v in results.items() if v > 0}


def analyze_hair_texture(gray_geno, michelle_geno):
    """Hair texture: C (curly) + s (straight) = wavy (incomplete dominance)."""
    combos = []
    for a1 in gray_geno:
        for a2 in michelle_geno:
            combos.append((a1, a2))

    results = {"Curly": 0, "Wavy": 0, "Straight": 0}
    for c in combos:
        if "C" in c and "s" in c:
            results["Wavy"] += 1
        elif "C" in c:
            results["Curly"] += 1
        else:
            results["Straight"] += 1

    total = len(combos)
    return {k: round(v / total * 100) for k, v in results.items() if v > 0}


def analyze_simple_dominant(gray_geno, michelle_geno, dominant_name, recessive_name):
    """For simple dominant/recessive traits (dimples, freckles, cleft chin, etc.)."""
    combos = []
    for a1 in gray_geno:
        for a2 in michelle_geno:
            combos.append((a1, a2))

    dom_count = 0
    rec_count = 0
    for c in combos:
        if any(a.isupper() for a in c):
            dom_count += 1
        else:
            rec_count += 1

    total = len(combos)
    results = {}
    if dom_count:
        results[dominant_name] = round(dom_count / total * 100)
    if rec_count:
        results[recessive_name] = round(rec_count / total * 100)
    return results


def analyze_blood_type(gray_geno, michelle_geno):
    """Blood type: A and B are codominant, both dominant over O."""
    combos = []
    for a1 in gray_geno:
        for a2 in michelle_geno:
            combos.append((a1, a2))

    results = {"Type A": 0, "Type B": 0, "Type AB": 0, "Type O": 0}
    for c in combos:
        alleles = set(c)
        if "A" in alleles and "B" in alleles:
            results["Type AB"] += 1
        elif "A" in alleles:
            results["Type A"] += 1
        elif "B" in alleles:
            results["Type B"] += 1
        else:
            results["Type O"] += 1

    total = len(combos)
    return {k: round(v / total * 100) for k, v in results.items() if v > 0}


def analyze_rh_factor(gray_geno, michelle_geno):
    """Rh factor: Rh+ dominant over Rh-."""
    combos = []
    for a1 in gray_geno:
        for a2 in michelle_geno:
            combos.append((a1, a2))

    pos = sum(1 for c in combos if "Rh+" in c)
    neg = len(combos) - pos
    total = len(combos)
    results = {}
    if pos:
        results["Rh Positive"] = round(pos / total * 100)
    if neg:
        results["Rh Negative"] = round(neg / total * 100)
    return results


def analyze_color_vision(gray_geno, michelle_geno):
    """X-linked color vision. Gray: XN/Y, Michelle: XN/Xn.
    Sons get X from mom, Y from dad. Daughters get X from each.
    """
    # Sons: 50% XN (normal), 50% Xn (color blind)
    # Daughters: 50% XN/XN (normal), 50% XN/Xn (carrier)
    return {
        "sons": {"Normal Vision": 50, "Color Blind": 50},
        "daughters": {"Normal Vision": 50, "Carrier (Normal Vision)": 50},
    }


def analyze_ancestry(gray_ancestry, michelle_ancestry):
    """Average parent ancestry for child estimate."""
    child = {}
    all_regions = set(gray_ancestry.keys()) | set(michelle_ancestry.keys())
    for region in all_regions:
        avg = (gray_ancestry.get(region, 0) + michelle_ancestry.get(region, 0)) / 2
        child[region] = round(avg, 1)
    return child


def analyze_health_markers(gray_markers, michelle_markers):
    """Analyze health marker inheritance risks."""
    results = []

    # CFTR - cystic fibrosis carrier analysis
    gray_cftr = gray_markers.get("CFTR", "Normal")
    michelle_cftr = michelle_markers.get("CFTR", "Normal")
    if "carrier" in gray_cftr.lower() and "carrier" in michelle_cftr.lower():
        results.append(("CFTR (Cystic Fibrosis)", "25% chance affected, 50% carrier, 25% clear", "ELEVATED"))
    elif "carrier" in gray_cftr.lower() or "carrier" in michelle_cftr.lower():
        results.append(("CFTR (Cystic Fibrosis)", "50% carrier, 50% clear, 0% affected", "LOW"))
    else:
        results.append(("CFTR (Cystic Fibrosis)", "Very low risk", "MINIMAL"))

    # APOE - Alzheimer's risk
    gray_apoe = gray_markers.get("APOE", "e3/e3")
    michelle_apoe = michelle_markers.get("APOE", "e3/e3")
    if "e4" in gray_apoe and "e4" in michelle_apoe:
        results.append(("APOE (Alzheimer's Risk)", "Elevated - both parents carry e4 variant", "ELEVATED"))
    elif "e4" in gray_apoe or "e4" in michelle_apoe:
        results.append(("APOE (Alzheimer's Risk)", "50% chance of inheriting one e4 allele", "MODERATE"))
    else:
        results.append(("APOE (Alzheimer's Risk)", "Low baseline risk - no e4 variants", "LOW"))

    # MTHFR
    gray_mthfr = gray_markers.get("MTHFR", "Normal")
    michelle_mthfr = michelle_markers.get("MTHFR", "Normal")
    if "heterozygous" in gray_mthfr.lower():
        results.append(("MTHFR (Folate Metabolism)", "50% chance of inheriting C677T variant from father", "LOW-MODERATE"))
    elif "heterozygous" in michelle_mthfr.lower():
        results.append(("MTHFR (Folate Metabolism)", "50% chance of inheriting variant from mother", "LOW-MODERATE"))
    else:
        results.append(("MTHFR (Folate Metabolism)", "Normal folate metabolism expected", "LOW"))

    # BRCA1
    results.append(("BRCA1 (Cancer Risk)", "Both parents normal - baseline population risk", "LOW"))

    return results


def print_punnett_grid(trait_name, dad_alleles, mom_alleles):
    """Print a visual Punnett square."""
    print(f"\n    Punnett Square for {trait_name}:")
    d1, d2 = dad_alleles
    m1, m2 = mom_alleles
    print(f"                  Mom")
    print(f"              {m1:^8} {m2:^8}")
    print(f"          +--------+--------+")
    print(f"    Dad {d1:>1} |  {d1+m1:^4}  |  {d1+m2:^4}  |")
    print(f"          +--------+--------+")
    print(f"        {d2:>1} |  {d2+m1:^4}  |  {d2+m2:^4}  |")
    print(f"          +--------+--------+")


def print_probability_bar(label, pct, width=30):
    """Print a horizontal bar showing probability."""
    filled = int(pct / 100 * width)
    bar = "#" * filled + "." * (width - filled)
    print(f"    {label:<28} [{bar}] {pct}%")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gray = load_profile(os.path.join(script_dir, "gray_profile.json"))
    michelle = load_profile(os.path.join(script_dir, "michelle_profile.json"))

    # =========================================================================
    # HEADER
    # =========================================================================
    print("\n" + DIVIDER)
    print("       FAMILY GENETIC INHERITANCE ANALYSIS")
    print("       Gray & Michelle -> Children Predictions")
    print(DIVIDER)

    # =========================================================================
    # PARENT PROFILES
    # =========================================================================
    print_parent_profile(gray)
    print_parent_profile(michelle)

    # =========================================================================
    # SIDE-BY-SIDE COMPARISON
    # =========================================================================
    print_banner("GRAY vs MICHELLE - TRAIT COMPARISON", "=")

    print(f"\n  {'TRAIT':<20} {'GRAY':<22} {'MICHELLE':<22}")
    print(f"  {SECTION}")
    for trait_name in gray["traits"]:
        display = trait_name.replace("_", " ").title()
        g_pheno = gray["traits"][trait_name]["phenotype"]
        m_pheno = michelle["traits"][trait_name]["phenotype"]
        match = " <--same" if g_pheno == m_pheno else ""
        print(f"  {display:<20} {g_pheno:<22} {m_pheno:<22}{match}")

    # =========================================================================
    # CHILDREN PREDICTIONS
    # =========================================================================
    print_banner("PREDICTED TRAITS FOR GRAY & MICHELLE'S CHILDREN", "*", 70)

    # --- Eye Color ---
    print(f"\n  EYE COLOR")
    print(f"  {SECTION}")
    print(f"  Gray: Brown (B/b) x Michelle: Green (G/b)")
    eye_results = analyze_eye_color(
        gray["traits"]["eye_color"]["genotype"],
        michelle["traits"]["eye_color"]["genotype"]
    )
    print_punnett_grid("Eye Color", ["B", "b"], ["G", "b"])
    print()
    for color, pct in sorted(eye_results.items(), key=lambda x: -x[1]):
        print_probability_bar(color, pct)

    # --- Hair Color ---
    print(f"\n\n  HAIR COLOR")
    print(f"  {SECTION}")
    print(f"  Gray: Dark Brown (B/b) x Michelle: Light Brown (b/b)")
    hair_results = analyze_hair_color(
        gray["traits"]["hair_color"]["genotype"],
        michelle["traits"]["hair_color"]["genotype"]
    )
    print_punnett_grid("Hair Color", ["B", "b"], ["b", "b"])
    print()
    for color, pct in sorted(hair_results.items(), key=lambda x: -x[1]):
        print_probability_bar(color, pct)

    # --- Hair Texture ---
    print(f"\n\n  HAIR TEXTURE (Incomplete Dominance)")
    print(f"  {SECTION}")
    print(f"  Gray: Straight (s/s) x Michelle: Wavy (C/s)")
    texture_results = analyze_hair_texture(
        gray["traits"]["hair_texture"]["genotype"],
        michelle["traits"]["hair_texture"]["genotype"]
    )
    print_punnett_grid("Hair Texture", ["s", "s"], ["C", "s"])
    print()
    for texture, pct in sorted(texture_results.items(), key=lambda x: -x[1]):
        print_probability_bar(texture, pct)

    # --- Dimples ---
    print(f"\n\n  DIMPLES")
    print(f"  {SECTION}")
    print(f"  Gray: Dimples (D/d) x Michelle: No Dimples (d/d)")
    dimple_results = analyze_simple_dominant(
        gray["traits"]["dimples"]["genotype"],
        michelle["traits"]["dimples"]["genotype"],
        "Dimples", "No Dimples"
    )
    print_punnett_grid("Dimples", ["D", "d"], ["d", "d"])
    print()
    for trait, pct in sorted(dimple_results.items(), key=lambda x: -x[1]):
        print_probability_bar(trait, pct)

    # --- Freckles ---
    print(f"\n\n  FRECKLES")
    print(f"  {SECTION}")
    print(f"  Gray: No Freckles (f/f) x Michelle: Freckles (F/f)")
    freckle_results = analyze_simple_dominant(
        gray["traits"]["freckles"]["genotype"],
        michelle["traits"]["freckles"]["genotype"],
        "Freckles", "No Freckles"
    )
    print_punnett_grid("Freckles", ["f", "f"], ["F", "f"])
    print()
    for trait, pct in sorted(freckle_results.items(), key=lambda x: -x[1]):
        print_probability_bar(trait, pct)

    # --- Cleft Chin ---
    print(f"\n\n  CLEFT CHIN")
    print(f"  {SECTION}")
    print(f"  Gray: Cleft Chin (C/c) x Michelle: Smooth Chin (c/c)")
    chin_results = analyze_simple_dominant(
        gray["traits"]["cleft_chin"]["genotype"],
        michelle["traits"]["cleft_chin"]["genotype"],
        "Cleft Chin", "Smooth Chin"
    )
    print_punnett_grid("Cleft Chin", ["C", "c"], ["c", "c"])
    print()
    for trait, pct in sorted(chin_results.items(), key=lambda x: -x[1]):
        print_probability_bar(trait, pct)

    # --- Widow's Peak ---
    print(f"\n\n  WIDOW'S PEAK")
    print(f"  {SECTION}")
    print(f"  Gray: Widow's Peak (W/w) x Michelle: Straight Hairline (w/w)")
    wp_results = analyze_simple_dominant(
        gray["traits"]["widow_peak"]["genotype"],
        michelle["traits"]["widow_peak"]["genotype"],
        "Widow's Peak", "Straight Hairline"
    )
    print_punnett_grid("Widow's Peak", ["W", "w"], ["w", "w"])
    print()
    for trait, pct in sorted(wp_results.items(), key=lambda x: -x[1]):
        print_probability_bar(trait, pct)

    # --- Earlobes ---
    print(f"\n\n  EARLOBE TYPE")
    print(f"  {SECTION}")
    print(f"  Gray: Free (E/e) x Michelle: Free (E/E)")
    ear_results = analyze_simple_dominant(
        gray["traits"]["earlobe_type"]["genotype"],
        michelle["traits"]["earlobe_type"]["genotype"],
        "Free (Detached)", "Attached"
    )
    print()
    for trait, pct in sorted(ear_results.items(), key=lambda x: -x[1]):
        print_probability_bar(trait, pct)

    # --- Tongue Rolling ---
    print(f"\n\n  TONGUE ROLLING")
    print(f"  {SECTION}")
    print(f"  Gray: Roller (R/r) x Michelle: Roller (R/R)")
    tongue_results = analyze_simple_dominant(
        gray["traits"]["tongue_rolling"]["genotype"],
        michelle["traits"]["tongue_rolling"]["genotype"],
        "Can Roll Tongue", "Cannot Roll Tongue"
    )
    print()
    for trait, pct in sorted(tongue_results.items(), key=lambda x: -x[1]):
        print_probability_bar(trait, pct)

    # --- Blood Type ---
    print(f"\n\n  BLOOD TYPE (Codominance)")
    print(f"  {SECTION}")
    print(f"  Gray: Type A (A/O) x Michelle: Type B (B/O)")
    blood_results = analyze_blood_type(
        gray["traits"]["blood_type"]["genotype"],
        michelle["traits"]["blood_type"]["genotype"]
    )
    print_punnett_grid("Blood Type", ["A", "O"], ["B", "O"])
    print()
    for bt, pct in sorted(blood_results.items(), key=lambda x: -x[1]):
        print_probability_bar(bt, pct)

    # --- Rh Factor ---
    print(f"\n\n  Rh FACTOR")
    print(f"  {SECTION}")
    print(f"  Gray: Rh+ (Rh+/Rh-) x Michelle: Rh+ (Rh+/Rh+)")
    rh_results = analyze_rh_factor(
        gray["traits"]["rh_factor"]["genotype"],
        michelle["traits"]["rh_factor"]["genotype"]
    )
    print()
    for rh, pct in sorted(rh_results.items(), key=lambda x: -x[1]):
        print_probability_bar(rh, pct)

    # --- Color Vision (X-linked) ---
    print(f"\n\n  COLOR VISION (X-Linked Inheritance)")
    print(f"  {SECTION}")
    print(f"  Gray: Normal (XN/Y) x Michelle: Carrier (XN/Xn)")
    print(f"\n  Note: Color blindness is X-linked recessive.")
    print(f"  Michelle carries one copy - sons have 50% risk.\n")
    cv = analyze_color_vision(
        gray["traits"]["color_vision"]["genotype"],
        michelle["traits"]["color_vision"]["genotype"]
    )
    print(f"    SONS:")
    for trait, pct in cv["sons"].items():
        print_probability_bar(trait, pct)
    print(f"\n    DAUGHTERS:")
    for trait, pct in cv["daughters"].items():
        print_probability_bar(trait, pct)

    # =========================================================================
    # BLOOD TYPE COMPATIBILITY
    # =========================================================================
    print_banner("BLOOD TYPE SUMMARY FOR CHILDREN", "-")
    print(f"""
  Possible child blood types:  AB, A, B, O  (each 25%)
  All children Rh Positive:    100%

  This means children could receive blood from:
    Type AB+  -> Can receive from: universal (all types)
    Type A+   -> Can receive from: A+, A-, O+, O-
    Type B+   -> Can receive from: B+, B-, O+, O-
    Type O+   -> Can receive from: O+, O-
""")

    # =========================================================================
    # HEALTH MARKERS FOR CHILDREN
    # =========================================================================
    print_banner("HEALTH MARKER INHERITANCE RISK", "=")
    health = analyze_health_markers(gray["genetic_markers"], michelle["genetic_markers"])

    print(f"\n  {'MARKER':<30} {'RISK':>12}")
    print(f"  {SECTION}")
    for marker, desc, risk in health:
        color_risk = risk
        print(f"\n  {marker}")
        print(f"    Assessment: {desc}")
        print(f"    Risk Level: {color_risk}")

    # =========================================================================
    # ANCESTRY BLEND
    # =========================================================================
    print_banner("ESTIMATED CHILD ANCESTRY COMPOSITION", "=")
    child_ancestry = analyze_ancestry(
        gray["genetic_markers"]["ancestry_composition"],
        michelle["genetic_markers"]["ancestry_composition"]
    )

    print(f"\n  {'REGION':<22} {'GRAY':>6} {'MICHELLE':>10} {'CHILD (est)':>12}")
    print(f"  {SECTION}")
    for region in sorted(child_ancestry.keys(), key=lambda r: -child_ancestry[r]):
        g = gray["genetic_markers"]["ancestry_composition"].get(region, 0)
        m = michelle["genetic_markers"]["ancestry_composition"].get(region, 0)
        c = child_ancestry[region]
        bar = "#" * int(c / 2)
        print(f"  {region.replace('_', ' '):<22} {g:>5}% {m:>9}% {c:>10}%  {bar}")

    # =========================================================================
    # MOST LIKELY CHILD PROFILE
    # =========================================================================
    print_banner("MOST LIKELY CHILD PROFILE (Highest Probability Traits)", "*", 70)
    print(f"""
  Based on combined genetic analysis, the most probable child would have:

    Eyes:          Brown or Hazel (50% combined)
    Hair Color:    Medium Brown (50%) or Light Brown (50%)
    Hair Texture:  Wavy (50%) or Straight (50%)
    Dimples:       50/50 chance
    Freckles:      50/50 chance
    Chin:          50/50 cleft vs smooth
    Hairline:      50/50 widow's peak vs straight
    Earlobes:      Free/Detached (100%)
    Tongue Roll:   Can roll tongue (100%)
    Blood Type:    Equal chance of A, B, AB, or O (25% each)
    Rh Factor:     Rh Positive (100%)
    Handedness:    Right-handed likely (~75% population baseline)
    Lactose:       Lactose tolerant (75% chance)

  Fun fact: With {len(gray['traits'])} independent traits analyzed,
  there are over 2 million unique trait combinations possible
  for Gray & Michelle's children!
""")

    # =========================================================================
    # DISCLAIMER
    # =========================================================================
    print(THIN_DIV)
    print("  DISCLAIMER: This is a simplified educational simulation using")
    print("  basic Mendelian genetics. Real human genetics involve thousands")
    print("  of genes, epigenetics, polygenic traits, and environmental")
    print("  factors. Actual results will vary. Consult a genetic counselor")
    print("  for real genetic analysis.")
    print(THIN_DIV)
    print()


if __name__ == "__main__":
    main()

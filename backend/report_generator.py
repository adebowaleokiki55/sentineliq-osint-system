def generate_intel_report(claim: str, result: dict):

    score = float(result.get("score", 0))
    label = str(result.get("label", "UNKNOWN"))
    evidence = result.get("evidence", [])
    contradictions = result.get("contradictions", [])

    # -------------------------
    # CONFIDENCE LEVEL
    # -------------------------
    if score >= 75:
        confidence = "HIGH"
    elif score >= 50:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # -------------------------
    # INTELLIGENCE SUMMARY
    # -------------------------
    if confidence == "HIGH":
        summary = (
            "Multiple high-relevance sources strongly align with the claim. "
            "Current available reporting suggests the claim is likely accurate."
        )
    elif confidence == "MEDIUM":
        summary = (
            "Some sources are relevant to the claim, but evidence is mixed or indirect. "
            "No definitive confirmation can be made from available data."
        )
    else:
        summary = (
            "Available sources do not strongly support the claim. "
            "Evidence is weak, indirect, or insufficient."
        )

    # -------------------------
    # TOP EVIDENCE SELECTION
    # -------------------------
    top_evidence = sorted(
        evidence,
        key=lambda x: x.get("weighted", 0),
        reverse=True
    )[:5]

    evidence_summary = []

    for ev in top_evidence:

        weight = float(ev.get("weighted", 0))

        if weight > 0.5:
            strength = "STRONG"
        elif weight > 0.3:
            strength = "MODERATE"
        else:
            strength = "WEAK"

        evidence_summary.append({
            "title": ev.get("title", ""),
            "url": ev.get("url", ""),
            "strength": strength
        })

    # -------------------------
    # FINAL REPORT STRUCTURE
    # -------------------------
    return {
        "claim": claim,
        "verdict": label,
        "score": score,
        "confidence_level": confidence,
        "summary": summary,
        "key_findings": {
            "sources_analyzed": int(len(evidence)),
            "contradictions": contradictions,
            "top_evidence": evidence_summary
        },
        "analyst_note": (
            "This report is generated using semantic similarity scoring "
            "and source credibility weighting. It does not represent absolute truth."
        )
    }
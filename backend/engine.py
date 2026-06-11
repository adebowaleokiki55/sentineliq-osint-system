from sentence_transformers import SentenceTransformer
import numpy as np
from backend.credibility import credibility_score, get_domain

class ClaimEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def run(self, claim, docs):

        if not docs:
            return {
                "score": 0.0,
                "label": "NO EVIDENCE FOUND",
                "sources_found": 0,
                "evidence": [],
                "contradictions": []
            }

        claim_emb = self.model.encode(claim)

        evidence_list = []
        similarities = []
        credibility_weights = []

        positive_signals = 0
        negative_signals = 0

        for d in docs:

            text = d.get("title", "")
            url = d.get("url", "")

            if not text:
                continue

            emb = self.model.encode(text)

            sim = float(
                np.dot(claim_emb, emb) /
                (np.linalg.norm(claim_emb) * np.linalg.norm(emb))
            )

            cred = credibility_score(url)

            weighted_sim = sim * cred

            similarities.append(sim)
            credibility_weights.append(cred)

            evidence_list.append({
                "title": text,
                "url": url,
                "similarity": float(sim),
                "credibility": float(cred),
                "weighted": float(weighted_sim)
            })

            
            lower = text.lower()

            if "denies" in lower or "false" in lower or "hoax" in lower:
                negative_signals += 1
            elif "confirmed" in lower or "reports" in lower or "announced" in lower:
                positive_signals += 1

        if not similarities:
            return {
                "score": 0.0,
                "label": "NO EVIDENCE FOUND",
                "sources_found": 0,
                "evidence": [],
                "contradictions": []
            }

        
        avg_sim = sum(similarities) / len(similarities)
        avg_cred = sum(credibility_weights) / len(credibility_weights)

        final_score = (avg_sim * 0.6 + avg_cred * 0.4) * 100

       
        contradictions = []

        if negative_signals > positive_signals:
            contradictions.append("More negating reports detected")
        elif positive_signals > 0:
            contradictions.append("Supporting reports detected")

       
        if final_score > 75:
            label = "SUPPORTED"
        elif final_score > 50:
            label = "UNCERTAIN"
        else:
            label = "NOT SUPPORTED"

        return {
            "score": float(final_score),
            "label": label,
            "sources_found": len(docs),
            "evidence": evidence_list,
            "contradictions": contradictions
        }
"""Evaluate sample outputs against a caller-supplied credential corpus."""
import re

def evaluate_exposure(*, samples: list[str], credentials: list[str]) -> dict[str, object]:
    if any(not isinstance(x,str) for x in samples+credentials): raise TypeError("samples and credentials must contain strings")
    secrets = list(dict.fromkeys(x for x in credentials if x))
    findings=[]
    for index, sample in enumerate(samples):
        matches=[secret for secret in secrets if secret in sample]
        findings.append({"sample_index":index,"exposed":bool(matches),"matched_count":len(matches),"matched_labels":[f"credential_{secrets.index(x)+1}" for x in matches]})
    return {"samples_checked":len(samples),"exposed_samples":sum(x["exposed"] for x in findings),"results":findings}

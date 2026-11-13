"""Review common production risks in parsed Helm values."""
from typing import Any

def review_values(values: dict[str, Any]) -> list[dict[str, str]]:
    if not isinstance(values, dict):
        raise ValueError("values must be a mapping")
    findings=[]
    replicas=values.get("replicaCount", 1)
    if not isinstance(replicas,int) or replicas < 0:
        raise ValueError("replicaCount must be a non-negative integer")
    if replicas < 2:
        findings.append({"severity":"medium","code":"LOW_REPLICAS","message":"Configure multiple replicas when the service requires replica-level availability."})
    image=values.get("image") or {}
    tag=image.get("tag")
    if tag in (None,"","latest"):
        findings.append({"severity":"high","code":"MUTABLE_IMAGE_TAG","message":"Pin an immutable image digest or controlled release tag instead of latest."})
    if not values.get("resources",{}).get("requests"):
        findings.append({"severity":"medium","code":"MISSING_RESOURCE_REQUESTS","message":"Define CPU and memory requests for scheduler placement."})
    if not values.get("podDisruptionBudget",{}).get("enabled",False):
        findings.append({"severity":"low","code":"NO_PDB","message":"Consider a PodDisruptionBudget to constrain voluntary disruptions."})
    if not values.get("autoscaling",{}).get("enabled",False):
        findings.append({"severity":"low","code":"NO_AUTOSCALING","message":"Evaluate autoscaling against measured load and service objectives."})
    if values.get("ingress",{}).get("enabled") and not values.get("ingress",{}).get("tls"):
        findings.append({"severity":"medium","code":"INGRESS_WITHOUT_TLS","message":"Configure TLS for externally exposed ingress endpoints."})
    return findings

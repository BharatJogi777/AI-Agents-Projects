"""Offline Docker image metadata inspection."""
from typing import Any

def inspect_image(image: dict[str, Any], large_layer_bytes: int = 100_000_000) -> dict[str, Any]:
    if not isinstance(image, dict) or not image.get("name"):
        raise ValueError("image.name is required")
    layers = image.get("layers", [])
    if not isinstance(layers, list):
        raise ValueError("layers must be a list")
    findings = []
    total = 0
    for i, layer in enumerate(layers):
        size = layer.get("size_bytes")
        if not isinstance(size, int) or size < 0:
            raise ValueError(f"layer {i}: size_bytes must be a non-negative integer")
        total += size
        if size > large_layer_bytes:
            findings.append({"severity":"medium","code":"LARGE_LAYER","message":f"Layer {i} is {size} bytes; inspect build context and cache usage."})
    config = image.get("config") or {}
    user = config.get("user") or image.get("user")
    if not user or user in {"0","root","root:root"}:
        findings.append({"severity":"high","code":"ROOT_DEFAULT_USER","message":"Image appears to run as root by default; use a dedicated non-root user where possible."})
    if not image.get("digest"):
        findings.append({"severity":"medium","code":"MISSING_DIGEST","message":"Immutable image digest is absent; pin deployments to a verified digest."})
    if not image.get("created"):
        findings.append({"severity":"low","code":"MISSING_CREATED","message":"Image creation timestamp is unavailable; verify build provenance."})
    if not image.get("sbom_present", False):
        findings.append({"severity":"medium","code":"MISSING_SBOM","message":"No SBOM evidence supplied; generate and retain an SBOM during build."})
    return {"image":image["name"],"layer_count":len(layers),"total_layer_bytes":total,"findings":findings}

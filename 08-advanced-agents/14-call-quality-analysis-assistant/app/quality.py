from dataclasses import dataclass
@dataclass(frozen=True)
class CallMetrics:
    duration_seconds:float
    dropped_packets:int
    total_packets:int
    latency_ms:float
    jitter_ms:float
def analyze_quality(m:CallMetrics)->dict:
    if m.duration_seconds<=0 or m.total_packets<=0 or m.dropped_packets<0 or m.dropped_packets>m.total_packets or m.latency_ms<0 or m.jitter_ms<0:
        raise ValueError("call metrics are outside valid ranges")
    loss=m.dropped_packets/m.total_packets
    issues=[]
    if loss>0.01: issues.append("packet_loss")
    if m.latency_ms>150: issues.append("high_latency")
    if m.jitter_ms>30: issues.append("high_jitter")
    return {"packet_loss_ratio":loss,"issues":issues,"quality":"poor" if len(issues)>=2 else "degraded" if issues else "within_configured_thresholds",
            "thresholds":{"packet_loss_ratio":0.01,"latency_ms":150,"jitter_ms":30}}

"""Review normalized Kafka topic configuration for operational risk."""
from dataclasses import dataclass

@dataclass(frozen=True)
class TopicFinding:
    topic: str
    severity: str
    issue: str
    recommendation: str

def review_topic(topic: str, config: dict) -> list[TopicFinding]:
    if not isinstance(topic,str) or not topic.strip(): raise ValueError("topic must be non-empty")
    if not isinstance(config,dict): raise TypeError("config must be an object")
    def integer(key,default):
        value=config.get(key,default)
        if isinstance(value,bool) or not isinstance(value,int): raise ValueError(f"{key} must be an integer")
        return value
    rf=integer("replication_factor",1); min_isr=integer("min_insync_replicas",1)
    retention=integer("retention_ms",-1); segment=integer("segment_ms",604800000)
    if rf<1 or min_isr<1 or retention< -1 or segment<=0: raise ValueError("invalid topic configuration values")
    findings=[]
    if rf<3: findings.append(TopicFinding(topic,"high","Replication factor below 3","Consider replication factor 3 across independent brokers or zones."))
    if min_isr>=rf: findings.append(TopicFinding(topic,"medium","min.insync.replicas is not below replication factor","Ensure producer availability and durability trade-offs are intentional."))
    if retention== -1: findings.append(TopicFinding(topic,"medium","Infinite retention","Confirm storage capacity, retention policy, and compliance requirements."))
    cleanup=config.get("cleanup_policy","delete")
    if cleanup not in {"delete","compact","compact,delete","delete,compact"}: raise ValueError("unsupported cleanup_policy")
    if cleanup=="compact" and retention>0: findings.append(TopicFinding(topic,"low","Compacted topic has finite retention","Verify tombstone retention and compaction behavior meet recovery needs."))
    return findings

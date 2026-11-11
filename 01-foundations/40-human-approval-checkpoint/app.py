"""Compatibility facade. New code should import approval_gate."""
from approval_gate import Approval,ApprovalNotFound,ApprovalGate,canonical_action_hash
__all__=["Approval","ApprovalNotFound","ApprovalGate","canonical_action_hash"]

import pytest
from plan_generator import *
class Planner:
 def generate(self,_):return [PlanStep("1","Inspect","Facts captured")]
def test_roundtrip_and_bounds():
 plan=PlanGenerationAgent(Planner()).generate("goal")
 assert from_json(to_json(plan))==plan
 with pytest.raises(PlanFormatError):from_json('{"objective":"x","steps":[]}')
def test_extra_and_duplicate_fields_rejected():
 with pytest.raises(PlanFormatError):from_json('{"objective":"x","steps":[],"extra":1}')
 raw='{"objective":"x","steps":[{"id":"a","action":"a","expected_outcome":"b"},{"id":"a","action":"c","expected_outcome":"d"}]}'
 with pytest.raises(PlanFormatError):from_json(raw)

import pytest
from app import *
class P:
 def generate(self,o):return [PlanStep("1","Inspect","Facts captured")]
def test_roundtrip():
 p=PlanGenerationAgent(P()).generate("goal");assert from_json(to_json(p))==p
def test_duplicate():
 class B:
  def generate(self,o):return [PlanStep("x","a","b"),PlanStep("x","c","d")]
 with pytest.raises(ValueError):PlanGenerationAgent(B()).generate("x")
def test_extra_field():
 with pytest.raises(ValueError):from_json('{"objective":"x","steps":[],"extra":1}')

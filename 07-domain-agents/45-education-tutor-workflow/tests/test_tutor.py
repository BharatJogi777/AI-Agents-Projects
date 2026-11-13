import pytest
from app.tutor import LearningObjective,build_learning_path
def test_orders_prerequisites_first():
 a=LearningObjective("A","Basics",(),0.8); b=LearningObjective("B","Advanced",("A",),0.9)
 r=build_learning_path([b,a],set())
 assert [x["objective_id"] for x in r["learning_path"]]==["A","B"]
def test_rejects_prerequisite_cycle():
 a=LearningObjective("A","A",("B",),0.8); b=LearningObjective("B","B",("A",),0.8)
 with pytest.raises(ValueError): build_learning_path([a,b],set())

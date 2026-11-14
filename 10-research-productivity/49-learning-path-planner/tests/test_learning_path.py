from app.learning_path import LearningTopic,build_learning_path
import pytest
def test_orders_prerequisites_first():
 topics=[LearningTopic("agents","Agents",("python",)),LearningTopic("python","Python")]
 assert [t.id for t in build_learning_path(topics)]==["python","agents"]
def test_cycle_rejected():
 with pytest.raises(ValueError,match="cycle"): build_learning_path([LearningTopic("a","A",("b",)),LearningTopic("b","B",("a",))])
def test_unknown_prerequisite_rejected():
 with pytest.raises(ValueError,match="unknown"): build_learning_path([LearningTopic("a","A",("missing",))])

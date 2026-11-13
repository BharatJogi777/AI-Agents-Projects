import pytest
from app.training import SkillGap,recommend
def test_recommendations_ranked_by_priority():
 r=recommend([SkillGap("Python",1,4,5)],[{"id":"c1","title":"Python basics","skills":["python"],"duration_hours":3}])
 assert r["recommendations"][0]["resources"][0]["id"]=="c1" and not r["automatic_enrollment"]
def test_invalid_level():
 with pytest.raises(ValueError): recommend([SkillGap("Go",8,4)],[])

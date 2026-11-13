import pytest
from app.navigation import NavigationSession
def test_back_restores_previous_page():
 s=NavigationSession({"a.example","b.example"}); s.navigate("https://a.example/one"); s.navigate("https://b.example/two")
 assert s.back()=="https://a.example/one"
def test_disallowed_host_rejected():
 with pytest.raises(ValueError): NavigationSession({"a.example"}).navigate("https://evil.example")

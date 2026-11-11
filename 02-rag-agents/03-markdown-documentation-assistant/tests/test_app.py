import pytest
from app import chunk_markdown
def test_heading_path_and_lines():
 rows=chunk_markdown("# Guide\\nintro\\n## Install\\nrun\\n### Linux\\nsteps")
 assert rows[-1].heading_path==("Guide","Install","Linux") and rows[0].start_line==1 and rows[-1].end_line==6
def test_validation():
 with pytest.raises(ValueError): chunk_markdown("x",10)
 with pytest.raises(TypeError): chunk_markdown(None)

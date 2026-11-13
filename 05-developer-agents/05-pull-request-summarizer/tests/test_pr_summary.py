from app.pr_summary import summarize_diff

def test_diff_summary():
    diff="diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n+added\n-removed\n context\ndiff --git a/b.txt b/b.txt\nBinary files a/b.txt and b/b.txt differ\n"
    result=summarize_diff(diff)
    assert (result.changed_files,result.additions,result.deletions)==(2,1,1)
    assert result.files[1].binary

def test_empty_diff():
    result=summarize_diff("")
    assert result.changed_files == result.additions == result.deletions == 0

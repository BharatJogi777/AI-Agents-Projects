from app import deduplicate,normalize
def test_duplicates():
 g=deduplicate({"a":"Hello, WORLD!","b":"hello world","c":"different"}); assert g[0].document_ids==("a","b")
def test_empty_and_normalize(): assert deduplicate({"a":"","b":" "})[0].document_ids==("a","b") and normalize("A-b_c")=="a b_c"

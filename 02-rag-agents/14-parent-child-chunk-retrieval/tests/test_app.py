from app import build_parent_child,expand_to_parents
def test_expansion():
 p,c=build_parent_child("doc","x"*900,600,200); out=expand_to_parents([c[0].id,c[1].id,c[-1].id],c,p); assert len(out)==2 and out[0].id==p[0].id
def test_empty(): assert build_parent_child("doc","",100,20)==([],[])

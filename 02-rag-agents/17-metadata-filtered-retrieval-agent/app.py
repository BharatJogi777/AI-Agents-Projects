from dataclasses import dataclass
@dataclass(frozen=True)
class MetadataFilter: field:str; operator:str; value:object
def validate_filters(filters,allowed_fields):
 ops={"eq","in","gte","lte","contains"}; out=[]
 for f in filters:
  if f.field not in allowed_fields or f.operator not in ops: raise ValueError("field or operator not allowed")
  if f.operator=="in" and (not isinstance(f.value,(list,tuple)) or len(f.value)>100): raise ValueError("in requires bounded list")
  if f.operator in {"gte","lte"} and (isinstance(f.value,bool) or not isinstance(f.value,(int,float))): raise ValueError("range requires number")
  out.append(f)
 return out
def matches(metadata,filters):
 for f in filters:
  a=metadata.get(f.field)
  if f.operator=="eq" and a!=f.value:return False
  if f.operator=="in" and a not in f.value:return False
  if f.operator=="gte" and (isinstance(a,bool) or not isinstance(a,(int,float)) or a<f.value):return False
  if f.operator=="lte" and (isinstance(a,bool) or not isinstance(a,(int,float)) or a>f.value):return False
  if f.operator=="contains" and (not isinstance(a,str) or not isinstance(f.value,str) or f.value.casefold() not in a.casefold()):return False
 return True

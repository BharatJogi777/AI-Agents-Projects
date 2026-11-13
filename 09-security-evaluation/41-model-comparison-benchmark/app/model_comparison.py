"""Compare model candidates using paired, caller-supplied evaluation scores."""
from dataclasses import dataclass
from typing import Mapping
@dataclass(frozen=True)
class ModelScore:
 model:str; mean_score:float; scored_cases:int
@dataclass(frozen=True)
class Comparison:
 rankings:tuple[ModelScore,...]; score_gaps:tuple[tuple[str,str,float],...]
def compare_models(scores:Mapping[str,Mapping[str,float]])->Comparison:
 if len(scores)<2: raise ValueError("at least two models are required")
 case_sets=[set(x) for x in scores.values()]
 if any(not x for x in case_sets) or any(x!=case_sets[0] for x in case_sets[1:]): raise ValueError("all models must have the same non-empty case IDs")
 means=[]
 for model,values in scores.items():
  if not model.strip() or any(not isinstance(v,(int,float)) or isinstance(v,bool) or not 0<=v<=1 for v in values.values()): raise ValueError("model names and scores in [0,1] required")
  means.append(ModelScore(model,sum(values.values())/len(values),len(values)))
 means.sort(key=lambda x:(-x.mean_score,x.model))
 gaps=tuple((means[i].model,means[j].model,means[i].mean_score-means[j].mean_score) for i in range(len(means)) for j in range(i+1,len(means)))
 return Comparison(tuple(means),gaps)

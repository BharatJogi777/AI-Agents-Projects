from memory_retrieval import *
def test_filter_rank_and_deduplicate():
 values=[Memory("a","python concise answers",True,.9,90),Memory("b","python",False,1,99),Memory("c","python private",True,1,99,sensitive=True),Memory("d","python expired",True,.9,99,100)]
 assert [m.id for m in retrieve("python",values,100)]==["a"]
 assert len(retrieve("python",values+[values[0]],100))==1
def test_no_overlap_and_ranked_result():
 assert not retrieve("unknown",[Memory("a","python",True,1,1)],10)
 assert retrieve_ranked("python",[Memory("a","python",True,1,1)],10)[0].score>0

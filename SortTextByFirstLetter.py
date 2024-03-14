#可以直接让GPT来排序。

references = [
    "[1] Anders K H. A hierarchical graph-clustering approach to find groups of objects [C]// In: Proceedings of the 5th ICA Workshop on Progress in Automated Map Generalization, pp: 28-35.2003",
    "[2] Anders K H. Grid typification [M]//In: RIEDL A, KAINZ W, ELMES G A. Progress in Spatial Data Handling. Berlin Heidelberg: Springer, pp: 633–642,2006.",
    "[3] Ai T, Yu W, He Y. Generation of constrained network Voronoi diagram using linear tessellation and expansion method[J]. Computers, Environment and Urban Systems, 2015, 51(3): 83-96.",
    "[4] Borruso G. Network density estimation: analysis of point patterns over a network[C] //International Conference on Computational Science and Its Applications. Springer, Berlin, Heidelberg, 2005: 126-132.",
    "[5] Bjorke,J. T. Framework for Entroy-bas"
]

def get_author_name(reference):
    # 获取作者名称
    start_index = reference.find("] ") + 2
    end_index = reference.find(".", start_index)
    return reference[start_index:end_index]

# 按照作者名称排序
sorted_references = sorted(references, key=get_author_name)

# 打印排序后的参考文献
for ref in sorted_references:
    print(ref)

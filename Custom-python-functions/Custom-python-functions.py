#从独热编码形式的标签，得到整数的标签。处理单个样本# From the tag in the unique thermal encoding form, get the integer tag. Processing a single sample
def getLabelOFIntFromLst(raw_y):
    for i2 in range(len(raw_y)):
        if raw_y[i2]==1:
            return i2
        
#将样本的列表型标签，转换成 单个整数的标签。处理批量样本# Convert the sample's column phenotype label to a single integer label. Processing batch samples
def transToEnsemInuputY(raw_y):
    y=[]
    for i1 in range(len(raw_y)):
        for i2 in range(len(raw_y[i1])):
            if raw_y[i1][i2]==1:
                    y.append(i2)
                    break
    y=np.array(y)
    return y                           
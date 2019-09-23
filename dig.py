import pandas as pd
import numpy as np
import orangecontrib.associate.fpgrowth as oaf
import functools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import json
fileInput = ''
#这个函数是将生成的关联规则转换成为DataFrame类型，便于存储在excel文件中 
def ResultDFToSave(rules,strDecode):
    try:
        with open('filelocation.json') as f_obj:
            fileInput=json.load(f_obj)
    except:
        with open('errorFlag.json','w') as e_obj:
            json.dump("File open process failed",e_obj)
        return
    returnRules = []
    for i in rules:
        temList = []
        temStr = '';
        for j in i[0]:   #处理第一个frozenset
            temStr = temStr + strDecode[j] + '&'
        temStr = temStr[:-1]
        temStr = temStr + ' ==> '
        for j in i[1]:
            temStr = temStr + strDecode[j] + '&'
        temStr = temStr[:-1]
        temList.append(temStr); temList.append(i[2]); temList.append(i[3]); temList.append(i[4])
        temList.append(i[5]); temList.append(i[6]); temList.append(i[7])
        returnRules.append(temList)
    return pd.DataFrame(returnRules,columns=('规则','项集出现数目','置信度','覆盖度','力度','提升度','利用度'))
        
def associateRules(support=0.02, confidence=0.5):
    support=0.15
    confidence=0.15
    try:
        with open('filelocation.json') as f_obj:
            fileInput=json.load(f_obj)
    except:
        with open('errorFlag.json','w') as e_obj:
            json.dump("File open process failed",e_obj)
        return
    filename=fileInput
    
    dfar=pd.read_csv(filename)
    tag=list(dfar.columns.values)
    listToAnalysis=[]#最终结果
    
    for item in range(1,len(tag)-1):#遍历列
        imax = max(list(dfar[tag[item]]))#上界
        imin = min(list(dfar[tag[item]]))#下界
        
        ijc = imax - imin#极差
        l = ijc / 4
        
        i1=imin+l
        i2=i1+l
        i3=i2+l
        
        listToStore=[]
        
        for i in range(dfar.shape[0]):
            s=dfar.iloc[i][tag[item]]
            
            if s >=i3 and s <= imax:
                ss=tag[item]+str(i3)+'-'+str(imax)
            elif s>=i2:
                ss=tag[item]+str(i2)+'-'+str(i3)
            elif s>=i1:
                ss=tag[item]+str(i1)+'-'+str(i2)
            elif s>=imin:
                ss=tag[item]+str(imin)+'-'+str(i1)
            listToStore.append(ss)
        
        listToAnalysis.append(listToStore.copy())

    listToAnalysis2 = []
    ll = len(listToAnalysis[0])

    for ii in range(ll):
        ltmp = []
        for it in listToAnalysis:
            ltmp.append(it[ii])
        listToAnalysis2.append(ltmp.copy())

    #创建编码词典与解码词典
    what=functools.reduce(lambda a,b:a+b,listToAnalysis2)
    strSet=set(what)
    
    zz=zip(strSet,range(len(strSet)))
    strEncode=dict(zz)#编码字典
    
    strDecode=dict(zip(strEncode.values(),strEncode.keys()))#解码字典
    
    listToAnalysis_int=[list(map(lambda item:strEncode[item],row)) for row in listToAnalysis2]
    
    with open('Information.json') as obj:
        infostring = json.load(obj)
    inforlist=infostring.split(' ')
    confidence=float(inforlist[0])/float(100)
    support=float(inforlist[1])/float(100)
    itemsets=dict(oaf.frequent_itemsets(listToAnalysis_int,support))
    #频繁项集
    
    rules=oaf.association_rules(itemsets,confidence)
    rules=list(rules)
    #关联规则
    
    regularNum=len(rules)
    
    #printRules=dealResult(result,strDecode)
    #######
    #print("You will get ")
    #print(regularNum)
    #print("association rules when\n"+"SupportRate = ",end='')
    #print(support,end='')
    #print("ConfidenceRate = "+str(confidence))
    informationBack="You will get "+str(regularNum)+"association rules when\n"\
                                                    +"SupportRate = "+str(support)+" ConfidenceRate = "+str(confidence)
    with open('InformationBack.json', 'w') as inf:
        json.dump(informationBack, inf)
    result=list(oaf.rules_stats(rules,itemsets,len(listToAnalysis_int)))
    
    dfToSave=ResultDFToSave(result,strDecode)
    with open('arInteractiveText.json','w') as ij:
        json.dump(str(dfToSave),ij)
    saveRegularName="Processed.xlsx"
    dfToSave.to_excel(saveRegularName)
    return regularNum

"""
这个文件的功能是针对ApplicantData.csv这一文件，按照是否获得offer，
进行主成分分析，画出聚类散点图。
"""
def PCA_graph():
    try:
        with open('filelocation.json') as f_obj:
            fileInput=json.load(f_obj)
    except:
        with open('errorFlag.json','w') as e_obj:
            json.dump("File open process failed",e_obj)
        return
    filename=fileInput
    dfpca=pd.read_csv(filename)#读入文件,df是Dataframe类型
    DataToProcess=np.array(dfpca)#将df转换为ndarray类型
    
    y=DataToProcess[...,-1:]
    y=[i[0] for i in y]
    #y是获取了所有人是否获取offer的信息
    yy=[]
    ytmp={}
    cnt = 0
    for i in y:
        if i not in ytmp.keys():
            ytmp[i] = cnt
            cnt+=1
        yy.append(ytmp[i])
    
    yy=np.array(yy)
    
    DataToProcess=DataToProcess[...,1:-1]
    #我们需要处理的数据，应该是去掉第一列（序号列）与最后一列（是否获得offer列）
    #的其他数据
    
    #将y转换为yy（ndarray类型），可以指明之后画图时的不同聚类的点的颜色
    #以下部分是作图
    
    fig=plt.figure("PCA",figsize=(8,6))
    ax=Axes3D(fig,elev=-150,azim=110)#后两个参数控制视角
    X_reduced=PCA(n_components=3).fit_transform(DataToProcess)
    #n_components=3是指，我们选取前三大的特征值
    ax.scatter(X_reduced[:,0],X_reduced[:,1],X_reduced[:,2],c=yy,cmap=plt.cm.Set1,edgecolor='k',s=40)
    #这些都是控制绘图的细节
    ax.set_title("First three PCA directions")
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("3rd eigenvector")
    ax.w_zaxis.set_ticklabels([])

    #plt.show()

def statistics():
    try:
        with open('filelocation.json') as f_obj:
            fileInput=json.load(f_obj)
    except:
        with open('errorFlag.json','w') as e_obj:
            json.dump("File open process failed",e_obj)
        return
    filename=fileInput
    dfst=pd.read_csv(filename)
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    dis=dfst.describe()
    
    tag=list(dfst.columns.values)
    
    #dfe=dis['UGScore']
    #print(dfe)
    df1=dis[tag[1]]
    df2=list(df1)
    df2=df2[1:]
    
    with open('InteractiveText.json','w') as ij:
        json.dump(str(dis)+'\n'+str(df2),ij)
    xaxis=["平均值","标准差","最小值","%25","%50","%75","最大值"]
    plt.bar(range(7),df2,align='center',color='steelblue')
    plt.ylabel('Statistics')
    plt.xticks(range(7),xaxis)
    for x,y in enumerate(df2):
        plt.text(x,y+10,'%s'%round(y,1),ha='center')


    # plt.show()
    
# if __name__=='__main__':
#     ar(0.2,0.5)
#     statistics()
#     PCA_graph()
#     plt.show()
#
        

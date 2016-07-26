# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 14:04:07 2016

@author: YI
"""

 
   
def createC1(dataset):
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if [item] not in c1:
                c1.append([item])
    return map(frozenset, c1)
    
def filterD(dataset, c1, minSupport=0.5):
    temp = {}
    for transaction in dataset:
        for item in c1:
            if item.issubset(transaction):
                if not temp.has_key(item):
                    temp[item] = 1
                else:
                    temp[item] += 1
    numTrans = len(dataset)
    retList = []
    supportData = {}
    for key in temp:
        support = temp[key] / float(numTrans)
        if support >= minSupport:
            retList.append(key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(retList, k):
    newretList = []
    m = len(retList)
    for i in range(m):
        for j in range(i+1, m):
            L1 = [retList[i]][:k-2]
            L2 = [retList[j]][:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                newretList.append(retList[i]|retList[j])
    return newretList
    
def apriori(dataset, k, minSupport=0.5):
    c1 = createC1(dataset)
    L1, supportdata = filterD(dataset, c1)
    L = [L1]
    while len(L[k-2]) > 0:
        ck = aprioriGen(L[k-2], k)
        Lk, supportk = filterD(dataset, ck)
        supportdata.update(supportk)
        L.append(Lk)
        k += 1
    return L, supportdata
    
def generateRules(L, supportData, minConf=0.7):
    ruleList = []
    for i in range(1, len(L)):
        for freqset in L[i]:
            iterm = [frozenset([iterm]) for iterm in freqset]
            if i > 1:
                rules(freqset, iterm, supportData, ruleList, minConf)
            else:
                calConf(freqset, iterm, supportData, ruleList, minConf)
        
def calConf(freqset, iterm, supportData, ruleList, minConf):
    pruneIterm = []
    for conseq in iterm:
        conf = supportData[freqset] / supportData[freqset - conseq]
        if conf > minConf:
            print freqset - conseq, '--->', conseq, 'conf:', conf
            ruleList.append((freqset-conseq, conseq, conf))
            pruneIterm.append(conseq)
    return pruneIterm
    
def rules(freqset, iterm, supportData, ruleList, minConf):
    m = len(iterm[0])
    if len(freqset) > m+1:
        nList = aprioriGen(iterm, m+1)
        nList = calConf(freqset, nList, supportData, ruleList, minConf)
        if len(nList) > 1:
            rules(freqset, nList, supportData, ruleList, minConf)
    
    

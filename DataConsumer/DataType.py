from typing import Iterable, OrderedDict

from pandas import array
from RangeType import *
import numpy as np
import collections as c
class DataConfig:
    '''
    该类型用于储存数据的相关参数,
    目前仅含有对于单位和名称(及其缩写)的储存
    '''
    def __init__(self,fullname:str,shortname:str=None,unit:str=None) -> None:
        '''初始化函数,保存相关信息'''
        self.fullname=fullname
        self.shortname=shortname
        self.unit=unit

    def tabular_format(self):
        '''
        该方法按照fullname$shortname$($\mathbf{unit}$)的方式进行格式化,
        可以作为表头
        '''
        retstrlist=[]
        if self.fullname:
            retstrlist.append(self.fullname)
        if self.shortname:
            retstrlist.append("$"+self.shortname+"$")
        if self.unit:
            retstrlist.append("($\mathbf{"+self.unit+"}$)")
        return "".join(retstrlist)
        
class DataConsumer:
    '''
    一个储存并且将数据按照指定方式进行处理的库
    '''
    def __init__(self,inpdict:dict,func,confdict:dict) -> None:
        '''inpdict:输入数据的字典(使用快速指标)
            func:对于数据中的每一组元素进行处理的函数,接受**argv,
            并且输出一个有序数组collections
            confdict:一个用于指示快速指标和内容关系的字典
        '''
        self._indict=inpdict
        self._confdict=confdict
        (self._inkeylist,self._inty,self._inarray)=\
            DataConsumer.__dict2array(self._indict)
        self._consume_func=func
        #字典展平
        odict=c.OrderedDict()
        for datal in self._inarray:
            ind=dict(zip(self._inkeylist,datal))
            oud: OrderedDict=self._consume_func(**ind)
            for k in oud:
                if not k in odict:
                    odict[k]=[]
                odict[k].append(oud[k])
        self._outdict: c.OrderedDict=odict
        (self._outkeylist,self._outty,self._outarray)=\
            DataConsumer.__dict2array(self._outdict)
        
    
    def __str__(self) -> str:
        '''将输出一个md风格的表格'''
        tablist=[self._confdict[key].tabular_format() for key in self._outkeylist]
        titlestr="|"+"|".join(tablist)+"|\n"
        setstr="|----"*len(self._outkeylist)+"|\n"
        mainstrlist=[]
        for k in self._outarray:
            mainstrlist.append("|"+"|".join(
                        [str(s) for s in k])+"|\n")
        retstr=titlestr+setstr+"".join(mainstrlist)
        return retstr

    def __dict2array(indict:dict):
        lis=list(indict.keys())
        ty=np.dtype([(key,list) for key in indict])
        wl=[]
        for k in range(len(indict[lis[0]])):
            l=[]
            for w in lis:
                l.append(indict[w][k])
            wl.append(tuple(l))
        array=np.array(wl,dtype=ty)
        return (lis,ty,array)


if __name__=="__main__":
    pass
        



from cProfile import label
from typing import Iterable, OrderedDict,Tuple

#?from pandas import array
from DataConsumer.RangeType import *
import math
import numpy as np
import collections as c
import matplotlib.pyplot as plt
import scipy.stats as stats
class DataConfig:
    """用于储存数据信息
    """    
    def __init__(self,fullname:str,shortname:str=None,unit:str=None) -> None:
        """__init__ 初始化一个DataConfig

        Parameters
        ----------
        fullname : str
            一个数据的全名
        shortname : str, optional
            一个数据名称的缩写, by default None
        unit : str, optional
            单位, by default None
        """               
        self.fullname=fullname
        self.shortname=shortname
        self.unit=unit

    def tabular_format(self)->str:
        """tabular_format 用于将其格式化为一个表头格式

        Returns
        -------
        str
            一个表头格式的字符串
        """              
        retstrlist=[]
        if self.fullname:
            retstrlist.append(self.fullname)
        if self.shortname:
            retstrlist.append("$"+self.shortname+"$")
        if self.unit:
            retstrlist.append("($\mathrm{"+self.unit+"}$)")
        return "".join(retstrlist)
    def mat_format(self)->str:
        """mat_format 格式化为绘图所用格式

        Returns
        -------
        str
            绘图所用格式的字符串
        """        
        #*目前与表头格式字符串实现相同
        return self.tabular_format()
        
class DataConsumer:
    """一个处理字符串的类型
    """    
    def __init__(self,inpdict:dict,func,confdict:dict,err_str:False) -> None:        
        """__init__ 初始化函数

        Parameters
        ----------
        inpdict : dict
            输入数据的字典(缩写指标)
        func : _type_
            一个数据处理用的函数
        confdict : dict
            保存数据信息的字典
        err_str : False
            选择是否在格式化字符串时输出误差
        """              
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
        """__str__ 返回md格式表格

        Returns
        -------
        str
            一个包含md格式表格的字符串
        """               
        tablist=[self._confdict[key].tabular_format() for key in self._outkeylist]
        titlestr="|"+"|".join(tablist)+"|\n"
        setstr="|----"*len(self._outkeylist)+"|\n"
        mainstrlist=[]
        for k in self._outarray:
            mainstrlist.append("|"+"|".join(
                        [str(s) for s in k])+"|\n")
        retstr=titlestr+setstr+"".join(mainstrlist)
        return retstr

    def latexstr(self)->str:
        tablist=[self._confdict[key].tabular_format() for key in self._outkeylist]
        titlestr="&".join(tablist)+"\\\\\\hline\n"
        setstr=""
        mainstrlist=[]
        for k in self._outarray:
            mainstrlist.append("&".join(
                        [str(s) for s in k])+"\\\\\\hline\n")
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
    def get_fitted(self,xdataname:str,ydataname:str)->c.namedtuple:              
        """get_fitted 获得拟合的多项式

        Parameters
        ----------
        xdataname : str
            x数据简称
        ydataname : str
            y数据简称

        Returns
        -------
        c.namedtuple
            同stats.linregress的返回
        """        
        xdata=np.array(self._outdict[xdataname],dtype=float)
        ydata=np.array(self._outdict[ydataname],dtype=float)
        #!该方法被弃用
        # poly=np.polyfit(xdata,ydata,1)
        # #*求SSR
        # pydata=np.polyval(poly,xdata)
        # SSR=np.sum((ydata-pydata)**2)
        # #*求SST
        # avey=np.mean(ydata)
        # SST=np.sum((ydata-avey)**2)
        # RS=1-SSR/SST
        # #*求不确定度

        return stats.linregress(xdata,ydata) 
    def draw_fitted(self,xdataname:str,ydataname:str
                    ,fig:plt.subplot,**kwargs)->Tuple[c.namedtuple,tuple]:
        """draw_fitted 绘制拟合后的图像

        Parameters
        ----------
        xdataname : str
            x数据简称
        ydataname : str
            y数据简称
        fig : plt.subplot
            用于绘图的子图
        Returns
        -------
        c.namedtuple
            同stats.linregress的返回
            slope:斜率
            intercept:截距
            rvalue:R(使用时需要平方)
            pvalue:P(一般要大于0.05有效)
            stderr:斜率误差
            intercept_stderr:截距误差
        tuple
            类似poly,但是里面的是RangeNumber
        """              
        fdata=self.get_fitted(xdataname,ydataname)
        rettuple=(RangeNumber(fdata.slope,fdata.stderr),
                  RangeNumber(fdata.intercept,fdata.intercept_stderr))
        RSquared=(fdata.rvalue)**2
        poly=(fdata.slope,fdata.intercept)
        xplot=np.linspace(min(self._outdict[xdataname])
                        ,max(self._outdict[xdataname]),20)
        yplot=np.polyval(poly,xplot)
        fig.plot(xplot,yplot,**kwargs)
        fig.set_xlabel(self._confdict[xdataname].mat_format())
        fig.set_ylabel(self._confdict[ydataname].mat_format())
        fig.set_title("$R^2=%0.4f$"%RSquared)
        return fdata,rettuple
    def quick_draw(self,xdataname:str,ydataname_list:list,yaxis_name:str,
                    fig:plt.subplot,*argc,**kwargs)->None:
        """quick_draw 对于一些变量进行快速绘图

        Parameters
        ----------
        xdataname : str
            x轴数据
        ydataname_list : list
            y轴数据的列表(单位相同)
        yaxis_name : str
            y轴名称
        fig : plt.subplot
            子图
        """        
        xplot=np.array(self._outdict[xdataname],dtype=float)
        for i in ydataname_list:
            yplot=np.array(self._outdict[i],dtype=float)
            fig.plot(xplot,yplot,
                    label=self._confdict[i].mat_format(),*argc,**kwargs)
        fig.set_ylabel(yaxis_name)
        fig.set_xlabel(self._confdict[xdataname].mat_format())
        fig.legend(loc="best")

if __name__=="__main__":
    pass
        



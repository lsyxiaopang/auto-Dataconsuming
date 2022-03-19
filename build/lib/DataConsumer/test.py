from typing import Tuple
import matplotlib.pyplot as plt

class PlotDotConfig:
    '''
    该类储存一个绘图点的信息

    该类信息包含:特殊标记(例如忽略该数据点,或予以强调);图注(如果有图注,应当以何种形式)
    '''
    def __init__(self,tag="",legend="") -> None:
        '''初始化标记和图注'''
        self._tag=tag
        self._legend=legend
    def checktag(self,tag)->bool:
        return self._tag==tag
    @property
    def legend(self)->str:
        return self._legend


class DrawType:
    '''该类储存一类数据所使用的绘图样式类型'''
    def __init__(self,linetype="b-",include_in_graph:bool=True,
                include_in_line:bool=True,annotateplace:Tuple=None) -> None:
        '''保存绘图的相关的特征'''
        self._linetype=linetype
        self._include_in_graph=include_in_graph
        self._include_in_line=include_in_line
        self._annotateplace=annotateplace




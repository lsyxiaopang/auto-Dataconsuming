from turtle import down
from typing import Tuple, List
import numpy as np
import math


class RangeNumber:
    """ 带有不确定度的数字

        支持四则运算，并且可以转换其格式'
    """

    def __init__(self, mainnumber: float, uperr: float = 0,
                 downerr: float = 0, err_str=True) -> None:
        """__init__ 用最基本的方法初始化一个有不确定度的数字

        Parameters
        ----------
        mainnumber : float
            数值
        uperr : float, optional
            上误差 by default 0
        downerr : float, optional
            下误差 by default 0注意,当其取默认值时为-uperr
        err_str : True
            是否显示误差的值

        Raises
        ------
        ValueError
            上误差应当大于等于0
        ValueError
            下误差应当小于等于0

        Examples
        ------
        >>RangeNumber(10.0)#创建一个没有误差的数字（误差为0）

        >>RangeNumber(10.0,0.1)#代表数字(10+-0.1)

        >>RangeNumber(10.0,0.2,-0.1)#代表数字（10+0.2-0.1）
        """
        self._mainnumber = float(mainnumber)
        if uperr < 0:
            raise ValueError("uperr should not less than zero!")
        else:
            self._uperr = uperr
        if downerr > 0:
            raise ValueError("downerr should not more than zero!")
        elif downerr == 0:
            self._downerr = -uperr
        else:
            self._downerr = downerr
        #!调试时打开此选项
        self.err_str = err_str  # *判断是否显示误差值

    @property
    def mainnum(self) -> float:
        """mainnum 属性,返回值

        Returns
        -------
        float
            值
        """
        return self._mainnumber

    @property
    def wholedata(self) -> Tuple[float, float, float]:
        """wholedata 得到全体数据

        Returns
        -------
        Tuple[float,float,float]
            返回完整的数据，以(downerr,mainnumber,uperr)的方式组织
        """        ''''''
        return (self._downerr, self._mainnumber, self._uperr)

    @property
    def uperr(self) -> float:
        return self._uperr

    @property
    def downerr(self) -> float:
        return self._downerr

    @property
    def mmatype(self) -> str:
        """mmatype mma风格

        Returns
        -------
        str
            返回一个mma风格的字符串
        """
        if abs(self._downerr) < abs(self._mainnumber)/100000 \
                and abs(self._uperr) < abs(self._mainnumber)/100000:  # 忽略误差
            return str(self._mainnumber)
        else:
            return "Around["+str(self._mainnumber)+",{"+str(self._downerr)\
                + ","+str(self._uperr)+"}]"

    def __str__(self) -> str:
        """__str__ 返回一个LaTex风格的字符串（在此时，mainnumber已经使用约化）

        Returns
        -------
        str
            返回一个LaTex风格的字符串（在此时，mainnumber已经使用约化）  
            当log10(mainnumber)>4，或max(|uperr|,|downerr|)>1则使用科学计数法表示
        """
        # todo 现有的数据修约可能存在问题,需要修改
        errnumu = "%.1g" % self._uperr
        errnumd = "%.1g" % self._downerr
        if self.err_str:  # *显示是否展示误差大小
            retstr = "$(" +\
                RangeNumber.__confloat(self._mainnumber,
                                       max(-self._downerr, self._uperr))\
                + ")"+"^{"+str(errnumu)+"}_{"+str(errnumd)+"}$"
        else:
            retstr = "$"+RangeNumber.__confloat(self._mainnumber,
                                                max(-self._downerr, self._uperr))+"$"
        return retstr

    def __getfloatlen(s: float):
        abss = abs(s)
        # if 10>abss>=0:#?遇到0失效,位数定位1
        #     log=1
        log = int(math.log10(abss)+1e-10)
        if log <= 0 and math.log10(abss) < 0:
            log -= 1
        return log

    def __confloat(s: float, err: float):
        ls = RangeNumber.__getfloatlen(s)
        lerr = RangeNumber.__getfloatlen(err)
        if abs(ls) < 4 and lerr < 0:
            allwstr = "%0.{}f".format(-lerr)
            return allwstr % s
        else:
            allwstr = "%0.{}f".format(ls-lerr+1)
            cds = s/(10**ls)
            return allwstr % cds+"\\times 10^{{ {} }}".format(ls)
# *以下部分为误差的相关运算
# todo 对于上下误差不等时的计算仍然可能存在问题需要修正

    def _get_lr(self, plist, xlist):
        """_get_lr 通过输入偏导,获得上下误差

        Parameters
        ----------
        plist : list
            一个储存了偏导的列表
        xlist : _type_
            数据列表

        Returns
        -------
        上下误差的元组

        """
        l = [0, 0]
        assert len(plist) == len(xlist)
        for i in range(len(plist)):
            p1 = plist[i]
            x1 = xlist[i]
            a = p1*x1._downerr
            b = p1*x1._uperr
            # ?如果上下不对称的情况,有待修正
            if a < 0:
                l[-1] += a**2
                l[0] += b**2
            else:
                l[0] += a**2
                l[-1] += b**2
        down = -math.sqrt(l[-1])
        up = math.sqrt(l[0])
        return up, down

    def __float__(self) -> float:
        '''当初始化float时,直接返回主值'''
        return self.mainnum

    def __add__(self, other):
        if not isinstance(other, RangeNumber):
            other = RangeNumber(other)
        r, l = self._get_lr([1, 1], [self, other])
        # l=-math.sqrt((self._downerr)**2+(other._downerr)**2)
        # r=math.sqrt((self._uperr)**2+(other._uperr)**2)
        data = self._mainnumber+other._mainnumber
        return RangeNumber(data, r, l)

    def __sub__(self, other):
        if not isinstance(other, RangeNumber):
            other = RangeNumber(other)
        r, l = self._get_lr([1, -1], [self, other])
        # l=-math.sqrt((self._downerr)**2+(other._downerr)**2)
        # r=math.sqrt((self._uperr)**2+(other._uperr)**2)
        data = self._mainnumber-other._mainnumber
        return RangeNumber(data, r, l)

    def __mul__(self, other):
        if not isinstance(other, RangeNumber):
            other = RangeNumber(other)
        r, l = self._get_lr([other.mainnum, self.mainnum],
                            [self, other])  # ?似乎与理论不同
        # l=-math.sqrt((self._downerr*other._mainnumber)**2+\
        #              (self._mainnumber*other._downerr)**2)
        # r=math.sqrt((self._uperr*other._mainnumber)**2+\
        #             (self._mainnumber*other._uperr)**2)
        data = self._mainnumber*other._mainnumber
        return RangeNumber(data, r, l)
    def __truediv__(self, other):

        if not isinstance(other, RangeNumber):
            # 处理除数的情况
            other = RangeNumber(other)
        leftdata = self.mainnum
        rightdata = other.mainnum
        md = float(self)/float(other)
        px1 = 1/rightdata
        px2 = -leftdata/(rightdata**2)
        u, d = self._get_lr([px1, px2], [self, other])
        return RangeNumber(md, u, d)

    def __pow__(self, other):
        if not isinstance(other, RangeNumber):
            other = RangeNumber(other)
        pl = (float(self)**(float(other)-1))*float(other)
        pr = (float(self)**float(other))*math.log(float(self))
        uperr, downerr = self._get_lr([pl, pr], [self, other])
        # downerr1=float(other)*(float(self)**(float(other)-1))*self._downerr
        # uperr1=float(other)*(float(self)**(float(other)-1))*self._uperr
        # # try:
        # #     downerr2=abs(math.log(abs(float(self))))*(float(self)**float(other))*other._downerr
        # #     uperr2=abs(math.log(abs(float(self))))*(float(self)**float(other))*other._uperr
        # # except:

        # # downerr=-math.sqrt(downerr1**2+downerr2**2)
        # # uperr=math.sqrt(uperr1**2+uperr2**2)
        # downerr=-math.sqrt(downerr1**2)
        # uperr=math.sqrt(uperr1**2)
        m = float(self)**float(other)
        return RangeNumber(m, uperr, downerr)
    # 以下是用于RangeNumber的math库中某些函数实现

    def log(x, base: float = math.e):
        """log 实现取对数的运算
            静态方法
        Parameters
        ----------
        x : RangeNumber
            求对数的数
        base : float, optional
            底数, 默认为自然对数

        Returns
        -------
        RangeNumber
            返回求对数后带有误差的值
        """
        p = 1/(float(x)*math.log(base))
        u, d = x._get_lr([p], [x])
        m = math.log(x, base)
        return RangeNumber(m, u, d)
###############################################################

    def fromlist(floatlist: float, uperr: float = 0, downerr: float = 0):
        """fromlist 对于相同误差快速初始化

        Parameters
        ----------
        floatlist : float
            输入的浮点数列表
        uperr : float, optional
            上误差, by default 0
        downerr : float, optional
            下误差, by default 0(同RangeNumber初始化)

        Returns
        -------
        List[RangeNumber]
            从浮点数列表直接获得的RangeNumber的列表
        """
        return [RangeNumber(k, uperr, downerr) for k in floatlist]


class RangeFromList(RangeNumber):
    """RangeFromList 采用从列表加入的方式获取多次测量所得平均以及相关误差
    """

    def __init__(self, datalist: list) -> None:
        """__init__ 用于初始化

        Parameters
        ----------
        datalist : List[RangeNumber]
            RangeNumber列表(有相同误差范围),作为多次测量结果
        """
        rlist = []
        mdl = []
        for d in datalist:
            if isinstance(d, RangeNumber):
                rlist.append(d)
            else:
                rlist.append(RangeNumber(d))
        errl=np.array([i.uperr for i in rlist])
        mnl=np.array([i.mainnum for i in rlist])
        d=np.sum(mnl/(errl**2))/np.sum(1/(errl**2))
        errau=np.sqrt(np.sum(((mnl-d)**2)/(errl**2)))
        errad1=np.sqrt(len(rlist)*(len(rlist)-1))
        errad2=np.sqrt(1/np.sum(errl**2))
        erra=errau/(errad1*errad2)
        errb=1/(np.sqrt(np.sum(1/errl**2)))
        err=np.sqrt(erra**2+errb**2)
        super().__init__(d,err)
        self._downerr,self._mainnumber,self._uperr=\
            (RangeNumber(d,err)).wholedata
        # lsum = RangeNumber(0)
        # for k in rlist:
        #     lsum += k
        # lsum = lsum/len(rlist)
        # if isinstance(lsum, RangeNumber):
        #     lsum._uperr = rlist[0]._uperr
        #     lsum._downerr = rlist[0]._downerr  # 多次测量时误差不叠加
        # for k in rlist:
        #     mdl.append((float(k)-float(lsum))**2)
        # gerr = math.sqrt(sum(mdl)/(len(rlist)*(len(rlist)-1)))
        # self._downerr, self._mainnumber, self._uperr =\
        #     (lsum+RangeNumber(0, gerr)).wholedata


if __name__ == "__main__":
    a1=RangeNumber(10,0.1)
    a2=RangeNumber(10,0.1)
    print(RangeFromList([a1,a2]))

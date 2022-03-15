# auto-Dataconsuming(0.0.4)
## 1.介绍
这个库分为两个部分RangeType和DataType
### 1.1 RangeType
可以用指定误差或给出多次测量得到的误差所给出**带有误差**的数据,可以在输出时对数据进行修约
### 1.2 DataType
可以通过输入数据字典和处理函数输出处理后的数据所产生的表格
## 2.安装
首先,在cmd中输入以下命令安装

`pip install DataConsumer`

其应当下载最新版本的DataConsumer,但请加以检查

其依赖库有`typing`,`pandas`,`numpy`和`collections`

在安装完成后,使用

`from DataConsumer.DataType import *`

导入所需的类型(已经包含了RangeType和DataType)
## 3.使用
### 3.1 RangeType
#### 3.1.1 RangeNumber类
这个类储存一个带有误差的数据.
##### 3.1.1.1 初始化
为了初始化一个RangeNumber对象,需要提供以下信息:量的值,上误差,下误差

例如,以下代码初始化了一个量值为10,上误差0.01,下误差-0.02的RangeNumber对象

`RangeNumber(10,0.01,-0.02)`

同时,一般上误差的值等于下误差的值,故我们可以忽略下误差,只输入上误差

例如,以下代码初始化了一个量值为10,上下误差绝对值均为0.01的RangeNumber对象

`RangeNumber(10,0.1)`

而在运算时,如果遇到了准确数,可以直接省去误差单参数初始化一个RangeNumber对象

----------
考虑到在使用时经常会遇到一批数据有相同的误差,所以可以使用RangeNumber.fromlist方法从浮点数列表直接获得RangeNumber的列表例如以下代码会返回一个RangeNumber列表

`RangeNumber.fromlist([1,2,3,4,5],0.01,-0.02)`

##### 3.1.1.2 支持操作
你可以读取一个RangeNUmber实例中的`wholedata`属性,其会储存完整的数据，以(downerr,mainnumber,uperr)的方式组织,但是你不可以修改它们

-----------
RangeNumber重载了加,减,乘,除和乘方运算符,但需要保证RangeNumber为左操作符,右操作符为RangeNumber或float均可

同时,RangeNumber.log(x,base)方法对RangeNumber可以求对数,用法与math.log相同,但x为一个RangeNumber对象

**注意**以上方法虽然也会对误差进行调整,但不能保证其准确性,需要加以检验!

-----------
如果用一个RangeNumber强制转换为float,这个float中会储存RangeNumber中的主值,因此你可以将RangeNumber直接用于math库中*注意此时其行为与float一致*

-----------
str(RangeNumber)会返回一个Latex字符串,例如以下代码

`a=RangeNumber(10,0.01,-0.2)`

`print(a)`
会输出:\$(10.0)^{0.01}_{-0.2}$

在Latex环境下,为$(10.0)^{0.01}_{-0.2}$

其自带数字修约
#### 3.1.2RangeFromList类
该类为RangeNumber的子类,有所不同的是其初始化方式
##### 3.1.2.1初始化
RangeFromList使用一个float或RangeNumber列表实现对同一量的多次测量,例如:

`RangeFromList([0.1,0.3,0.2])`

但在单次测量亦存在误差的情况下,可以结合使用fromlist方法,例如:

`RangeFromList(RangeNumber.fromlist([0.1,0.2,0.2],0.1))`

即可实现单次测量误差0.1,测量三次的效果

### 3.2DataType
#### 3.2.1DataConfig类
该类型用于储存数据的相关参数,目前仅含有对于单位和名称(及其缩写)的储存
##### 3.2.1.1初始化
其初始化函数需要按序接受:数据全称,数据的简称,单位 例如以下代码初始化了一个DataConfig类

`DataConfig("转动惯量","J","kgm^2")`

**数据简称和单位支持Latex语法**
##### 3.2.1.2 支持操作
tabular_format方法可以将一个数据信息形成一个表头格式的Latex风格字符串
例如上文所提到数据可以被转化为如下形式

转动惯量$J$($\mathbf{kgm^2}$)

但该操作主要是用于DataConsumer类型

#### 3.2.2DataConsumer类
该类型储存输入数据的词典和用于处理的函数,对数据进行格式化
##### 3.2.2.1初始化
初始化时,需要包括一个输入数据简称的字典(键为数据简称,值为数据列表)

一个用于处理数据的函数(参数名称为输入数据简称,对一条数据进行处理,返回一个包含以输出数据为值,输出数据简称为键的字典**如果希望将输入数据保留,则需要将输入数据的字典整合于其中**)

一个包括输入输出数据信息的字典(键为输入输出数据简称,值为输入输出数据的信息的DataConfig类实例)

##### 3.2.2.2支持操作
该类型的字符串转换方法可以输出一个Markdown风格的表格

##### 3.2.2.3实例
该实例使用的为3.13瑞利盘测量细线扭力系数的数据
```python
from DataConsumer.DataType import *
m2=RangeFromList([1.80,1.78,1.81])
m1=RangeFromList([1.43,1.43,1.41])
m3=RangeFromList([2.24,2.25,2.25])#对质量的三次测量
mlist=[m1,m2,m3]#不同质量圆片
rlist=RangeNumber.fromlist([40,45,50],0.01)#从已有数据得到半径
t1=RangeFromList([27.58/2,41.69/3])
t2=RangeFromList([59.5/4,57.07/4,62.41/4,58.88/4,53.46/5,46.5/3])
t3=RangeFromList([56.98/3,60.00/3,60.03/3])#对周期的多次测量
tlist=[t1,t2,t3]#不同质量圆片周期
idict={"m":mlist,"r":rlist,"t":tlist,"n":[1,2,3]}#输入数据内容
confd={"m":DataConfig("质量","m","kg"),\
       "n":DataConfig("编号","n"),\
       "r":DataConfig("半径","r","m"),\
       "T":DataConfig("周期","T","s"),\
       "J":DataConfig("转动惯量","J","kgm^2"),\
       "k":DataConfig("测得扭力系数","k","kgm^2s^{-2}")}#数据信息
def con(m,r,t,n):#处理函数
    pis=math.pi**2*4
    m/=1000
    r/=1000
    i=r*r*m/4
    k=(i/(t*t))*pis
    sigma=m/(r*r)
    return {"n":n,"m":m,"r":r,
            "T":t,"J":i,
            "k":k}
print(DataConsumer(idict,con,confd))#输出结果
```
运行该段代码,即可得到如下表格
|编号$n$|质量$m$($\mathbf{kg}$)|半径$r$($\mathbf{m}$)|周期$T$($\mathbf{s}$)|转动惯量$J$($\mathbf{kgm^2}$)|测得扭力系数$k$($\mathbf{kgm^2s^{-2}}$)|
|----|----|----|----|----|----|
|1|$(0.001423)^{7e-06}_{-7e-06}$|$(0.040000)^{1e-05}_{-1e-05}$|$(13.84)^{0.05}_{-0.05}$|$(5.693\times 10^{ -7 })^{3e-09}_{-3e-09}$|$(1.1729\times 10^{ -7 })^{8e-10}_{-8e-10}$|        
|2|$(0.001797)^{9e-06}_{-9e-06}$|$(0.045000)^{1e-05}_{-1e-05}$|$(14.3)^{0.7}_{-0.7}$|$(9.096\times 10^{ -7 })^{4e-09}_{-4e-09}$|$(1.76\times 10^{ -7 })^{1e-08}_{-1e-08}$|
|3|$(0.002247)^{3e-06}_{-3e-06}$|$(0.050000)^{1e-05}_{-1e-05}$|$(19.7)^{0.3}_{-0.3}$|$(1.4042\times 10^{ -6 })^{2e-09}_{-2e-09}$|$(1.433\times 10^{ -7 })^{3e-09}_{-3e-09}$|





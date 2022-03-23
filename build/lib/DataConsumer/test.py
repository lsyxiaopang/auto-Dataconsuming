from DataType import *
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题
tlist=[28.58,30,32.65,35.04,37.55,39.50,42.82,45.00,47.50,50.00]
rlist=[8934,8631,7986,7379,6845,6410,5713,5347,4972,4570]
inpd={"T":tlist,"R":rlist}
def cfunc(T,R):
    t=1/T
    lnr=math.log(R)
    return {"t":t,"lnr":lnr}
confdict={"t":DataConfig("温度倒数",r"\frac{1}{T}"),"lnr":DataConfig("电阻对数","\\ln r")}
k=DataConsumer(inpd,cfunc,confdict)
aw=plt.figure()

a=aw.add_subplot(111)
k.draw_fitted("t","lnr",a)
plt.show()
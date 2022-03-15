import math
from RangeType import *
def __getfloatlen(s:float):
    abss=abs(s)
    log=int(math.log10(abss))
    if log<=0 and math.log10(abss)<0:
        log-=1
    return log

def __confloat(s:float,err:float):
    ls=__getfloatlen(s)
    lerr=__getfloatlen(err)
    allwstr="%.{}g".format(ls-lerr+1)
    if abs(ls)<4:
        print(allwstr%s)
    else:
        cds=s/(10**ls)
        print(allwstr%cds+"\\times 10^{{ {} }}".format(ls))


print(RangeNumber(10,0.1))
print(int(0.9))
print(math.log10(0.9))
print(int(-0.04))

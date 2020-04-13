# simple EZ-diffusion model based on Wagenmakers et al, 2007
import numpy

def ezdiff(rt,correct,s=1.0):
    logit = lambda p:numpy.log(p/(1-p))

    assert len(rt)>0
    assert len(rt)==len(correct)
    
    assert numpy.max(correct)<=1
    assert numpy.min(correct)>=0
    
    pc=numpy.mean(correct)

    assert pc > 0
    
    # subtract or add 1/2 an error to prevent division by zero
    if pc==1.0:
        pc=1 - 1/(2*len(correct))
    if pc==0.5:
        pc=0.5 + 1/(2*len(correct))
    MRT=numpy.mean(rt)/1000 #from millisecond to second
    VRT=numpy.var(rt)/1000**2 #from squared millisecond to squared second

    assert VRT > 0
    
    r=(logit(pc)*(((pc**2) * logit(pc)) - pc*logit(pc) + pc - 0.5))/VRT
    v=numpy.sign(pc-0.5)*s*(r)**0.25
    a=(s**2 * logit(pc))/v
    y=(-1*v*a)/(s**2)
    MDT=(a/(2*v))*((1-numpy.exp(y))/(1+numpy.exp(y)))
    t=MRT-MDT

    return([MRT,VRT,pc,a,v,t])

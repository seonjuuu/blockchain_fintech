import time
import hashlib
import binascii
import random

#Domain parameters
p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798 
gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# y^2=x^3+ax+b
a=0
b=7


# 0 : on curve
# 1 : not on curve 
# 점 (x, y)가 타원곡선 위에 있는지 검사
def is_oncurve(x,y):
    t0 = (x**3+a*x+b)%p
    t1 = (y**2)%p
    if t0==t1:
        return 0
    else:
        return 1
    

# 이진 확장 유클리드 알고리즘으로 GCD와 계수(a, b) 계산
def bin_extgcd(x,y):
    tx = x
    ty = y
    g=1
    while tx&1==0 and ty&1==0:
        tx = tx>>1
        ty = ty>>1
        g = g<<1
    u = tx
    v = ty
    A = 1
    B = 0
    C = 0
    D = 1
    flag =0

    while flag==0:
        while u&1==0:
            u=u>>1
            if A&1==0 and B&1==0:
                A=A>>1
                B=B>>1
            else:
                A=(A+ty)>>1
                B=(B-tx)>>1
        while v&1==0:
            v=v>>1
            if C&1==0 and D&1==0:
                C=C>>1
                D=D>>1
            else:
                C=(C+ty)>>1
                D=(D-tx)>>1
        if u>=v:
            u=u-v
            A=A-C
            B=B-D
        else:
            v=v-u
            C=C-A
            D=D-B        
        if u==0:
            a=C
            b=D
            flag =1
        else:
            flag =0
    
    
    return a, b, (g*v)


# x^-1 mod q
# x의 모듈로 역원 계산
def mod_inv(x,q):
    xinv,_ , _ = bin_extgcd(x,q)
    return xinv


# R=P+Q
# 평면 좌표계에서 두 점 P, Q를 더함
def pt_add(px,py, qx,qy):
    #lambda = t0/t1
    t0 = (py-qy)
    t1 = (px-qx)
    t1inv = mod_inv(t1,p)# t1^-1

    t0 = (t0*t1inv)%p
    rx = (t0**2-px-qx)%p
    ry = (t0*(px-rx)-py)%p
    return rx, ry


# R=2P
# 평면 좌표계에서 점 P를 두 배로 만듦 (2P)
def pt_dbl(px, py):
    #3px^2
    t0 = px**2  #px^2
    t1 = t0+t0 # 2px^2
    t1 = (t1 + t0)%p #3px^2

    t0 = (py+py)%p
    t0inv = mod_inv(t0, p)
    #t0*t0inv ==1
    #print("chk: ",(t0*t0inv)%p)
    t0 = (t1*t0inv)%p

    rx = (t0**2-px-px)%p
    ry = (t0*(px-rx)-py)%p

    return rx, ry


# 프로젝티브 좌표계에서 점 P의 두 배 연산
def pt_dbl_proj(x,y,z):
    rx = 2*x*y*z*(9*(x**3)-8*(y**2)*z)
    rx = rx%p

    ry = -27*(x**6)+36*(x**3)*(y**2)*z-8*(y**4)*(z**2)
    ry = ry%p

    rz = 8*(y**3)*(z**3)
    rz = rz%p

    return rx, ry, rz


# 프로젝티브 좌표계에서 두 점 P + Q 연산
def pt_add_proj(X,Y,Z, x,y,z):

    oX = (Z*x - X*z)*(-((Z*x)**3 - X*((Z*x)**2)*z - (Z**3)*(y**2)*z - (X**2)*Z*x*(z**2) + 2*Y*(Z**2)*y*(z**2) + (X*z)**3 - (Y**2)*Z*(z**3)))
    oY = ((Z**4)*(x**3)*y - 2*Y*(Z**3)*(x**3)*z - (Z**4)*(y**3)*z + 3*X*Y*(Z**2)*(x**2)*(z**2) - 3*(X**2)*(Z**2)*x*y*(z**2) + 3*Y*(Z**3)*(y**2)*(z**2) + 2*(X**3)*Z*y*(z**3) - 3*(Y**2)*(Z**2)*y*(z**3) - (X**3)*Y*(z**4) + (Y**3)*Z*(z**4))
    oZ = ((Z*x - X*z)**3*Z*z)

    oX=oX%p
    oY=oY%p
    oZ=oZ%p

    return oX, oY, oZ

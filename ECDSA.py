import time
import random
import hashlib

#Domain parameters
p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798 
gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# y^2=x^3+ax+b
a=0
b=7

def is_oncurve(x,y):
    t0=(x**3+a*x+b)%p
    t1 = (y**2)%p
    if t0==t1:
        return 0
    else:
        return 1
    
def bin_extgcd(x,y):
    tx=x
    ty=y
    g=1
    while(tx&1==0 and ty&1==0):
        tx=tx>>1           # /2 = >>1
        ty=ty>>1
        g=g<<1             # *2 = <<1
    u=tx
    v=ty 
    A=1 
    B=0
    C=0
    D=1
    flag =0
    while (flag==0):        
        while(u&1==0):       # %2 = &1
            u=u>>1
            if(A&1==0 and B&1==0):
                A=A>>1
                B=B>>1
            else:
                A=(A+ty)>>1
                B=(B-tx)>>1
        while(v&1==0):        # %2 = &1
            v=v>>1
            if(C&1==0 and D&1==0):
                C=C>>1
                D=D>>1
            else:
                C=(C+ty)>>1
                D=(D-tx)>>1
        if(u>=v):
            u=u-v
            A=A-C
            B=B-D
        else:
            v=v-u
            C=C-A
            D=D-B
        
        if(u==0):
            a=C
            b=D
            flag=1         # while문 나감
        else:
            flag=0


    return a,b,(g*v)

# x^-1 mod q = xinv
def mod_inv(x,q):
    xinv,_,_ = bin_extgcd(x,q)  # '_'는 사용되지 않는 변수
    return (xinv)

print(mod_inv(3,7))
            

#R=P+Q
def pt_add(px,py,qx,qy):
    t0=(py-qy)
    t1=(px-qx)
    t1inv=mod_inv(t1,p) #(t1^-1)mod p
    
    t0=(t0*t1inv)%p  #lamda
    
    rx=(t0**2-px-qx)%p
    ry=(t0*(px-rx)-py)%p
    return rx, ry

#R=2P
#lamda = (t0/t1)modp = (t0*t^-1)modp

def pt_dbl(px,py):
    #3px^2(A생략)
    t0=px**2 #px^2
    t1=t0+t0 #2px^2
    t1=(t1+t0)%p #3px^2

    t0=(py+py)%p  #2py
    t0inv = mod_inv(t0,p)
    #chk : t0*t0inv == 1
    print("chk: ", (t0*t0inv)%p)
    t0 =(t1*t0inv)%p
    
    rx=(t0**2-px-px)%p
    ry=(t0*(px-rx)-py)%p
    
    return rx, ry

def pt_dbl_prdj(x,y,z):
    rx = 2*x*y*z*(9*(x**3)-8*(y**2)*z)
    rx = rx%p
    
    ry = -27*(x**6)+36*(x**3)*(y**2)*z-8*(y**4)*(z**2)
    ry = ry%p
    
    rz = 8*(y**3)*(z**3)
    rz = rz%p
    
    return rx, ry, rz

def pt_add_proj(X,Y,Z, x,y,z):
    
    oX = (Z*x - X*z)*(-((Z*x)**3 - X*((Z*x)**2)*z - (Z**3)*(y**2)*z - (X**2)*Z*x*(z**2) + 2*Y*(Z**2)*y*(z**2) + (X*z)**3 - (Y**2)*Z*(z**3)))

    oY = ((Z**4)*(x**3)*y - 2*Y*(Z**3)*(x**3)*z - (Z**4)*(y**3)*z + 3*X*Y*(Z**2)*(x**2)*(z**2) - 3*(X**2)*(Z**2)*x*y*(z**2) + 3*Y*(Z**3)*(y**2)*(z**2) + 2*(X**3)*Z*y*(z**3) - 3*(Y**2)*(Z**2)*y*(z**3) - (X**3)*Y*(z**4) + (Y**3)*Z*(z**4))

    oZ = ((Z*x - X*z)**3*Z*z)

    oX=oX%p

    oY=oY%p

    oZ=oZ%p

    return oX, oY, oZ

# 점p = (X,Y,Z)
def kmul(k, X, Y, Z):
    tx = X
    ty = Y
    tz = Z
    kbit = k.bit_length()
    i = 1
    i = i<<(kbit-2)
    while(i != 0):
        chk = (k&i)
        tx, ty, tz = pt_dbl_prdj(tx, ty, tz) # 2배
        if(chk): #chk != 0, 현재 비트는 1
            tx, ty, tz = pt_add_proj(tx, ty, tz, X, Y, Z) # 1이면 점p 더하기
            #print("bit : 1")
        i = i >> 1  # 오른쪽으로 이동
    
    return tx, ty, tz

# check(rx와 chk가 같은지)
rx,ry = pt_dbl(gx,gy)
X,Y,Z = pt_dbl_prdj(gx,gy,1)
zinv = mod_inv(Z,p)
chk = (X*zinv)%p

print("rx:",rx)
print("proj :",chk)

#[23]p kmul과 같은지 비교하기위하여
rx, ry, rz = pt_dbl_prdj(gx, gy, 1) #2p
rx, ry, rz = pt_dbl_prdj(rx, ry, rz) #4p
rx, ry, rz = pt_add_proj(rx, ry, rz, gx, gy, 1) #5p
rx, ry, rz = pt_dbl_prdj(rx, ry, rz) #10p
rx, ry, rz = pt_add_proj(rx, ry, rz, gx, gy, 1) #11p
rx, ry, rz = pt_dbl_prdj(rx, ry, rz) #22p
rx, ry, rz = pt_add_proj(rx, ry, rz, gx, gy, 1) #23p

zinv = mod_inv(rz,p)
chk = (rx*zinv)%p
print("[23]P x :", chk)

#kmul(23,gx,gy,1)
X,Y,Z = kmul(23,gx,gy,1)
zinv = mod_inv(Z,p)
chk = (X*zinv)%p
print("[23]P kmul:",chk)


### ECDSA ### 
def ecdsa_keygen() :
    # 개인키 선택
    d = random.randrange(1,n)
    # 공개키 연산 Q = [d]G
    X, Y, Z = kmul(d, gx, gy, 1)
    zinv = mod_inv(Z,p)
    
    Qx=(X*zinv)%p
    Qy=(Y*zinv)%p
    
    return d, Qx, Qy

# 키 생성
d, Qx, Qy = ecdsa_keygen()

def ecdsa_siggen(msg,d):
    encode_msg=msg.encode()
    msgdigest = hashlib.sha256(encode_msg).hexdigest()
    print(msgdigest)
    print(type(msgdigest))
    e=int(msgdigest,16) # msgdigest를 16진수로 표현된 문자열을 10진수로 변환하여 e에 할당
    e=e%p
    
    flag=0
    while flag==0:        
        k = random.randrange(1,n)
        X, Y, Z = kmul(k, gx, gy, 1) #[k]G (G의 위수 = n => [n]G =0)
        zinv = mod_inv(Z,p) 
        x1 = (X*zinv)%p
        y1 = (Y*zinv)%p
        
        r = x1%n
        kinv = mod_inv(k,n)
        s = kinv*(e+r*d)%n
        if r==0: 
            flag=0
        elif s==0:
            flag =0
        else:
            flag =1
    
    return r, s

    
r, s = ecdsa_siggen("abc",d)   #메세지:'abc' , 개인키:d => 서명값 : (r,s)

def ecdsa_verify(m,r,s,qx,qy):
    emsg = m.encode()
    h = hashlib.sha256(emsg).hexdigest()
    h = int(h,16)
    sinv = mod_inv(s,n)
    u1 = (h*sinv)%n
    u2 = (r*sinv)%n
    X, Y, Z = kmul(u1, gx, gy, 1)
    X2,Y2,Z2 = kmul(u2,qx,qy,1)
    Zinv = mod_inv(Z,p)
    u1x = (X*Zinv)%p
    u1y = (Y*Zinv)%p
def ecdsa_sigver(msg,r,s,Qx,Qy):
    ret = 0
    #  r과 s 중 하나라도 주어진 범위에 속하지 않으면 ret 값을 0으로 설정하고 반환(둘다 범위안에 속한다면 return ret=0)
    if not(1<=r<=n-1 or 1<=s<=n-1):
        ret =0 
        return ret
    else:
        #step 2
        encode_msg=msg.encode()
        msgdigest = hashlib.sha256(encode_msg).hexdigest()
        e=int(msgdigest,16)
        z=e%p
        #step 3
        sinv = mod_inv(s,n)
        u1 = (z*sinv)%n
        u2 = (r*sinv)%n
        #step 4
        u1x, u1y, u1z = kmul(u1,gx,gy,1)        
        u2x, u2y, u2z = kmul(u2,Qx,Qy,1)
        X, Y, Z = pt_add_proj(u1x, u1y, u1z, u2x, u2y, u2z)
        zinv = mod_inv(Z,p)
        x1 = (X*zinv)%p
        
        chk = x1%n
        if chk == r:
            ret = 1
        else:
            ret = 0
        
        return ret
    
# 키 생성
d, Qx, Qy = ecdsa_keygen()
# 서명생성
r,s = ecdsa_siggen("abc",d)
# 서명검증
ret = ecdsa_sigver("abc", r, s, Qx,Qy)
print("verification:",ret)
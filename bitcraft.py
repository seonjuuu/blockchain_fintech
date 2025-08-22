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
# 점 (x, y)가 타원곡선 위에 있는지 판별
def is_oncurve(x,y):
    t0 = (x**3+a*x+b)%p
    t1 = (y**2)%p
    if t0==t1:
        return 0
    else:
        return 1
    

#확장 유클리드 알고리즘 GCD 및 계수 계산
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
# x의 모듈러 역원
def mod_inv(x,q):
    xinv,_ , _ = bin_extgcd(x,q)
    return xinv

#print(mod_inv(3,7))

#R=P+Q
def pt_add(px,py, qx,qy):
    #lambda = t0/t1
    t0 = (py-qy)
    t1 = (px-qx)
    t1inv = mod_inv(t1,p)# t1^-1

    t0 = (t0*t1inv)%p
    rx = (t0**2-px-qx)%p
    ry = (t0*(px-rx)-py)%p
    return rx, ry


#R=2P
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


# 프로젝티브 좌표계에서 두 배 연산 수행
def pt_dbl_proj(x,y,z):
    rx = 2*x*y*z*(9*(x**3)-8*(y**2)*z)
    rx = rx%p

    ry = -27*(x**6)+36*(x**3)*(y**2)*z-8*(y**4)*(z**2)
    ry = ry%p

    rz = 8*(y**3)*(z**3)
    rz = rz%p

    return rx, ry, rz


# 프로젝티브 좌표계에서 두 점 덧셈 수행
def pt_add_proj(X,Y,Z, x,y,z):

    oX = (Z*x - X*z)*(-((Z*x)**3 - X*((Z*x)**2)*z - (Z**3)*(y**2)*z - (X**2)*Z*x*(z**2) + 2*Y*(Z**2)*y*(z**2) + (X*z)**3 - (Y**2)*Z*(z**3)))
    oY = ((Z**4)*(x**3)*y - 2*Y*(Z**3)*(x**3)*z - (Z**4)*(y**3)*z + 3*X*Y*(Z**2)*(x**2)*(z**2) - 3*(X**2)*(Z**2)*x*y*(z**2) + 3*Y*(Z**3)*(y**2)*(z**2) + 2*(X**3)*Z*y*(z**3) - 3*(Y**2)*(Z**2)*y*(z**3) - (X**3)*Y*(z**4) + (Y**3)*Z*(z**4))
    oZ = ((Z*x - X*z)**3*Z*z)

    oX=oX%p
    oY=oY%p
    oZ=oZ%p

    return oX, oY, oZ


# 스칼라 곱 연산: [k]P 계산
def kmul(k, X, Y, Z):
    tx = X
    ty = Y
    tz = Z
    kbit = k.bit_length()
    i = 1
    i = i <<(kbit-2)
    while(i!=0):
        chk = (k&i)
        tx, ty, tz = pt_dbl_proj(tx, ty, tz)
        if(chk): #chk!=0, 현재 비트 1
            tx, ty, tz = pt_add_proj(tx, ty, tz,X, Y,Z)
    #        print("bit :  1")
        i= i>>1
    return tx, ty, tz


# 정수 n을 little-endian hex 문자열로 변환
def dec_to_little_endian_str(n,tlen):
    n_str = hex(n)
    n_str = n_str[2:]
    while len(n_str)  != (tlen<<1):
        n_str = '0' + n_str
    ret=''
    for i in range(len(n_str)-1,-1,-2):
        ret = ret+n_str[i-1]
        ret = ret+n_str[i]
    return ret


# hex 문자열을 little-endian으로 변환
def hex_to_little_endian_str(n,tlen):
    n_str = n
    while len(n_str)  != (tlen):
        n_str = '0' + n_str
    ret=''
    for i in range(len(n_str)-1,-1,-2):
        ret = ret+n_str[i-1]
        ret = ret+n_str[i]
    return ret


# Base58 주소를 hex로 디코딩
def base58_to_hex(n):
    b58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    tmp = n
    tmp = tmp[::-1]
    exp =0
    ret =0
    for i in tmp:
        idx = b58.find(i)
        ret = ret + idx*(58**exp)
        exp=exp+1
    return hex(ret)[2:]


# Base58 지갑 주소에서 공개키 해시 부분 추출
def wallet_to_pub(n):
    pub = n[2:len(n)-8]
    return pub , (len(pub)>>1)


### ECDSA ###

#ECDSA 개인키 생성 및 공개키 계산
def ecdsa_keygen():
    # 개인키 선택
    d = random.randrange(1,n)
    # 공개키 연산 Q = [d]G
    X,Y,Z = kmul(d, gx, gy, 1)
    zinv=mod_inv(Z,p)

    Qx=(X*zinv)%p
    Qy=(Y*zinv)%p
    
    return d, Qx, Qy


# 메시지 m을 개인키 d로 ECDSA 서명
def ecdsa_siggen(m, d):
    emsg = m.encode()
    h = hashlib.sha256(emsg).hexdigest()
    h = int(h,16)
    flag=0
    while flag==0:
        k = random.randrange(1, n) #step 2
        X,Y,Z = kmul(k, gx, gy, 1) #X/Z, Y/Z
        zinv=mod_inv(Z,p) #Z^-1
        x1 = (X*zinv)%p
        r = x1%n
        if r!=0:
            flag = 1
            kinv = mod_inv(k,n)
            s = (h+r*d)%n
            s = (s*kinv)%n
            if s!=0:
                flag =1
            else:
                flag=0
    return r,s


# 공개키로 ECDSA 서명 검증 수행
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
    Zinv = mod_inv(Z2,p)
    u2x = (X2*Zinv)%p
    u2y = (Y2*Zinv)%p
    rx, _ = pt_add(u1x,u1y,u2x,u2y)
    if (r%n) ==(rx%n):
        return 1
    else:
        return 0
    

def form_length(n):
    tmp=n
    while len(tmp)!=64:
        tmp = '0'+tmp
    return tmp


##5시작
incnt = 2
inn0=['7b46bff49c3eeb7b10c37aca0b930e06bae473f99f34e9c9f45451653847ed6b',0]
inn1=['7b46bff49c3eeb7b10c37aca0b930e06bae473f99f34e9c9f45451653847ed6b',1]

# 트랜잭션 입력 부분(이전 UTXO 등) 구성
def tx_in(incnt, *inn):
    ver='01000000' #버전값
    in_str = dec_to_little_endian_str(incnt,1)
    head = ver+in_str
    ret=[]
    for i in range(0, incnt):
        a=""
        tmp=hex_to_little_endian_str(inn[i][0],len(inn[i][0]))
        a=a+tmp
        tmp=dec_to_little_endian_str(inn[i][1],4)
        a=a+tmp
        ret.append(a)
    return head, ret
#print(tx_in(incnt,inn0,inn1))

#
out1=[0.03664619,'mt6URnuGsPZxDAPYLEBypA4BBbZ36cH9yv']
out2=[0.0172902,'mvqjQUERnKZbH9knpka5HEsQ9eraQrEQQa']

def tx_out(outcnt, *out):
    ret=dec_to_little_endian_str(outcnt,1)
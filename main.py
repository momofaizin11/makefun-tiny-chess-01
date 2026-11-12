# tiny-chess-01: alpha-beta engine, stdlib only.
import json,os,sys,urllib.request as U
NB=60000;N=0
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':30000}
D=(1,-1,10,-10,11,9,-11,-9)
J=(21,19,12,8,-8,-12,-19,-21)
X=Exception
def po(p,d):
 u=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL unset")
 try:return json.load(U.urlopen(U.Request(u+p,json.dumps(d).encode(),{"content-type":"application/json"})))
 except U.HTTPError as e:sys.exit(e.code)
def F(s):
 a=s.split();b=['.'if 20<=i<100 and 0<i%10<9 else'#'for i in range(120)]
 for i,r in enumerate(a[0].split('/')):
  f=0
  for c in r:
   if c>'9':b[(9-i)*10+f+1]=c;f+=1
   else:f+=int(c)
 return b,int(a[1]=='b'),-1 if a[3]=='-'else(int(a[3][1])+1)*10+ord(a[3][0])-96
def A(b,t,c):
 z=9-18*c
 if b[t-z]=='Pp'[c]or b[t-z-2+4*c]=='Pp'[c]:return 1
 for d in J:
  if b[t+d]=='Nn'[c]:return 1
 for d in D:
  if b[t+d]=='Kk'[c]:return 1
 for k,d in enumerate(D):
  x=t
  while 1:
   x+=d;q=b[x]
   if q=='.':continue
   if q<'A':break
   if q in('BQbq'if k>3 else'RQrq')[2*c:2*c+2]:return 1
   break
 return 0
def K(b,s,ep,m):
 f,t,p=m;b=b[:];q=b[t];x=b[f];u=x.upper();b[f]='.'
 if u=='K'and abs(f-t)==2:
  if t>f:b[t-1]=b[t+1];b[t+1]='.'
  else:b[t+1]=b[t-2];b[t-2]='.'
 if u=='P'and(t-f)%10 and q=='.':b[t-10+20*s]='.'
 b[t]=(p.upper()if s==0 else p)if p else x
 return b,1-s,(f+t)//2 if u=='P'and abs(t-f)==20 else-1
def G(b,s,ep,u):
 m=[];O='pnbrqk'if s==0 else'PNBRQK';e=1-2*s
 for i,x in enumerate(b):
  if x<'A'or x in O:continue
  v=x.upper();r=i//10
  if v=='P':
   d=10*e;y=i+d
   if b[y]=='.'and(u<1 or y//10 in(2,9)):
    m+=[(i,y,z)for z in'qrbn']if y//10 in(2,9)else[(i,y,'')]
    if r==(3,8)[s]and b[y+d]=='.':m.append((i,y+d,''))
   for d in(9*e,11*e):
    t=i+d;q=b[t]
    if q in O:m+=[(i,t,z)for z in'qrbn']if t//10 in(2,9)else[(i,t,'')]
    elif t==ep:m.append((i,t,''))
  elif v in'NK':
   for d in(J if v=='N'else D):
    t=i+d;q=b[t]
    if q in O or(q=='.'and u<1):m.append((i,t,''))
  else:
   for k,d in enumerate(D):
    if v!='Q'and(v=='B')==(k<4):continue
    t=i
    while 1:
     t+=d;q=b[t]
     if q=='.':
      if u<1:m.append((i,t,''))
     else:
      if q in O:m.append((i,t,''))
      break
  if v=='K'and u<1:
   z=21+70*s
   if i==z+4:
    for a,o,c,h,rk,ds in((5,7,4,7,7,6),(1,4,2,5,0,2)):
     if b[z+rk]=='Rr'[s]and all(b[z+x]=='.'for x in range(a,o))and not any(A(b,z+x,1-s)for x in range(c,h)):m.append((z+4,z+ds,''))
 r=[];k=b.index('Kk'[s])
 for x in m:
  n=K(b,s,ep,x)[0]
  if not A(n,x[1]if x[0]==k else k,1-s):r.append(x)
 return r
def E(b):
 s=0;L=[[0]*8,[0]*8];B=[0,0]
 for i,x in enumerate(b):
  if x<'A':continue
  f=i%10-1;r=i//10-2;v=x.upper();w=x>'Z';z=V[x.lower()]
  if v=='P':L[w][f]+=1;z+=8*r-8 if not w else 8*(6-r)
  elif v=='K':z=-10*(r if not w else 7-r)
  else:
   if v=='B':B[w]+=1
   if v<'P':z+=8-abs(f-3)-abs(r-3)
  s+=z if not w else-z
 for w in(0,1):
  q=1-2*w
  if B[w]>1:s+=30*q
  for n in L[w]:
   if n>1:s+=12*q
 return s
def S(b,m):
 f,t,p=m;q=b[t]
 v=V[q.lower()]if q>'.'else 0
 if p:v+=V[p]
 return v*8-V[b[f].lower()]//8
def B(b,s,ep,d,al,be):
 global N
 N+=1
 if N>NB:raise X
 e=E(b)*(-1)**s
 if d<1:
  if e>=be:return e
  if e>al:al=e
  ms=G(b,s,ep,1);bs=e
 else:
  ms=G(b,s,ep,0)
  if not ms:return -30000 if A(b,b.index('Kk'[s]),1-s)else 0
  bs=-99999
 for m in sorted(ms,key=lambda m:-S(b,m)):
  v=-B(*K(b,s,ep,m),d-1,-be,-(al if al>bs else bs))
  if v>bs:bs=v
  if bs>al:al=bs
  if al>=be:break
 return al if d<1 else bs
def P(fs,lm):
 global N
 b,s,ep=F(fs);N=0;bm=lm[0]
 L=[(b,s,ep,((int(u[1])+1)*10+ord(u[0])-96,(int(u[3])+1)*10+ord(u[2])-96,u[4:5]),u)for u in lm]
 for d in range(1,12):
  al=-99999;cb=bm
  try:
   for nb,ns,ne,m,u in L:
    v=-B(*K(nb,ns,ne,m),d-1,-99999,-al)
    if v>al:al=v;cb=u
  except X:break
  bm=cb
 return bm
def R():
 W=sys.stderr.write
 while 1:
  g=po("/game",{})
  if g["status"]!="your_move":break
  while g["status"]=="your_move":g=po("/move",{"game":g["game"],"move":P(g["fen"],g["legal_moves"])})
 W("%s/%s/%s\n"%(g.get('wins'),g.get('draws'),g.get('losses')))
R()

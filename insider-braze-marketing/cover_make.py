import sys
from PIL import Image, ImageDraw, ImageFont
S=2; W,H=1600*S,2560*S
BG=(246,243,236); NAVY=(22,34,64); MUTED=(92,104,128)
CORAL=(234,98,76); TEAL=(28,150,140); AMBER=(232,160,40); BLUE=(66,110,214); LINE=(196,200,210)
F="/mnt/c/Windows/Fonts/"
bold=lambda s: ImageFont.truetype(F+"malgunbd.ttf", s*S)
reg=lambda s: ImageFont.truetype(F+"malgun.ttf", s*S)
im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
X=140*S
d.rectangle([X,200*S,X+120*S,212*S],fill=CORAL)
y=270*S
for line in ["Insider One과","Braze로 시작하는","CRM 마케팅"]:
    d.text((X,y),line,font=bold(148),fill=NAVY); y+=200*S
y+=40*S
d.text((X,y),"보내기 전에 설계하라",font=reg(72),fill=MUTED)

def bez(p0,p1,p2,p3,n=240):
    out=[]
    for i in range(n+1):
        t=i/n
        out.append(((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0],
                    (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]))
    return out
def P(x,y): return (x*S,y*S)
def curve(a,b,color,w=10):
    mx=(a[0]+b[0])/2
    d.line(bez(P(*a),P(mx,a[1]),P(mx,b[1]),P(*b)),fill=color,width=w*S,joint="curve")

start=(220,1760); split=(540,1760); end=(1380,1760)
branches=[((900,1460),CORAL),((900,1760),TEAL),((900,2060),AMBER)]
d.line([P(*start),P(*split)],fill=NAVY,width=10*S)
for b,c in branches:
    curve(split,b,c); curve(b,end,c)
# dashed "not sent" holdout path
for i in range(15):
    x0=540+i*58
    d.line([P(x0,2250),P(x0+28,2250)],fill=LINE,width=6*S)

def node(c,r,fill,ring=None):
    x,y=P(*c); r*=S
    if ring: d.ellipse([x-r-14*S,y-r-14*S,x+r+14*S,y+r+14*S],fill=BG,outline=ring,width=6*S)
    d.ellipse([x-r,y-r,x+r,y+r],fill=fill)
node(start,34,NAVY); node(split,26,NAVY,ring=NAVY)
for b,c in branches: node(b,46,c)
node(end,52,NAVY,ring=BLUE)

def env(cx,cy):
    x,y=P(cx,cy); w,h=32*S,22*S
    d.rectangle([x-w//2,y-h//2,x+w//2,y+h//2],outline=BG,width=4*S)
    d.line([(x-w//2,y-h//2),(x,y+3*S),(x+w//2,y-h//2)],fill=BG,width=4*S)
def chat(cx,cy):
    x,y=P(cx,cy)
    d.rounded_rectangle([x-18*S,y-15*S,x+18*S,y+9*S],radius=6*S,outline=BG,width=4*S)
    d.polygon([(x-9*S,y+9*S),(x-13*S,y+20*S),(x+1*S,y+9*S)],fill=BG)
def phone(cx,cy):
    x,y=P(cx,cy)
    d.rounded_rectangle([x-13*S,y-21*S,x+13*S,y+21*S],radius=4*S,outline=BG,width=4*S)
    d.ellipse([x-3*S,y+10*S,x+3*S,y+16*S],fill=BG)
phone(*branches[0][0]); env(*branches[1][0]); chat(*branches[2][0])
x,y=P(*end)
d.line([(x-18*S,y),(x-5*S,y+14*S),(x+20*S,y-14*S)],fill=BG,width=7*S,joint="curve")

d.line([P(140,2400),P(1460,2400)],fill=LINE,width=2*S)
d.text((X,2430*S),"Toby-AI",font=reg(52),fill=NAVY)
im=im.resize((1600,2560),Image.LANCZOS)
im.save(sys.argv[1])
im.resize((200,320),Image.LANCZOS).save(sys.argv[2])
print(im.size)

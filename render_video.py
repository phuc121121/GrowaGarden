import math, sys, subprocess, numpy as np, wave, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT=sys.argv[1]; PREVIEW=len(sys.argv)>2
W,H=1920,1080; VW,VH=960,540; FPS=24
NAVY=(11,31,68); GOLD=(242,182,50); WHITE=(245,245,245)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FS='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def F(s,b=True,serif=False): return ImageFont.truetype(FS if serif else (FB if b else FR),s)
def new(bg): 
    im=Image.new('RGB',(W,H),bg); return im,ImageDraw.Draw(im)
def rr(d,box,r,fill,outline=None,w=1): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=w)
def txt(d,xy,s,font,fill,anchor='la'): d.text(xy,s,font=font,fill=fill,anchor=anchor)
def logo(d,x,y,s,dark=False):
    rr(d,(x,y,x+s,y+s),s//5,WHITE if dark else NAVY)
    c=NAVY if dark else WHITE
    d.polygon([(x+s*.5,y+s*.18),(x+s*.82,y+s*.82),(x+s*.68,y+s*.82),(x+s*.5,y+s*.4),(x+s*.32,y+s*.82),(x+s*.18,y+s*.82)],fill=NAVY if dark else WHITE)
    cx,cy,r=x+s*.5,y+s*.62,s*.12
    pts=[(cx+(r if i%2==0 else r*.45)*math.sin(i*math.pi/5),cy-(r if i%2==0 else r*.45)*math.cos(i*math.pi/5)) for i in range(10)]
    d.polygon(pts,fill=GOLD)
def wordmark(d,x,y,size,dark=False):
    f=F(size); a="APPLY"; w=d.textlength(a,font=f)
    txt(d,(x,y),a,f,WHITE if dark else NAVY); txt(d,(x+w+size*.1,y),"SPARK",f,GOLD)
def person(d,x,y,s,shirt,skin=(236,196,160),hair=(25,25,30),glasses=False,tie=None,sit=True):
    # x,y = center of head-top; torso below
    hx,hy=x,y+50*s
    d.rounded_rectangle((x-75*s,y+105*s,x+75*s,y+420*s),int(40*s),fill=shirt)
    if tie: d.polygon([(x,y+110*s),(x-14*s,y+140*s),(x,y+260*s),(x+14*s,y+140*s)],fill=tie)
    d.rectangle((x-18*s,y+90*s,x+18*s,y+115*s),fill=skin)
    d.ellipse((hx-48*s,hy-52*s,hx+48*s,hy+52*s),fill=skin)
    d.pieslice((hx-52*s,hy-62*s,hx+52*s,hy+40*s),180,360,fill=hair)
    for ex in(-18,18): d.ellipse((hx+ex*s-5*s,hy-2*s,hx+ex*s+5*s,hy+8*s),fill=(30,30,30))
    d.arc((hx-14*s,hy+14*s,hx+14*s,hy+34*s),20,160,fill=(150,70,60),width=max(2,int(3*s)))
    if glasses:
        for ex in(-18,18): d.ellipse((hx+ex*s-15*s,hy-12*s,hx+ex*s+15*s,hy+18*s),outline=(20,20,20),width=max(2,int(3*s)))
        d.line((hx-3*s,hy+2*s,hx+3*s,hy+2*s),fill=(20,20,20),width=max(2,int(3*s)))
def shelf(d,x0,y0,x1,y1,seed=1):
    rng=np.random.RandomState(seed); d.rectangle((x0,y0,x1,y1),fill=(40,28,22))
    for row in range(4):
        yy=y0+10+row*(y1-y0)//4; xx=x0+10
        d.rectangle((x0,yy+(y1-y0)//4-16,x1,yy+(y1-y0)//4-8),fill=(70,48,34))
        while xx<x1-30:
            w=int(rng.randint(18,38)); h=int(rng.randint(70,(y1-y0)//4-30)); c=tuple(int(v) for v in rng.randint(60,190,3))
            d.rectangle((xx,yy+(y1-y0)//4-16-h,xx+w,yy+(y1-y0)//4-16),fill=c); xx+=w+3
def laptop(d,x,y,w,h,screen=(210,225,240)):
    d.polygon([(x-w*.55,y+h),(x+w*.55,y+h),(x+w*.5,y+h+30),(x-w*.5,y+h+30)],fill=(90,95,105))
    rr(d,(x-w/2,y,x+w/2,y+h),12,(60,64,72)); rr(d,(x-w/2+12,y+12,x+w/2-12,y+h-12),6,screen)
# ---------- sets ----------
def set_room(p=0):
    im,d=new((20,32,44)); shelf(d,0,0,1000,820,3); d.rectangle((1000,0,W,820),fill=(28,44,60))
    d.ellipse((1450,150,1550,250),fill=(255,214,140)); d.rectangle((1494,250,1506,520),fill=(60,60,60))
    d.rectangle((0,820,W,H),fill=(18,18,22)); d.rectangle((300,720,1700,790),fill=(86,52,34)); d.rectangle((340,790,380,1080),fill=(70,42,28)); d.rectangle((1620,790,1660,1080),fill=(70,42,28))
    person(d,980,360,1.15,(235,240,248),glasses=True,tie=NAVY)
    laptop(d,1180,560,420,240,(200,220,245)); 
    for i,c in enumerate([(255,220,90),(255,150,170),(140,230,170)]): d.rectangle((560+i*60,520+i*25,610+i*60,570+i*25),fill=c)
    d.rectangle((420,745,560,790),fill=(220,60,60)); return im
def set_top(p=0):
    im,d=new((120,78,50)); rng=np.random.RandomState(5)
    for i in range(14):
        x,y=rng.randint(100,1700),rng.randint(60,900); c=(250,250,245) if i%3 else (255,225,110)
        sh=Image.new('RGBA',(220,260),(0,0,0,0)); ImageDraw.Draw(sh).rectangle((0,0,219,259),fill=c+(255,)); 
        for l in range(6): ImageDraw.Draw(sh).line((20,40+l*30,190,40+l*30),fill=(150,150,160,255),width=3)
        sh=sh.rotate(rng.randint(-40,40),expand=True); im.paste(sh,(x,y),sh)
    d=ImageDraw.Draw(im); laptop(d,960,330,700,420,(210,228,248)); rr(d,(1500,700,1640,840),20,(240,240,240)); d.ellipse((1515,715,1625,825),fill=(90,50,30))
    txt(d,(700,300),"IELTS?  deadline?  học bổng?",F(40),(200,40,40)); return im
def set_screen(p=0):
    im,d=new((16,20,28)); rr(d,(160,90,1760,990),24,(245,247,250))
    for i in range(12):
        c=(225,230,238) if i else (255,255,255); rr(d,(180+i*125,110,295+i*125,160),8,c); d.rectangle((200+i*125,130,260+i*125,138),fill=(150,160,175))
    for r in range(11):
        for c in range(9):
            col=(255,230,230) if (r*3+c)%7==0 else (255,255,255); d.rectangle((200+c*170,200+r*62,365+c*170,256+r*62),fill=col,outline=(205,210,220))
    txt(d,(210,205),"Deadline",F(26),(200,30,30)); txt(d,(540,331),"15/11   30/11   01/12",F(26),(200,30,30)); return im
def card(lines,sub=None,bg=NAVY):
    def f(p=0):
        im,d=new(bg); y=H//2-(len(lines)*90)//2-40
        for i,l in enumerate(lines): txt(d,(W//2,y+i*100),l,F(78,True),GOLD if i==0 and len(lines)>1 else WHITE,'mm')
        if sub: txt(d,(W//2,H//2+len(lines)*55+30),sub,F(40,False),(160,185,225),'mm')
        return im
    return f
def set_kitchen(p=0):
    im,d=new((196,150,106)); d.rectangle((0,0,W,700),fill=(214,176,130)); d.rectangle((1300,120,1760,520),fill=(250,230,170)); d.line((1530,120,1530,520),fill=(180,140,90),width=8)
    d.rectangle((0,700,W,H),fill=(130,92,60)); d.rectangle((200,760,1720,830),fill=(110,70,44))
    person(d,760,300,1.2,(90,120,150),skin=(226,180,140),hair=(120,120,125),glasses=True)
    rr(d,(900,640,1260,780),8,(245,245,240)); d.rectangle((900,640,1080,780),fill=NAVY); txt(d,(990,710),"TƯ VẤN",F(34),GOLD,'mm')
    rr(d,(1330,600,1470,800),14,(60,60,70)); rr(d,(1345,615,1455,660),4,(170,200,170)); txt(d,(1450,640),"???",F(26),(30,40,30),'rm')
    for i in range(3):
        for j in range(3): d.ellipse((1352+j*38,685+i*36,1376+j*38,709+i*36),fill=(200,200,205))
    d.ellipse((470,700,560,760),fill=(240,240,240)); return im
def set_calc(p=0):
    im,d=new((60,40,30)); rr(d,(560,100,1360,1000),50,(50,52,60)); rr(d,(620,170,1300,380),18,(165,200,165)); txt(d,(1270,275),"?,???,???",F(110),(30,50,30),'rm')
    for i in range(4):
        for j in range(4): rr(d,(630+j*170,430+i*130,760+j*170,540+i*130),22,(190,190,196) if j<3 else GOLD)
    return im
def set_class(p=0):
    im,d=new((196,210,196)); d.rectangle((250,120,1350,640),fill=(28,70,52),outline=(120,80,50),width=18)
    txt(d,(800,380),"Study Abroad 2027",F(70,False),(230,235,230),'mm')
    d.polygon([(1450,0),(1920,0),(1920,700),(1450,560)],fill=(255,240,190))
    d.rectangle((0,780,W,H),fill=(150,120,90))
    for i in range(4): d.rectangle((150+i*450,740,420+i*450,790),fill=(180,140,100)); d.rectangle((190+i*450,790,210+i*450,980),fill=(110,80,60))
    person(d,1180,300,1.25,(70,110,170),glasses=False,tie=None); d.rectangle((1130,520,1230,600),fill=(250,200,70)) 
    person(d,1620,520,.9,(60,70,90),hair=(20,20,20)); return im
def set_chalk(p=0):
    im,d=new((22,60,46)); s="applysparkvn.com"; n=int(len(s)*min(1,p*1.3))
    txt(d,(W//2,H//2),s[:n],F(120),GOLD,'mm')
    txt(d,(W//2,H//2-170),"→ Thử ngay",F(70,False),(230,235,230),'mm'); return im
def ui_frame(inner):
    def f(p=0):
        im,d=new((9,18,40)); 
        glow=Image.new('RGB',(W,H),(9,18,40)); gd=ImageDraw.Draw(glow); gd.ellipse((300,100,1620,980),fill=(60,50,20)); glow=glow.filter(ImageFilter.GaussianBlur(160)); im=glow; d=ImageDraw.Draw(im)
        rr(d,(220,110,1700,900),22,(245,247,250)); rr(d,(220,110,1700,170),22,(228,232,240)); 
        for i,c in enumerate([(240,100,90),(245,190,70),(100,200,110)]): d.ellipse((250+i*34,130,270+i*34,150),fill=c)
        rr(d,(420,125,1300,155),14,WHITE); txt(d,(440,140),"applysparkvn.com",F(22,False),(90,100,120),'lm')
        inner(d,p); return im
    return f
def nav(d):
    logo(d,250,190,56); wordmark(d,320,196,40)
    for i,t in enumerate(["Trường","Hạn nộp","Công cụ","Gói"]): txt(d,(1000+i*150,218),t,F(26,False),(70,80,100),'lm')
def ui_home(d,p):
    nav(d); txt(d,(260,380),"Thắp sáng tiềm năng",F(70),NAVY); txt(d,(260,490),"hồ sơ của bạn",F(70),GOLD)
    txt(d,(260,610),"Tìm trường, lưu danh sách, theo dõi hạn nộp.",F(34,False),(70,80,100))
    rr(d,(260,700,1000,780),40,WHITE,(200,205,215),3); txt(d,(300,740),"Tìm trường đại học...",F(32,False),(140,150,170),'lm'); rr(d,(1010,700,1220,780),40,NAVY); txt(d,(1115,740),"Tìm kiếm",F(32),WHITE,'mm')
    for i,(a,b) in enumerate([("Toàn cầu","tìm kiếm"),("Hạn nộp","nhắc nhở"),("Hồ sơ","phân tích")]):
        rr(d,(1250,330+i*130,1650,430+i*130),18,(255,248,230),GOLD,3); txt(d,(1280,365+i*130),a,F(34),NAVY,'lm'); txt(d,(1280,405+i*130),b,F(26,False),(90,100,120),'lm')
def ui_uni(d,p):
    nav(d); txt(d,(260,300),"Đại học mẫu · Overview",F(50),NAVY)
    for i,t in enumerate(["Overview","Rankings","Admissions","Costs","Scholarships","Deadlines"]):
        rr(d,(260+i*190,380,430+i*190,430),25,NAVY if i==int(p*6)%6 else (230,234,242)); txt(d,(345+i*190,405),t,F(24),WHITE if i==int(p*6)%6 else NAVY,'mm')
    for i in range(3):
        rr(d,(260+i*470,480,690+i*470,820),18,WHITE,(210,215,225),3); txt(d,(290+i*470,520),["QS Rank","Học phí","Hạn nộp"][i],F(30),NAVY); d.rectangle((290+i*470,580,290+i*470+int(250*(.5+.15*i)),600),fill=GOLD); d.rectangle((290+i*470,640,290+i*470+160,660),fill=(210,220,235))
def ui_saved(d,p):
    nav(d); txt(d,(260,290),"Danh sách đã lưu",F(46),NAVY)
    for i in range(3): rr(d,(260,360+i*120,800,460+i*120),16,WHITE,(210,215,225),3); d.ellipse((285,385+i*120,335,435+i*120),fill=GOLD); txt(d,(360,410+i*120),["Trường A · hạn 15/11","Trường B · hạn 30/11","Trường C · hạn 01/12"][i],F(30),NAVY,'lm')
    txt(d,(900,290),"Timeline hạn nộp",F(46),NAVY); d.line((920,420,1640,420),fill=NAVY,width=6)
    for i in range(4): x=940+i*230; d.ellipse((x-16,404,x+16,436),fill=GOLD if i<=int(p*4) else (200,205,215)); txt(d,(x,470),["Th10","Th11","Th12","Th1"][i],F(26),NAVY,'mm')
    rr(d,(900,540,1650,820),18,(255,248,230),GOLD,3); txt(d,(930,580),"Roadmap: còn 5 tháng",F(38),NAVY); d.rectangle((930,660,1620,690),fill=(225,225,225)); d.rectangle((930,660,930+int(690*(.3+.5*p)),690),fill=GOLD)
def ui_profile(d,p):
    nav(d); txt(d,(260,290),"Phân tích hồ sơ",F(50),NAVY)
    cx,cy=560,600; d.ellipse((cx-190,cy-190,cx+190,cy+190),outline=(225,228,236),width=30); d.arc((cx-190,cy-190,cx+190,cy+190),-90,-90+int(360*.72*min(1,p*1.6)),fill=GOLD,width=30); txt(d,(cx,cy),"72",F(110),NAVY,'mm')
    for i,t in enumerate(["GPA","Hoạt động ngoại khóa","Bài luận","Chứng chỉ"]): rr(d,(960,380+i*110,1640,470+i*110),14,WHITE,(210,215,225),3); txt(d,(990,425+i*110),t,F(32),NAVY,'lm'); d.rectangle((1330,415+i*110,1330+int(250*(.5+.1*i)),435+i*110),fill=GOLD)
def ui_agency(d,p):
    nav(d); txt(d,(260,290),"Trung tâm tư vấn đã kiểm chứng",F(46),NAVY)
    for i in range(3):
        rr(d,(260+i*470,380,690+i*470,800),18,WHITE,GOLD if i==0 else (210,215,225),5 if i==0 else 3); d.ellipse((300+i*470,420,380+i*470,500),fill=NAVY); txt(d,(300+i*470,540),["Tuan Minh Consulting","Trung tâm B","Trung tâm C"][i],F(32),NAVY,'lm'); txt(d,(300+i*470,600),"✓ Đã kiểm chứng",F(28,False),(40,140,80),'lm'); txt(d,(300+i*470,660),"Mã giảm giá Premium",F(26,False),(90,100,120),'lm')
def ui_tools(d,p):
    nav(d); txt(d,(260,290),"Công cụ cho hồ sơ du học",F(46),NAVY)
    for i,(t,u) in enumerate([("Câu lạc bộ","Clubs"),("Cuộc thi","Competitions"),("Thực tập","Internships"),("Alumni","Alumni"),("Hồ sơ mẫu","Archive"),("Đội nhóm","Teams")]):
        x=260+(i%3)*470; y=380+(i//3)*250; rr(d,(x,y,x+430,y+210),18,(255,248,230) if i%2==0 else WHITE,GOLD if i==int(p*6) else (210,215,225),5); d.ellipse((x+25,y+30,x+85,y+90),fill=NAVY); txt(d,(x+25,y+130),t,F(36),NAVY,'lm'); txt(d,(x+25,y+175),u,F(24,False),(100,110,130),'lm')
def set_office(p=0):
    im,d=new((200,205,215)); d.rectangle((250,100,1670,700),fill=(40,70,110))
    for (x,y,w,h) in [(400,250,330,200),(800,200,260,150),(950,400,200,230),(1280,260,260,220),(1350,500,180,100),(500,520,160,100)]: d.ellipse((x,y,x+w,y+h),fill=(80,150,130))
    d.rectangle((0,780,W,H),fill=(110,80,60)); d.rectangle((300,730,1700,800),fill=(86,56,38))
    person(d,960,300,1.2,(60,70,95),hair=(20,20,25),tie=GOLD); laptop(d,1220,560,420,240,(215,225,245)); return im
def set_exit(p=0):
    im,d=new((255,200,110)); d.rectangle((0,0,W,H),fill=(255,215,140)); d.rectangle((400,0,1520,H),fill=(255,235,185),outline=(90,60,40),width=24)
    d.line((960,0,960,H),fill=(90,60,40),width=14); d.rectangle((0,900,W,H),fill=(120,90,70))
    x=500+int(900*p); person(d,x,330,1.2,(235,240,248),glasses=True,tie=NAVY); d.rounded_rectangle((x-110,430,x-40,640),20,fill=(40,60,110)); return im
def set_door(p=0):
    im=set_room(); d=ImageDraw.Draw(im); o=int(960*min(1,max(0,(p-.15)/.7))**.8)
    d.rectangle((960-960+0,0,960-o,H),fill=(150,150,155)); d.rectangle((960+o,0,W,H),fill=(150,150,155))
    for xx in (960-o,960+o): d.rectangle((xx-8,0,xx+8,H),fill=(235,190,70))
    return im
def set_end(p=0):
    im,d=new((22,70,160)); logo(d,W//2-90,230,180,True); wordmark(d,W//2-250,450,120,True)
    txt(d,(W//2,640),"Thắp sáng tiềm năng hồ sơ",F(64,True,True),WHITE,'mm')
    rr(d,(W//2-340,760,W//2+340,850),44,WHITE); txt(d,(W//2,805),"applysparkvn.com",F(46),NAVY,'mm'); return im
SADMODE=[False]
def set_face(p=0,sad=False):
    im,d=new((20,32,44)); shelf(d,0,0,W,H,3); im=im.filter(ImageFilter.GaussianBlur(25)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((560,760,1360,1300),200,fill=(235,240,248)); d.ellipse((650,180,1270,860),fill=(236,196,160)); d.pieslice((630,140,1290,640),180,360,fill=(25,25,30))
    for ex in(780,1140): d.ellipse((ex-30,470,ex+30,510),fill=(30,30,30))
    for ex in(780,1140): d.ellipse((ex-110,420,ex+110,560),outline=(20,20,20),width=10)
    d.line((890,490,1030,490),fill=(20,20,20),width=10)
    d.rounded_rectangle((680,640,860,880),90,fill=(236,196,160)); d.rounded_rectangle((1060,640,1240,880),90,fill=(226,186,150)) # hands
    d.arc((880,640,1040,720),200,340,fill=(150,70,60),width=8) if SADMODE[0] else d.arc((880,640,1040,720),20,160,fill=(150,70,60),width=8); return im

def set_sad(p=0):
    SADMODE[0]=True; im=set_face(); SADMODE[0]=False; return im
def set_club(p=0):
    im,d=new((60,50,45)); rr(d,(200,100,1720,900),14,(190,150,100),(110,70,40),16)
    rng=np.random.RandomState(8)
    for i,t in enumerate(["CLB Tranh biện","Tình nguyện","Robotics","Âm nhạc","Thể thao","Khởi nghiệp","Báo chí","Cuộc thi?"]):
        x=260+(i%4)*370; y=170+(i//4)*340; sh=Image.new('RGBA',(300,260),(0,0,0,0)); sd=ImageDraw.Draw(sh)
        sd.rectangle((0,0,299,259),fill=tuple(int(v) for v in rng.randint(190,255,3))+(255,)); sd.text((150,130),t,font=F(34),fill=(30,40,70,255),anchor='mm'); sd.ellipse((140,8,160,28),fill=(200,40,40,255))
        sh=sh.rotate(rng.randint(-8,8),expand=True); im.paste(sh,(x,y),sh)
    d=ImageDraw.Draw(im); person(d,260,380,0.9,(235,240,248),glasses=True,tie=NAVY)
    txt(d,(1450,60),"? ? ?",F(70),(255,200,90),'mm'); return im
def set_path(p=0):
    im,d=new((16,20,28)); rr(d,(160,90,1760,990),24,(245,247,250)); txt(d,(960,200),"Du học: bắt đầu từ đâu?",F(70),NAVY,'mm')
    for i,t in enumerate(["Chọn nước?","Chọn ngành?","Hoạt động ngoại khóa?","Học bổng?","Hạn nộp?","Luận văn?"]):
        x=260+(i%3)*500; y=330+(i//3)*280; rr(d,(x,y,x+440,y+200),24,(255,248,230),GOLD,4); txt(d,(x+220,y+100),t,F(38),NAVY,'mm')
    txt(d,(960,900),"?",F(90),(200,40,40),'mm'); return im
def set_parent(p=0):
    im=set_kitchen(); d=ImageDraw.Draw(im); d.rectangle((880,600,1520,830),fill=(130,92,60)); d.rectangle((200,760,1720,830),fill=(110,70,44))
    person(d,1250,360,1.1,(150,95,110),skin=(226,180,140),hair=(40,30,30)); rr(d,(900,650,1100,780),10,(240,240,245)); d.ellipse((960,780,1040,830),fill=(240,240,240)); return im
def set_meet(p=0):
    im=set_office(); d=ImageDraw.Draw(im); d.rectangle((0,0,520,H),fill=(30,36,46)); person(d,240,340,1.3,(235,240,248),glasses=True,tie=NAVY); return im
def set_price(p=0):
    im,d=new((200,205,215)); rr(d,(380,100,1540,980),12,(250,250,245)); txt(d,(960,230),"Báo giá tư vấn",F(76),NAVY,'mm')
    for i in range(3): d.line((520,360+i*100,1400,360+i*100),fill=(200,205,215),width=6)
    txt(d,(960,640),"?,???,??? VND",F(120),(200,40,40),'mm'); return im
def set_friends(p=0):
    im,d=new((255,215,160)); d.rectangle((0,0,W,620),fill=(190,215,235)); d.rectangle((0,620,W,H),fill=(150,120,95)); 
    for i in range(4): d.rectangle((0,700+i*70,W,740+i*70),fill=(165,135,108))
    person(d,640,200,1.4,(235,240,248),glasses=True,tie=NAVY); person(d,1320,230,1.4,(50,100,170),hair=(60,40,25)); laptop(d,980,640,420,240,(215,225,245))
    return im
# ---------- shots: (set, dur, cam0(cx,cy,z), cam1, rot0, rot1, grade, sub, caption, fg) ----------
cool=(30,60,110,60); warm=(255,170,60,45); neu=(0,0,0,0)
C=lambda x,y,z:(x,y,z)
S=[
 (set_door,5,C(960,540,1.05),C(960,540,1.5),0,0,cool,None,None,None),
 (set_room,5,C(900,520,1.0),C(1050,470,1.5),0,0,cool,None,None,'ots'),
 (set_club,6,C(1200,500,1.0),C(500,520,1.7),0,0,cool,None,"Câu lạc bộ? Hoạt động ngoại khóa?",None),
 (set_room,6,C(1000,420,2.0),C(1050,400,2.6),0,0,cool,"“Mình muốn đi du học… nhưng chưa biết bắt đầu từ đâu.”",None,None),
 (set_top,5,C(960,540,1.0),C(1000,420,1.6),-6,8,cool,None,None,None),
 (set_path,6,C(1000,540,1.1),C(800,480,1.9),8,12,cool,None,None,None),
 (card(["Muốn du học.","Chưa có lộ trình."],"He loves studying abroad. He has no path yet."),5,C(960,540,1.0),C(960,540,1.08),0,0,neu,None,None,None),
 (set_parent,7,C(1100,540,1.0),C(850,460,1.6),0,0,neu,"“Con thích du học thì đi hỏi thử xem.”",None,None),
 (set_office,6,C(960,540,1.0),C(980,500,1.5),0,0,neu,None,"Trung tâm tư vấn du học",None),
 (set_meet,6,C(900,540,1.0),C(1100,500,1.5),0,0,neu,None,None,'ots'),
 (set_price,5,C(960,540,1.0),C(960,600,1.3),0,0,neu,None,None,None),
 (set_sad,5,C(960,500,1.0),C(960,480,1.35),0,0,cool,None,None,None),
 (set_friends,7,C(960,540,1.1),C(1250,560,1.8),0,0,warm,"“Thử ApplySpark đi. Miễn phí, tìm trường, CLB, hạn nộp.”",None,None),
 (ui_frame(ui_home),5,C(960,540,1.0),C(960,480,1.35),-6,0,warm,None,"Thắp sáng tiềm năng hồ sơ",None),
 (ui_frame(ui_uni),6,C(900,560,1.0),C(1000,520,1.5),0,4,warm,None,"Nghiên cứu trường toàn cầu, một nơi",None),
 (ui_frame(ui_saved),6,C(1000,520,1.1),C(1300,600,1.7),5,0,warm,None,"Danh sách · Hạn nộp · Lộ trình",None),
 (ui_frame(ui_profile),6,C(960,540,1.0),C(700,600,1.6),0,-5,warm,None,"Gợi ý hồ sơ, không phải cam kết đậu",None),
 (ui_frame(ui_tools),5,C(960,540,1.0),C(1100,560,1.4),0,0,warm,None,"CLB · Cuộc thi · Thực tập · Alumni",None),
 (ui_frame(ui_agency),6,C(960,540,1.0),C(1100,560,1.35),0,0,warm,None,"Basic miễn phí · Trung tâm uy tín",None),
 (set_exit,6,C(960,540,1.2),C(1100,420,1.0),0,0,warm,"“Giờ mình biết mình đang đi đâu.”",None,None),
 (set_end,6,C(960,540,1.0),C(960,540,1.06),0,0,neu,None,None,None),
]
starts=np.cumsum([0]+[s[1] for s in S]); TOT=int(starts[-1])
# ---------- render ----------
yy,xx=np.mgrid[0:VH,0:VW]; vig=1-0.55*(((xx-VW/2)/(VW/2))**2+((yy-VH/2)/(VH/2))**2)/2; vig=np.clip(vig,0.35,1)[...,None]
def mkfg(kind):
    im=Image.new('RGBA',(VW,VH),(0,0,0,0)); d=ImageDraw.Draw(im)
    if kind=='ots': d.ellipse((-120,150,330,700),fill=(12,12,16,255)); d.rounded_rectangle((-60,420,420,900),120,fill=(18,18,24,255))
    else: d.ellipse((560,200,1100,800),fill=(60,60,70,255)); 
    return im.filter(ImageFilter.GaussianBlur(14))
FGS={'ots':mkfg('ots'),'ots2':mkfg('ots2').transpose(Image.FLIP_LEFT_RIGHT)}
def ease(t): return t*t*(3-2*t)
def subimg(text,font,maxw=1500):
    return text
cache={}
def getset(i,p):
    fn=S[i][0]
    if fn in (set_door,set_chalk,set_exit) or fn.__name__=='f':
        return fn(p)
    if i not in cache: cache[i]=fn(0)
    return cache[i]
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{VW}x{VH}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','24','-preset','veryfast','-pix_fmt','yuv420p',OUT],stdin=subprocess.PIPE)
fsub=F(30,False); fcap=F(40); stat=None
frames=range(TOT*FPS) if not PREVIEW else [int((starts[i]+S[i][1]/2)*FPS) for i in range(len(S))]
anim_f=0
for fr in frames:
    t=fr/FPS; i=int(np.searchsorted(starts,t,side='right')-1); i=min(i,len(S)-1)
    sh=S[i]; p=(t-starts[i])/sh[1]; e=ease(p)
    base=getset(i,p)
    cx=sh[2][0]+(sh[3][0]-sh[2][0])*e; cy=sh[2][1]+(sh[3][1]-sh[2][1])*e; z=sh[2][2]+(sh[3][2]-sh[2][2])*e
    th=math.radians(sh[4]+(sh[5]-sh[4])*e); s=(W/z)/VW; c,sn=math.cos(th),math.sin(th)
    a=s*c; b=-s*sn; cc=cx-480*a-270*b; dd=s*sn; ee=s*c; ff_=cy-480*dd-270*ee
    v=base.transform((VW,VH),Image.AFFINE,(a,b,cc,dd,ee,ff_),Image.BILINEAR)
    if sh[9]: v=v.convert('RGBA'); v.alpha_composite(FGS[sh[9]]); v=v.convert('RGB')
    arr=np.asarray(v).astype(np.float32)
    g=sh[6]
    if g[3]: arr=arr*(1-g[3]/255)+np.array(g[:3])*(g[3]/255)
    arr=arr*vig
    arr+= np.random.randn(VH,VW,1).astype(np.float32)*3
    f=np.clip(arr,0,255)
    lt=t-starts[i]; fade=min(1,lt/0.4,(sh[1]-lt)/0.4) if i not in(0,) else min(1,(sh[1]-lt)/0.4)
    f*=max(0,fade)
    im=Image.fromarray(f.astype(np.uint8)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,VW,40),fill=(0,0,0)); d.rectangle((0,VH-40,VW,VH),fill=(0,0,0))
    if sh[8] and 0.6<lt<sh[1]-0.5:
        tw=d.textlength(sh[8],font=fcap); d.rounded_rectangle((VW/2-tw/2-20,VH-140,VW/2+tw/2+20,VH-84),14,fill=(11,31,68)); d.text((VW/2,VH-112),sh[8],font=fcap,fill=GOLD if True else WHITE,anchor='mm')
    if sh[7] and 0.8<lt<sh[1]-0.4:
        words=sh[7]; 
        d.text((VW/2+1,VH-62+1),words,font=fsub,fill=(0,0,0),anchor='mm'); d.text((VW/2,VH-62),words,font=fsub,fill=(255,235,170),anchor='mm')
    if i==0 or i==len(S)-1: pass
    im.paste((0,0,0),(0,0,0,0)) if False else None
    ff.stdin.write(im.tobytes())
ff.stdin.close(); ff.wait()
print("done",TOT)

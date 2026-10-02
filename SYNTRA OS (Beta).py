from ti_draw import set_color,fill_rect,draw_rect,draw_line,draw_text
from ti_system import wait_key,recall_list,store_list
from time import monotonic

W,H=320,210
RIGHT,LEFT,UP,DOWN,ENTER,CLEAR,SECOND,DEL=26,24,25,34,105,45,21,23
WHITE=(245,247,250); MUTED=(165,173,188); BG=(10,12,18); BAR=(24,28,38)
CARD=(35,40,52); SEL=(50,57,72); PURPLE=(155,75,235)
wp=0
try: wp=int(recall_list('A84WALL')[0])
except: pass

Y,M,D,h,mi=2026,9,22,10,10
anchor=monotonic()
try:
 v=recall_list('A84CLK')
 if len(v)>=5: Y,M,D,h,mi=[int(x) for x in v[:5]]; anchor=monotonic()
except: pass

def col(c): set_color(c[0],c[1],c[2])
def box(x,y,w,h,c,fill=1):
 if w<=0 or h<=0:return
 col(c)
 if fill: fill_rect(int(x),int(y),int(w),int(h))
 else: draw_rect(int(x),int(y),int(w),int(h))
def txt(x,y,s,c=WHITE):
 s=str(s); x=int(x); y=int(y)
 if x<0: s=s[(-x+9)//10:]; x=0
 n=max(0,(W-x)//10)
 if n and s: col(c); draw_text(x,y,s[:n])
def center(y,s,c=WHITE):
 s=str(s); s=s[:32]; txt((W-len(s)*10)//2,y,s,c)
def ln(x1,y1,x2,y2,c): col(c); draw_line(max(0,min(319,int(x1))),max(0,min(209,int(y1))),max(0,min(319,int(x2))),max(0,min(209,int(y2))))

def days(m): return 29 if m==2 and Y%4==0 else 28 if m==2 else 30 if m in (4,6,9,11) else 31
def clock():
 t=h*3600+mi*60+int(monotonic()-anchor); carry=t//86400; z=t%86400
 hh=z//3600; mm=(z%3600)//60
 y,m,d=Y,M,D
 for _ in range(carry):
  d+=1
  if d>days(m): d=1; m+=1
  if m>12: m=1; y+=1
 return y,m,d,hh,mm

def wallpaper():
 box(0,0,W,H,BG)
 if wp==1:
  for x in range(0,W,24): ln(x,24,x,189,(31,20,45))
  for y in range(24,190,24): ln(0,y,319,y,(31,20,45))
 elif wp==2:
  for x,y in ((15,35),(48,70),(82,42),(118,94),(151,43),(181,76),(220,38),(252,84),(287,48),(305,111),(37,151),(91,174),(142,144),(204,167),(268,151),(300,181)): box(x,y,2,2,WHITE)

def header(s): box(0,0,W,23,BAR); txt(7,18,s)
def footer(s='CLEAR Back'): box(0,190,W,20,BAR); txt(7,207,s,MUTED)
def status():
 box(0,0,W,24,BAR); y,m,d,hh,mm=clock(); txt(7,18,'{:02d}/{:02d}/{:04d}'.format(m,d,y)); txt(263,18,'{:02d}:{:02d}'.format(hh,mm))
def app_icon(x,y,letter,c=PURPLE,sel=0):
 box(x,y,30,30,SEL if sel else CARD); box(x+6,y+6,18,18,c); txt(x+11,y+19,letter,WHITE)
def s_logo():
 p=[(159,28),(188,53),(188,78),(163,96),(188,115),(188,139),(159,166),(130,139),(130,115),(155,96),(130,78),(130,53),(159,28)]
 for a,b in zip(p,p[1:]): ln(a[0],a[1],b[0],b[1],PURPLE); ln(a[0]+1,a[1],b[0]+1,b[1],PURPLE)
def boot():
 box(0,0,W,H,(0,0,0)); s_logo(); center(180,'SYNTRA OS',WHITE); center(198,'Press ENTER to start',WHITE)
 while wait_key()!=ENTER: pass

APPS=[('Calculator','C'),('Games','G'),('Notes','N'),('Gallery','P'),('Files','F'),('Settings','S')]
sel=0
def tile(i,selected=None):
 x=8+(i%3)*102; y=29+(i//3)*82; q=sel if selected is None else selected
 box(x,y,96,76,SEL if i==q else CARD); app_icon(x+33,y+5,APPS[i][1],PURPLE if i==3 or i==5 else (45,190,120) if i==1 else (55,130,245),i==q); txt(x+(96-len(APPS[i][0])*10)//2,y+58,APPS[i][0],WHITE if i==q else MUTED)
def home():
 global sel
 wallpaper(); status()
 for i in range(6): tile(i)
 footer('ARROWS Select ENTER Open 2nd Apps')
 while 1:
  k=wait_key(); old=sel
  if k==CLEAR:return
  if k==RIGHT and sel%3<2: sel+=1
  elif k==LEFT and sel%3>0: sel-=1
  elif k==DOWN and sel<3: sel+=3
  elif k==UP and sel>=3: sel-=3
  elif k==SECOND: apps(); wallpaper(); status(); [tile(i) for i in range(6)]; footer('ARROWS Select ENTER Open 2nd Apps'); continue
  elif k==ENTER: open_app(); wallpaper(); status(); [tile(i) for i in range(6)]; footer('ARROWS Select ENTER Open 2nd Apps'); continue
  if old!=sel: tile(old); tile(sel)
def apps():
 q=0; wallpaper(); header('Apps')
 for i in range(6): tile(i,q)
 footer('ARROWS Move ENTER Open CLEAR Back')
 while 1:
  k=wait_key(); old=q
  if k==CLEAR:return
  if k==RIGHT and q%3<2:q+=1
  elif k==LEFT and q%3>0:q-=1
  elif k==DOWN and q<3:q+=3
  elif k==UP and q>=3:q-=3
  elif k==ENTER: open_index(q); wallpaper(); header('Apps'); [tile(i,q) for i in range(6)]; footer('ARROWS Move ENTER Open CLEAR Back'); continue
  if old!=q: tile(old,q); tile(q,q)
def open_app(): open_index(sel)
def open_index(i):
 if i==0: calculator()
 elif i==1: games()
 elif i==2: notes()
 elif i==3: gallery()
 elif i==4: files()
 else: settings()

def calculator():
 keys='789/456*123-0.=+CDEL()'; q=0; expr=''
 def key(i):
  x=12+(i%4)*75; y=76+(i//4)*22; box(x,y,68,19,SEL if i==q else CARD); txt(x+34-len(keys[i])*5,y+14,keys[i],WHITE if i==q else MUTED)
 box(0,0,W,H,BG); header('Calculator'); box(10,27,299,42,(5,7,10)); txt(18,41,'HOME',MUTED); txt(18,59,'0')
 for i in range(20):key(i)
 footer('ARROWS Move ENTER Use CLEAR')
 while 1:
  k=wait_key(); old=q
  if k==CLEAR:return
  if k==RIGHT and q%4<3:q+=1
  elif k==LEFT and q%4>0:q-=1
  elif k==DOWN and q<16:q+=4
  elif k==UP and q>=4:q-=4
  elif k==ENTER:
   a=keys[q]
   if a=='C':expr=''
   elif a=='DEL':expr=expr[:-1]
   elif a=='=':
    try:
     if any(c not in '0123456789.+-*/() ' for c in expr):raise ValueError
     expr=str(eval(expr,{'__builtins__':{}},{}))
    except:expr='ERR'
   else: expr=('.' if expr=='ERR' else expr)+a
   box(10,27,299,42,(5,7,10)); txt(18,41,'HOME',MUTED); txt(18,59,expr or '0')
  if old!=q:key(old);key(q)

def note_get(i):
 try:
  v=recall_list('N'+str(i)); return ''.join(chr(int(x)) for x in v[:80]) if v and int(v[0]) else ''
 except:return ''
def note_put(i,s):
 try: store_list('N'+str(i),[ord(c) for c in s[:80]] or [0])
 except: pass
def notes():
 q=0; note_list(q)
 while 1:
  k=wait_key(); old=q
  if k==CLEAR:return
  if k==DOWN:q=min(9,q+1)
  elif k==UP:q=max(0,q-1)
  elif k==ENTER: note_edit(q); note_list(q)
  elif k==DEL:note_put(q,''); note_list(q)
  if old!=q: note_row(old,0); note_row(q,1)
def note_row(i,s):
 y=29+i*16; box(8,y-2,296,15,SEL if s else BG); txt(18,y+10,'Note '+str(i+1),WHITE if s else MUTED)
def note_list(q):
 box(0,0,W,H,BG); header('Notes')
 for i in range(10):note_row(i,i==q)
 footer('ARROWS Select ENTER Edit CLEAR')
def note_edit(i):
 s=note_get(i); chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?+-*/()'; q=0
 while 1:
  box(0,0,W,H,BG); header('Note '+str(i+1)); txt(12,42,s[:30]); txt(12,57,s[30:60]); txt(12,72,s[60:80]); txt(12,88,'Length '+str(len(s))+'/80',MUTED)
  for n,c in enumerate(chars):
   if n>=32:break
   x=10+(n%8)*38;y=100+(n//8)*22;box(x,y,34,19,SEL if n==q else CARD);txt(x+14,y+14,c,WHITE if n==q else MUTED)
  footer('ENTER Add DEL Back CLEAR Save')
  k=wait_key()
  if k==CLEAR:note_put(i,s);return
  if k==DEL:s=s[:-1]
  elif k==RIGHT:q=min(31,q+1)
  elif k==LEFT:q=max(0,q-1)
  elif k==DOWN:q=min(31,q+8)
  elif k==UP:q=max(0,q-8)
  elif k==ENTER and len(s)<80:s+=chars[q]

def gallery():
 try:
  from ti_image import load_image,show_image
 except:
  box(0,0,W,H,BG);header('Gallery');center(95,'TI Image module unavailable');footer();wait_key();return
 q=0
 while 1:
  box(0,0,W,H,BG);header('Gallery');
  try:load_image('PIC'+str(q+1 if q<9 else 0));show_image(20,31)
  except:center(95,'Empty picture slot');center(116,'PIC'+str(q+1 if q<9 else 0),MUTED)
  footer('LEFT Prev RIGHT Next CLEAR Back'); k=wait_key()
  if k==CLEAR:return
  if k==RIGHT:q=(q+1)%10
  elif k==LEFT:q=(q-1)%10

def files():
 q=0
 while 1:
  box(0,0,W,H,BG);header('Files')
  for i,n in enumerate(('Pictures','Notes','Misc.')):
   y=45+i*34;box(18,y-7,283,27,SEL if i==q else CARD);txt(31,y+10,n,WHITE if i==q else MUTED)
  footer('ARROWS Select ENTER Open CLEAR Back');k=wait_key()
  if k==CLEAR:return
  if k==DOWN:q=min(2,q+1)
  elif k==UP:q=max(0,q-1)
  elif k==ENTER:
   if q==0:gallery()
   elif q==1:notes()
   else:
    box(0,0,W,H,BG);header('Misc.');center(95,'No user misc files.');footer();wait_key()

def settings():
 items=('Wallpaper','Date and Time','Navigation Instructions');q=0
 while 1:
  box(0,0,W,H,BG);header('Settings')
  for i,n in enumerate(items):y=45+i*34;box(12,y-8,294,27,SEL if i==q else CARD);txt(25,y+9,n,WHITE if i==q else MUTED)
  footer('ARROWS Select ENTER Open CLEAR Back');k=wait_key()
  if k==CLEAR:return
  if k==DOWN:q=min(2,q+1)
  elif k==UP:q=max(0,q-1)
  elif k==ENTER:
   if q==0:wall_settings()
   elif q==1:time_settings()
   else:nav_help()
def wall_settings():
 global wp
 names=('Midnight','Purple Grid','Stars');q=wp if wp<3 else 0
 while 1:
  box(0,0,W,H,BG);header('Wallpaper')
  for i,n in enumerate(names):y=35+i*28;box(12,y-7,294,22,SEL if i==q else CARD);txt(25,y+8,n,WHITE if i==q else MUTED)
  footer('UP/DOWN Choose ENTER Apply CLEAR');k=wait_key()
  if k==CLEAR:return
  if k==DOWN:q=min(2,q+1)
  elif k==UP:q=max(0,q-1)
  elif k==ENTER:
   wp=q
   try:store_list('A84WALL',[wp])
   except:pass
   return
def time_settings():
 global Y,M,D,h,mi,anchor
 vals=[Y,M,D,h,mi]; names=('Year','Month','Day','Hour','Minute');q=0
 while 1:
  box(0,0,W,H,BG);header('Date and Time');txt(18,40,'Use arrows to edit',MUTED)
  for i,n in enumerate(names):y=60+i*24;box(12,y-8,294,21,SEL if i==q else CARD);txt(25,y+7,n);txt(205,y+7,vals[i])
  footer('UP/DOWN Field LEFT/RIGHT Edit ENTER Save');k=wait_key()
  if k==CLEAR:return
  if k==DOWN:q=min(4,q+1)
  elif k==UP:q=max(0,q-1)
  elif k in (LEFT,RIGHT):vals[q]+= -1 if k==LEFT else 1
  elif k==ENTER:
   Y,M,D,h,mi=vals;anchor=monotonic()
   try:store_list('A84CLK',[Y,M,D,h,mi])
   except:pass
   return
def nav_help():
 box(0,0,W,H,BG);header('Navigation');
 for i,s in enumerate(('ARROWS  move/select','ENTER   open/confirm','CLEAR   back/cancel','2nd     app launcher','DEL     delete')):txt(16,50+i*24,s)
 footer();
 while wait_key()!=CLEAR:pass

def games():
 run()

from ti_draw import set_color, fill_rect, draw_line, draw_text, fill_circle, clear
from ti_system import wait_key, get_key
from time import monotonic
from random import randint

W,H=320,210
CHAR_W=10
RIGHT,LEFT,UP,DOWN,ENTER,CLEAR=26,24,25,34,105,45
WHITE=(245,247,250); MUTED=(165,173,188); BG=(10,12,18); BAR=(24,28,38)
CARD=(35,40,52); CARD2=(50,57,72)
PURPLE=(155,75,235); GREEN=(45,190,120); RED=(230,70,80)
BLUE=(55,130,245); CYAN=(55,210,220); YELLOW=(245,205,55)

def col(c): set_color(c[0],c[1],c[2])
def rect(x,y,w,h,c):
    if w<=0 or h<=0: return
    col(c); fill_rect(int(x),int(y),int(w),int(h))
def line(x1,y1,x2,y2,c):
    col(c); draw_line(max(0,min(319,int(x1))),max(0,min(209,int(y1))),
                     max(0,min(319,int(x2))),max(0,min(209,int(y2))))
def circle(x,y,r,c):
    if r<=0: return
    col(c); fill_circle(int(x),int(y),int(r))
def txt(x,y,s,c=WHITE):
    s=str(s); x=int(x); y=int(y)
    if x<0:
        s=s[(-x+9)//10:]; x=0
    n=max(0,(W-x)//10)
    if n and s:
        col(c); draw_text(x,y,s[:n])
def center_text(y,s,c=WHITE):
    s=str(s)[:32]
    txt((W-len(s)*10)//2,y,s,c)
def clear_screen():
    col(BG); clear()
def header(s):
    rect(0,0,W,23,BAR); txt(7,18,s)
def footer(s="CLEAR Back"):
    rect(0,190,W,20,BAR); txt(7,207,s,MUTED)
from random import randint
def game_key(last_key=0):
    try:
        return get_key(0)
    except:
        return wait_key()
def game_tile_geometry(i):
    return (i % 4) * 79, 27 + (i // 4) * 78, 79, 78
def controls_screen(name,game_id):
    while True:
        clear_screen(); txt(7,15,"Games",WHITE); center_text(52,name,WHITE); center_text(78,"CONTROLS",PURPLE)
        a=["ARROWS = Move","UP/DOWN = Paddle","LEFT/RIGHT = Move | ENTER = Drop","LEFT/RIGHT = Paddle","UP or ENTER = Flap","ARROWS = Move | ENTER = Reveal","ARROWS = Slide","LEFT/RIGHT = Move | ENTER = Fire"][game_id]
        center_text(108,a,WHITE); center_text(151,"Press ENTER to play",WHITE); center_text(174,"CLEAR = Back",MUTED)
        k=wait_key()
        if k==CLEAR:return
        if k==ENTER:
            [snake,pong,tetris,breakout,flappy,mines,game2048,space_game][game_id](); return
def game_start(title,score_text=""):
    rect(0,0,W,H,(0,0,0)); header(title)
    if score_text:
        rect(150,1,163,20,BAR); txt(W-len(score_text)*CHAR_W-7,18,score_text,MUTED)
def game_score(title, score):
    rect(150, 1, 163, 20, BAR)
    s = "Score " + str(score)
    txt(W - len(s) * CHAR_W - 7, 18, s, MUTED)
def game_over(title, score):
    rect(0, 0, W, H, (0, 0, 0))
    center_text(72, title, WHITE)
    center_text(98, "Score " + str(score), YELLOW)
    center_text(128, "ENTER / CLEAR = Back", MUTED)
    while True:
        k = wait_key()
        if k == CLEAR:
            return False
        if k == ENTER:
            return True
def erase_snake_cell(p):
    rect(8 + p[0] * 7, 22 + p[1] * 8, 6, 7, (0, 0, 0))
def draw_snake_cell(p):
    rect(8 + p[0] * 7, 22 + p[1] * 8, 6, 7, GREEN)
def snake():
    body = [[10, 6], [9, 6], [8, 6]]
    dx, dy = 1, 0
    food = [randint(2, 37), randint(2, 18)]
    score = 0
    last = monotonic()
    previous = 0
    game_start("Snake", "Score 0")
    for p in body:
        draw_snake_cell(p)
    rect(8 + food[0] * 7, 22 + food[1] * 8, 6, 7, RED)
    while True:
        k = game_key(previous)
        if k == CLEAR:
            return
        previous = k
        if k == UP and dy == 0:
            dx, dy = 0, -1
        elif k == DOWN and dy == 0:
            dx, dy = 0, 1
        elif k == LEFT and dx == 0:
            dx, dy = -1, 0
        elif k == RIGHT and dx == 0:
            dx, dy = 1, 0
        now = monotonic()
        if now - last >= 0.11:
            last = now
            old_tail = body[-1][:]
            head = [body[0][0] + dx, body[0][1] + dy]
            if head[0] < 1 or head[0] > 38 or head[1] < 1 or head[1] > 18 or head in body:
                game_over("Snake", score)
                return
            ate = head == food
            if not ate:
                erase_snake_cell(old_tail)
                body.pop()
            body.insert(0, head)
            draw_snake_cell(head)
            if ate:
                score += 1
                game_score("Snake", score)
                food = [randint(2, 37), randint(2, 18)]
                while food in body:
                    food = [randint(2, 37), randint(2, 18)]
                rect(8 + food[0] * 7, 22 + food[1] * 8, 6, 7, RED)
def pong():
    px, py = 18, 95
    bx, by = 159, 95
    vx, vy = 2, 1
    old_px, old_by = px, by
    old_bx, old_ball_y = bx, by
    score = 0
    last = monotonic()
    previous = 0
    game_start("Pong", "Score 0")
    rect(18, py - 22, 5, 44, WHITE)
    rect(296, by - 18, 5, 36, BLUE)
    circle(bx, by, 3, YELLOW)
    while True:
        k = game_key(previous)
        if k == CLEAR:
            return
        if k == UP:
            py -= 3
        elif k == DOWN:
            py += 3
        py = max(48, min(144, py))
        now = monotonic()
        if now - last >= 0.03:
            last = now
            rect(18, old_px - 22, 5, 44, (0, 0, 0))
            rect(296, old_by - 18, 5, 36, (0, 0, 0))
            circle(old_bx, old_ball_y, 3, (0, 0, 0))
            bx += vx
            by += vy
            if by < 30 or by > 178:
                vy = -vy
            if bx > 296:
                vx = -abs(vx)
            if bx < 28 and abs(by - py) < 24:
                vx = abs(vx)
                score += 1
                game_score("Pong", score)
            if bx < 4:
                game_over("Pong", score)
                return
            if bx > 315:
                bx, by = 159, 95
                vx = -2
            rect(18, py - 22, 5, 44, WHITE)
            rect(296, by - 18, 5, 36, BLUE)
            circle(bx, by, 3, YELLOW)
            old_px, old_by = py, by
            old_bx, old_ball_y = bx, by
def tetris():
    grid = []
    x, y = 5, 1
    score = 0
    last = monotonic()
    previous = 0
    falling = True
    game_start("Blocks", "Score 0")
    rect(60 + x * 18, 25 + y * 8, 16, 7, CYAN)
    while True:
        k = game_key(previous)
        if k == CLEAR:
            return
        old_x, old_y = x, y
        if k == LEFT:
            x = max(0, x - 1)
        elif k == RIGHT:
            x = min(9, x + 1)
        elif k == ENTER:
            while y < 18 and [x, y + 1] not in grid:
                y += 1
            if [x, y] not in grid:
                grid.append([x, y])
            score += 1
            game_score("Blocks", score)
            x, y = 5, 1
        now = monotonic()
        if now - last > 0.35:
            last = now
            y += 1
            if y >= 19 or [x, y] in grid:
                y -= 1
                if y < 1:
                    game_over("Blocks", score)
                    return
                if [x, y] not in grid:
                    grid.append([x, y])
                score += 1
                game_score("Blocks", score)
                x, y = 5, 1
        if old_x != x or old_y != y:
            rect(60 + old_x * 18, 25 + old_y * 8, 16, 7, (0, 0, 0))
            if [old_x, old_y] in grid:
                rect(60 + old_x * 18, 25 + old_y * 8, 16, 7, PURPLE)
        rect(60 + x * 18, 25 + y * 8, 16, 7, CYAN)
def breakout():
    px = 135
    bx, by = 159, 145
    vx, vy = 2, -2
    bricks = [[1 + b * 20, 35 + a * 9, 17, 7] for a in range(4) for b in range(15)]
    score = 0
    last = monotonic()
    previous = 0
    game_start("Breakout", "Score 0")
    for i, r in enumerate(bricks):
        rect(r[0], r[1], r[2], r[3], BLUE if i % 2 else GREEN)
    rect(px, 172, 58, 5, WHITE)
    circle(bx, by, 3, YELLOW)
    while True:
        k = game_key(previous)
        previous = k
        if k == CLEAR:
            return
        old_px, old_bx, old_by = px, bx, by
        if k == LEFT:
            px = max(8, px - 4)
        elif k == RIGHT:
            px = min(253, px + 4)
        now = monotonic()
        if now - last >= 0.025:
            last = now
            rect(old_px, 172, 58, 5, (0, 0, 0))
            circle(old_bx, old_by, 3, (0, 0, 0))
            bx += vx
            by += vy
            if bx < 3 or bx > 316:
                vx = -vx
            if by < 24:
                vy = abs(vy)
            if 165 < by < 181 and px - 8 < bx < px + 58 and vy > 0:
                vy = -abs(vy)
            hit = -1
            for i, r in enumerate(bricks):
                if r[0] < bx < r[0] + r[2] and r[1] < by < r[1] + r[3]:
                    hit = i
                    break
            if hit >= 0:
                r = bricks.pop(hit)
                rect(r[0], r[1], r[2], r[3], (0, 0, 0))
                vy = -vy
                score += 1
                game_score("Breakout", score)
            if by > 188:
                game_over("Breakout", score)
                return
            if not bricks:
                game_over("You Win!", score)
                return
            rect(px, 172, 58, 5, WHITE)
            circle(bx, by, 3, YELLOW)
def flappy():
    y = 100
    vy = 0
    x = 80
    pipes = [[319, 80], [440, 110]]
    score = 0
    last = monotonic()
    previous = 0
    game_start("Flappy", "Score 0")
    circle(x, y, 6, YELLOW)
    for p in pipes:
        top_h = max(1, p[1] - 45)
        bottom_y = p[1] + 45
        bottom_h = max(1, H - 19 - bottom_y)
        if p[0] < W:
            rect(p[0], 20, 18, top_h, GREEN)
            rect(p[0], bottom_y, 18, bottom_h, GREEN)
    while True:
        k = game_key(previous)
        if k == CLEAR:
            return
        if k == UP or (k == ENTER and previous != ENTER):
            vy = -4.2
        previous = k
        now = monotonic()
        if now - last >= 0.04:
            last = now
            old_y = y
            old_pipes = [[p[0], p[1]] for p in pipes]
            circle(x, old_y, 6, (0, 0, 0))
            for p in old_pipes:
                top_h = max(1, p[1] - 45)
                bottom_y = p[1] + 45
                bottom_h = max(1, H - 19 - bottom_y)
                rect(p[0], 20, 18, top_h, (0, 0, 0))
                rect(p[0], bottom_y, 18, bottom_h, (0, 0, 0))
            vy += 0.22
            y += vy
            for p in pipes:
                p[0] -= 2
            if pipes[0][0] < -18:
                pipes.pop(0)
                pipes.append([pipes[-1][0] + 121, randint(65, 125)])
                score += 1
                game_score("Flappy", score)
            hit = False
            for p in pipes:
                if p[0] < x + 6 and p[0] + 18 > x - 6:
                    gap = p[1]
                    if y - 6 < gap - 25 or y + 6 > gap + 25:
                        hit = True
            if y < 26 or y > 180 or hit:
                game_over("Flappy", score)
                return
            circle(x, y, 6, YELLOW)
            for p in pipes:
                top_h = max(1, p[1] - 45)
                bottom_y = p[1] + 45
                bottom_h = max(1, H - 19 - bottom_y)
                rect(p[0], 20, 18, top_h, GREEN)
                rect(p[0], bottom_y, 18, bottom_h, GREEN)
def mine_cell(xx, yy, selected, revealed, mineset):
    bx = 55 + xx * 25
    by = 35 + yy * 25
    rect(bx, by, 20, 20, CARD2 if revealed else CARD)
    if revealed and [xx, yy] in mineset:
        circle(bx + 10, by + 10, 6, RED)
    if selected:
        rect(bx, by, 20, 20, BLUE, False)
def mines():
    mineset = []
    while len(mineset) < 8:
        p = [randint(0, 7), randint(0, 4)]
        if p not in mineset:
            mineset.append(p)
    revealed = []
    x = y = 0
    game_start("Mines")
    for yy in range(5):
        for xx in range(8):
            mine_cell(xx, yy, xx == x and yy == y, [xx, yy] in revealed, mineset)
    while True:
        k = wait_key()
        if k == CLEAR:
            return
        oldx, oldy = x, y
        if k == LEFT:
            x = max(0, x - 1)
        elif k == RIGHT:
            x = min(7, x + 1)
        elif k == UP:
            y = max(0, y - 1)
        elif k == DOWN:
            y = min(4, y + 1)
        elif k == ENTER:
            if [x, y] in mineset:
                mine_cell(x, y, False, True, mineset)
                game_over("Mine!", len(revealed))
                return
            if [x, y] not in revealed:
                revealed.append([x, y])
                mine_cell(x, y, False, True, mineset)
                if len(revealed) >= 32:
                    game_over("You Win!", len(revealed))
                    return
        if oldx != x or oldy != y:
            mine_cell(oldx, oldy, False, [oldx, oldy] in revealed, mineset)
            mine_cell(x, y, True, [x, y] in revealed, mineset)
def slide_left(b):
    changed = False
    for y in range(4):
        old = b[y][:]
        vals = [v for v in b[y] if v]
        out = []
        i = 0
        while i < len(vals):
            if i + 1 < len(vals) and vals[i] == vals[i + 1]:
                out.append(vals[i] * 2)
                i += 2
            else:
                out.append(vals[i])
                i += 1
        while len(out) < 4:
            out.append(0)
        b[y] = out
        if old != out:
            changed = True
    return changed
def flip(b):
    for y in range(4):
        b[y].reverse()
def transpose(b):
    for y in range(4):
        for x in range(y + 1, 4):
            b[y][x], b[x][y] = b[x][y], b[y][x]
def add_tile(b):
    spots = []
    for y in range(4):
        for x in range(4):
            if b[y][x] == 0:
                spots.append([y, x])
    if spots:
        p = spots[randint(0, len(spots) - 1)]
        b[p[0]][p[1]] = 4 if randint(1, 10) == 10 else 2
def moves_available(b):
    for y in range(4):
        for x in range(4):
            if b[y][x] == 0:
                return True
            if x < 3 and b[y][x] == b[y][x + 1]:
                return True
            if y < 3 and b[y][x] == b[y + 1][x]:
                return True
    return False
def draw_2048_cell(x, y, v):
    rect(54 + x * 52, 35 + y * 36, 46, 31, CARD2 if v else CARD)
    if v:
        s = str(v)
        txt(77 + x * 52 - len(s) * 5, 55 + y * 36, s, WHITE)
def game2048():
    board = [[0, 0, 0, 0] for _ in range(4)]
    add_tile(board)
    add_tile(board)
    game_start("2048")
    for yy in range(4):
        for xx in range(4):
            draw_2048_cell(xx, yy, board[yy][xx])
    while True:
        k = wait_key()
        if k == CLEAR:
            return
        old = [row[:] for row in board]
        changed = False
        if k == LEFT:
            changed = slide_left(board)
        elif k == RIGHT:
            flip(board)
            changed = slide_left(board)
            flip(board)
        elif k == UP:
            transpose(board)
            changed = slide_left(board)
            transpose(board)
        elif k == DOWN:
            transpose(board)
            flip(board)
            changed = slide_left(board)
            flip(board)
            transpose(board)
        if changed:
            add_tile(board)
            for yy in range(4):
                for xx in range(4):
                    if old[yy][xx] != board[yy][xx]:
                        draw_2048_cell(xx, yy, board[yy][xx])
        if any(2048 in row for row in board):
            game_over("2048!", 2048)
            return
        if not moves_available(board):
            game_over("Game Over", 0)
            return
def space_game():
    x = 159
    enemies = [[randint(20, 299), randint(25, 90)] for _ in range(5)]
    shots = []
    score = 0
    last = monotonic()
    previous = 0
    def draw_ship(px, c):
        line(px, 176, px - 8, 190, c)
        line(px, 176, px + 8, 190, c)
        line(px - 8, 190, px + 8, 190, c)
    def draw_enemy(e, c):
        circle(e[0], e[1], 7, c)
    game_start("Space", "Score 0")
    draw_ship(x, CYAN)
    for e in enemies:
        draw_enemy(e, RED)
    while True:
        k = game_key(previous)
        if k == CLEAR:
            return
        old_x = x
        old_enemies = [[e[0], e[1]] for e in enemies]
        old_shots = [[s[0], s[1]] for s in shots]
        if k == LEFT:
            x = max(10, x - 4)
        elif k == RIGHT:
            x = min(309, x + 4)
        elif k == ENTER and previous != ENTER:
            shots.append([x, 170])
        previous = k
        now = monotonic()
        if now - last >= 0.035:
            last = now
            draw_ship(old_x, (0, 0, 0))
            for s in old_shots:
                rect(s[0] - 1, s[1], 3, 7, (0, 0, 0))
            for e in old_enemies:
                draw_enemy(e, (0, 0, 0))
            for s in shots:
                s[1] -= 5
            shots = [s for s in shots if s[1] > 20]
            for e in enemies:
                e[1] += 0.5
                if e[1] > 172:
                    game_over("Invaded!", score)
                    return
            for s in shots[:]:
                hit = -1
                for i, e in enumerate(enemies):
                    if abs(s[0] - e[0]) < 10 and abs(s[1] - e[1]) < 9:
                        hit = i
                        break
                if hit >= 0:
                    shots.remove(s)
                    enemies[hit] = [randint(20, 299), randint(25, 80)]
                    score += 1
                    game_score("Space", score)
            draw_ship(x, CYAN)
            for s in shots:
                rect(s[0] - 1, s[1], 3, 7, YELLOW)
            for e in enemies:
                draw_enemy(e, RED)

def run():
    names=["Snake","Pong","Tetris","Breakout","Flappy","Minesweeper","2048","Space"]
    s=0
    while True:
        clear_screen(); header("Games")
        for i,n in enumerate(names):
            y=29+i*20; rect(12,y,296,18,CARD2 if i==s else CARD); txt(22,y+13,n,WHITE if i==s else MUTED)
        footer("ARROWS Select  ENTER Open  CLEAR Back")
        k=wait_key()
        if k==CLEAR: return
        if k==DOWN: s=min(7,s+1)
        elif k==UP: s=max(0,s-1)
        elif k==ENTER:
            fn=[snake,pong,tetris,breakout,flappy,mines,game2048,space_game][s]
            fn()


boot();home()

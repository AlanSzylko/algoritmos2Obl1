from math import atan2,cos,sin,pi
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,Color,white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

W,H=595.28,841.89
C={'ink':'#163247','muted':'#587080','teal':'#008B83','blue':'#3266D5','coral':'#D35740','purple':'#7757BC','amber':'#AC7509','light':'#F0F5F8','line':'#D7E2E9','paleTeal':'#E6F5F0','paleBlue':'#EDF2FD','paleCoral':'#FCEFE9','palePurple':'#F3EFFB'}
def color(v):return HexColor(C.get(v,v))
def fonts():
    for n,f in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Italic','ariali.ttf'),('Mono','consola.ttf'),('Symbols','seguisym.ttf')]:
        pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
def markup(s):
    import re
    s=escape(str(s));s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    cmap=pdfmetrics.getFont('Body').face.charToGlyph
    return ''.join(c if ord(c)<128 or ord(c) in cmap else '<font name="Symbols">'+c+'</font>' for c in s)
def p(c,x,y,w,s,size=10.5,col='ink',bold=False,leading=None):
    st=ParagraphStyle('v',fontName='Bold' if bold else 'Body',fontSize=size,leading=leading or size*1.35,textColor=color(col))
    ob=Paragraph(markup(s),st);_,h=ob.wrap(w,1000);ob.drawOn(c,x,H-y-h);return h
def line(c,x1,y1,x2,y2,col='line',width=1,dash=None):
    c.saveState();c.setStrokeColor(color(col));c.setLineWidth(width)
    if dash:c.setDash(dash)
    c.line(x1,H-y1,x2,H-y2);c.restoreState()
def arrow(c,x1,y1,x2,y2,col='ink',width=2,head=7,dash=None):
    line(c,x1,y1,x2,y2,col,width,dash)
    a=atan2(y2-y1,x2-x1)
    for da in [-.45,.45]:line(c,x2,y2,x2-head*cos(a+da),y2-head*sin(a+da),col,width)
def rect(c,x,y,w,h,fill='light',stroke=None,r=9):
    c.saveState();c.setFillColor(color(fill));c.setStrokeColor(color(stroke or fill));c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke));c.restoreState()
def circle(c,x,y,r=3,fill='ink',stroke=None):
    c.saveState();c.setFillColor(color(fill));c.setStrokeColor(color(stroke or fill));c.circle(x,H-y,r,stroke=bool(stroke),fill=1);c.restoreState()
def poly(c,pts,fill='paleTeal',stroke='teal',alpha=.7):
    c.saveState();c.setFillColor(color(fill));c.setStrokeColor(color(stroke));c.setFillAlpha(alpha);path=c.beginPath();path.moveTo(pts[0][0],H-pts[0][1])
    for x,y in pts[1:]:path.lineTo(x,H-y)
    path.close();c.drawPath(path,fill=1,stroke=1);c.restoreState()
def chip(c,x,y,w,s,col='teal',fill='paleTeal'):
    rect(c,x,y,w,31,fill,r=6);p(c,x+10,y+7,w-20,s,10,col,True)
def card(c,x,y,w,h,title,body,col='teal',fill='light'):
    rect(c,x,y,w,h,fill);rect(c,x,y,4,h,col,r=0)
    p(c,x+14,y+12,w-28,title,11,col,True)
    p(c,x+14,y+34,w-28,body,10.4)
def note(c,y,title,text,col='teal'):
    card(c,38,y,519,77,title,text,col)
def steps(c,y,items):
    for i,(title,body) in enumerate(items):
        top=y+i*68
        circle(c,53,top+15,14,'teal');p(c,45,top+7,20,str(i+1),12,'#FFFFFF',True)
        p(c,79,top,465,title,11,'ink',True);p(c,79,top+21,465,body,10.2)
def header(c,chapter,title,subtitle):
    rect(c,0,0,W,8,'teal',r=0)
    p(c,38,31,519,f'TEMA {chapter}  /  EXPLICACIÓN VISUAL',9,'teal',True)
    used=p(c,38,54,519,title,24,'ink',True,leading=28)
    p(c,38,62+used,519,subtitle,10.8,'muted')
def matrix(c,x,y,rows,label=None,cols=None,cellw=29,cellh=28,fill='light',size=13):
    n=len(rows);m=len(rows[0]);w=m*cellw+18;h=n*cellh+14
    if label:p(c,x,y-26,w+20,label,11,'ink',True)
    rect(c,x,y,w,h,fill,r=7)
    if cols:
        for j,col in cols.items():rect(c,x+9+j*cellw,y+7,cellw,n*cellh,col,r=4)
    for i,row in enumerate(rows):
        for j,v in enumerate(row):p(c,x+12+j*cellw,y+9+i*cellh,cellw-2,str(v),size)
    line(c,x+5,y+7,x+5,y+h-7,'ink',1.2);line(c,x+5,y+7,x+9,y+7,'ink',1.2);line(c,x+5,y+h-7,x+9,y+h-7,'ink',1.2)
    line(c,x+w-5,y+7,x+w-5,y+h-7,'ink',1.2);line(c,x+w-9,y+7,x+w-5,y+7,'ink',1.2);line(c,x+w-9,y+h-7,x+w-5,y+h-7,'ink',1.2)
    return w,h
def axes(c,x,y,w,h,xmin=-1,xmax=4,ymin=-1,ymax=4,grid=True):
    def pt(a,b):return x+(a-xmin)/(xmax-xmin)*w,y+h-(b-ymin)/(ymax-ymin)*h
    if grid:
        for a in range(int(xmin),int(xmax)+1):
            xx,yy=pt(a,0);line(c,xx,y,xx,y+h,'line',.5)
        for b in range(int(ymin),int(ymax)+1):
            xx,yy=pt(0,b);line(c,x,yy,x+w,yy,'line',.5)
    xx,yy=pt(0,0);arrow(c,x,yy,x+w+4,yy,'muted',.9,4);arrow(c,xx,y+h,xx,y-4,'muted',.9,4)
    p(c,x+w+5,yy-4,15,'x',9,'muted');p(c,xx+5,y-14,18,'y',9,'muted');circle(c,xx,yy,2,'muted')
    return pt
def vec(c,pt,v,col='teal',start=(0,0),label=None,offset=(5,-15),width=2.6,dash=None):
    a=pt(*start);b=pt(*v);arrow(c,*a,*b,col,width,dash=dash)
    if label:p(c,b[0]+offset[0],b[1]+offset[1],100,label,10,col,True)

def combination(c):
    header(c,1,'Una combinación lineal se puede ver','Moverse en direcciones conocidas para construir un vector nuevo.')
    pt=axes(c,57,181,290,248,-.5,4,-.5,3)
    poly(c,[pt(0,0),pt(2,0),pt(3,2),pt(1,2)],'paleTeal','line',.7)
    vec(c,pt,(2,0),'teal',label='u = (2,0)',offset=(-45,12))
    vec(c,pt,(1,2),'coral',label='v = (1,2)',offset=(-55,-24))
    vec(c,pt,(3,2),'purple',label='u + v',offset=(7,-6))
    vec(c,pt,(3,2),'coral',start=(2,0),width=1.3,dash=[4,3])
    vec(c,pt,(3,2),'teal',start=(1,2),width=1.3,dash=[4,3])
    card(c,386,178,169,112,'SUMAR','Trasladá v al extremo de u. El destino es u + v.','teal','paleTeal')
    card(c,386,307,169,117,'ESCALAR','2u llega al doble de distancia. -u invierte el sentido.','coral','paleCoral')
    chip(c,76,475,443,'(2,0) + (1,2) = (3,2)','purple','palePurple')
    steps(c,538,[('Elegí las direcciones','Los generadores son u y v; no tienen por qué ser los ejes canónicos.'),('Elegí los coeficientes','αu + βv permite escalar cada dirección por separado.'),('Recorré todas las combinaciones','El conjunto de destinos posibles es s.g.(u,v). Aquí es todo R².')])
def subspace(c):
    header(c,1,'Subespacio e independencia','Dos preguntas distintas: ¿hay cierre? ¿sobran direcciones?')
    for x,title in [(47,'SÍ: recta y = x'),(322,'NO: recta y = x + 1')]:
        p(c,x,164,230,title,12,'teal' if x==47 else 'coral',True)
    a=axes(c,61,208,204,162,-2,2,-2,2);line(c,*a(-1.8,-1.8),*a(1.8,1.8),'teal',3)
    b=axes(c,336,208,204,162,-2,2,-2,2);line(c,*b(-2,-1),*b(1,2),'coral',3);circle(c,*b(0,0),5,'#FFFFFF','coral')
    p(c,47,389,232,'Contiene 0 y cualquier combinación de sus vectores permanece en la recta.',10.5)
    p(c,322,389,232,'No contiene 0. Por eso no puede ser subespacio.',10.5)
    line(c,38,455,557,455)
    p(c,47,475,230,'L.I.: dos direcciones distintas',12,'teal',True)
    p(c,322,475,230,'L.D.: una dirección repetida',12,'coral',True)
    a=axes(c,67,520,193,142,-.5,3,-.5,2.5);vec(c,a,(2,0),'teal',label='u',offset=(-3,10));vec(c,a,(1,2),'coral',label='v')
    b=axes(c,342,520,193,142,-.5,3,-.5,2.5);vec(c,b,(2.5,1.25),'coral',label='v = 2u',offset=(-33,-22));vec(c,b,(1.25,.625),'teal',label='u',offset=(-18,8))
    p(c,47,691,238,'αu + βv = 0 obliga a α = β = 0. Dos vectores L.I. forman base de R².',10.4)
    p(c,322,691,233,'2u - v = 0 es una relación no trivial: los coeficientes son 2 y -1. El segundo vector no agrega dirección.',10.4)
def intersection(c):
    header(c,1,'Sumar no es unir: la parte compartida','La intersección cuenta una sola vez; la suma reúne todas las combinaciones.')
    o=(175,341)
    def pt(x,y,z):return(o[0]+62*x+62*y,o[1]+30*x-30*y-75*z)
    poly(c,[pt(-1,0,-1),pt(1,0,-1),pt(1,0,1),pt(-1,0,1)],'paleBlue','blue',.72)
    poly(c,[pt(0,-1,-1),pt(0,1,-1),pt(0,1,1),pt(0,-1,1)],'paleCoral','coral',.6)
    arrow(c,*pt(-1.4,0,0),*pt(1.6,0,0),'muted',1);arrow(c,*pt(0,-1.4,0),*pt(0,1.6,0),'muted',1)
    arrow(c,*pt(0,0,-1.4),*pt(0,0,1.6),'purple',3)
    p(c,51,187,220,'U: y = 0 (plano xz)',11,'blue',True)
    p(c,51,212,220,'W: x = 0 (plano yz)',11,'coral',True)
    p(c,195,238,135,'U ∩ W: eje z',10,'purple',True)
    card(c,365,201,187,92,'INTERSECCIÓN','Lo que pertenece a los dos planos: el eje z.','purple','palePurple')
    card(c,365,312,187,104,'SUMA','Entre ambos permiten construir cualquier (x,y,z): U + W = R³.','teal','paleTeal')
    chip(c,67,496,460,'dim(U + W) = 2 + 2 - 1 = 3','purple','palePurple')
    p(c,48,554,260,'¿Cuándo es directa?',16,'ink',True)
    pt2=axes(c,62,605,170,115,-.3,3,-.3,2)
    vec(c,pt2,(2.5,0),'teal');vec(c,pt2,(0,1.5),'coral');vec(c,pt2,(2.5,1.5),'purple')
    card(c,279,591,275,125,'SI SOLO COMPARTEN EL CERO','En R², el eje x y el eje y tienen intersección {0}. Cada vector se descompone de manera única: (a,b) = (a,0) + (0,b).','teal','light')
def kernel(c):
    header(c,2,'Núcleo e imagen: lo que se pierde y queda','T(x,y) = (x,0). La proyección conserva x y elimina y.')
    p(c,54,163,200,'DOMINIO: R²',11,'blue',True);p(c,349,163,200,'CODOMINIO: R²',11,'blue',True)
    a=axes(c,57,208,184,225,-1,3,-2,3);b=axes(c,349,208,184,225,-1,3,-2,3)
    line(c,*a(0,-1.8),*a(0,2.8),'coral',4)
    line(c,*b(-.8,0),*b(2.8,0),'teal',4)
    for q in [(2,2),(2,-1)]:circle(c,*a(*q),5,'purple')
    line(c,*a(2,-1),*a(2,2),'purple',1,[3,3]);circle(c,*b(2,0),5,'purple');circle(c,*b(0,0),5,'coral')
    arrow(c,261,309,326,309,'ink',2);p(c,267,276,62,'T',16,'ink',True)
    p(c,50,449,219,'(2,2) y (2,-1) tienen la misma imagen: (2,0).',10.5,'purple')
    p(c,342,449,219,'Todas las salidas están sobre el eje x.',10.5,'teal')
    card(c,39,518,250,109,'NÚCLEO: EN LA ENTRADA','N(T) = {(0,y)}. Toda la recta vertical termina en el cero. Su dimensión es 1.','coral','paleCoral')
    card(c,307,518,250,109,'IMAGEN: EN LA SALIDA','Im(T) = {(x,0)}. Es el conjunto de resultados posibles. Su dimensión es 1.','teal','paleTeal')
    chip(c,71,668,455,'dim(dominio) = nulidad + rango: 2 = 1 + 1','blue','paleBlue')
    p(c,50,728,505,'No es inyectiva: distintas entradas coinciden. No es sobreyectiva en R²: nunca sale un vector con y ≠ 0.',10.5)
def maps(c):
    header(c,2,'Inyectiva, sobreyectiva y biyectiva','El codominio forma parte del problema: no alcanza con mirar la fórmula.')
    data=[('Inyectiva','T: R → R², T(t) = (t,0)','Cada entrada tiene una salida distinta, pero queda parte del codominio sin alcanzar.','n = 1   rango = 1   m = 2','teal'),('Sobreyectiva','T: R² → R, T(x,y) = x','Se alcanza todo R; diferentes valores de y pueden producir la misma salida.','n = 2   rango = 1   m = 1','blue'),('Biyectiva','T: R² → R², T(x,y) = (2x,y)','No pierde información y alcanza todo R². Tiene inversa: (u,v) ↦ (u/2,v).','n = 2   rango = 2   m = 2','purple')]
    for i,(title,formula,body,dims,col) in enumerate(data):
        y=161+i*178;rect(c,38,y,519,157,'light')
        p(c,55,y+14,290,title,17,col,True);p(c,55,y+41,470,formula,11,'ink',True)
        p(c,219,y+72,320,body,10.3);p(c,219,y+121,325,dims,10,col,True)
        if i==0:
            line(c,67,y+113,99,y+113,col,4);arrow(c,112,y+113,147,y+113);rect(c,161,y+82,40,57,'#FFFFFF','line',0);line(c,164,y+113,198,y+113,col,3)
        elif i==1:
            rect(c,63,y+82,40,57,'#FFFFFF','line',0)
            for dy in [-15,0,15]:line(c,68,y+113+dy,99,y+113+dy,col,1.3)
            arrow(c,115,y+113,151,y+113);line(c,165,y+113,200,y+113,col,4)
        else:
            rect(c,60,y+85,36,49,'palePurple',col,0);arrow(c,109,y+111,146,y+111);rect(c,160,y+85,46,49,'palePurple',col,0)
    chip(c,48,716,499,'Inyectiva: rango = n. Sobreyectiva: rango = m.','blue','paleBlue')
def columns(c):
    header(c,3,'Las imágenes se convierten en columnas','A representa T(x,y) = (x+y, 2y) en la base canónica.')
    card(c,40,164,243,101,'ENTRADA 1: e₁ = (1,0)','T(e₁) = (1,0). Esta será la primera columna de A.','teal','paleTeal')
    card(c,311,164,243,101,'ENTRADA 2: e₂ = (0,1)','T(e₂) = (1,2). Esta será la segunda columna de A.','coral','paleCoral')
    arrow(c,160,278,249,321,'teal');arrow(c,427,278,294,321,'coral')
    p(c,185,357,40,'A =',15,'ink',True)
    matrix(c,226,331,[[1,1],[0,2]],cols={0:'paleTeal',1:'paleCoral'},cellw=45,cellh=38,size=17)
    p(c,70,470,440,'Multiplicar por una columna es combinar imágenes',15,'ink',True)
    matrix(c,54,517,[[1,1],[0,2]],cols={0:'paleTeal',1:'paleCoral'})
    matrix(c,144,517,[[2],[1]],cellw=28);p(c,201,537,35,'=',18)
    p(c,239,537,24,'2',18,'teal',True);matrix(c,262,517,[[1],[0]],fill='paleTeal')
    p(c,325,537,28,'+',18);matrix(c,362,517,[[1],[2]],fill='paleCoral')
    p(c,420,537,35,'=',18);matrix(c,461,517,[[3],[2]],fill='palePurple')
    steps(c,648,[('La entrada (2,1) significa 2e₁ + e₂','Por linealidad: T(2e₁ + e₂) = 2T(e₁) + T(e₂).'),('Regla general: columna j = [T(bⱼ)]_C','Si C no es canónica, primero calculá las coordenadas de T(bⱼ) en C.')])
def compose(c):
    header(c,3,'El orden cambia el resultado','Ejercicio 1.12: R rota 45°; S proyecta sobre el eje x. Partimos de e₂.')
    titles=[('Primero S; después R',185,'teal'),('Primero R; después S',448,'coral')]
    for title,y,col in titles:
        p(c,44,y-30,500,title,15,col,True)
        for j in range(3):
            pt=axes(c,58+j*179,y+24,118,124,-1.2,1.2,-.4,1.4)
            vv=[(0,1),(0,0),(0,0)] if col=='teal' else [(0,1),(-.707,.707),(-.707,0)]
            if vv[j]==(0,0):circle(c,*pt(0,0),5,col)
            else:vec(c,pt,vv[j],col,width=2.4)
            if j<2:
                arrow(c,185+j*179,y+82,219+j*179,y+82,col,1.7)
                p(c,188+j*179,y+54,31,('S' if j==0 else 'R') if col=='teal' else ('R' if j==0 else 'S'),12,col,True)
        labs=['(0,1)','(0,0)','(0,0)'] if col=='teal' else ['(0,1)','(-1/√2, 1/√2)','(-1/√2, 0)']
        for j,lab in enumerate(labs):p(c,57+j*179,y+168,146,lab,10.6,col,True)
    note(c,699,'CONCLUSIÓN','R∘S ≠ S∘R. En el producto de matrices, la operación de la derecha se aplica primero.','purple')
def basis(c):
    header(c,4,'Un mismo vector, dos listas de coordenadas','Ejemplo original: B canónica; B′ = ((1,1),(1,2)); v = (3,4).')
    for i in [0,1]:
        x=50+i*278;p(c,x,166,238,'BASE CANÓNICA B' if i==0 else 'BASE NUEVA B′',11,'blue' if i==0 else 'purple',True)
        pt=axes(c,x+10,214,205,230,-.5,4,-.5,5)
        vec(c,pt,(3,4),'ink',label='v',offset=(8,-8))
        if i==0:
            vec(c,pt,(3,0),'blue',label='3e₁',offset=(-30,12));vec(c,pt,(3,4),'coral',start=(3,0),width=1.6,dash=[3,2]);p(c,x+150,338,55,'4e₂',10,'coral',True)
        else:
            vec(c,pt,(2,2),'teal',label='2b′₁',offset=(-50,3));vec(c,pt,(3,4),'coral',start=(2,2),width=2,label='b′₂',offset=(10,12))
        chip(c,x,483,232,'[v]_B = (3,4)' if i==0 else '[v]_B′ = (2,1)','blue' if i==0 else 'purple','paleBlue' if i==0 else 'palePurple')
    matrix(c,79,575,[[1,1],[1,2]],'P: nuevas → viejas',cellw=32)
    matrix(c,185,575,[[2],[1]],cellw=29);p(c,240,593,35,'=',18);matrix(c,283,575,[[3],[4]],cellw=29)
    card(c,377,553,175,118,'EL VECTOR NO CAMBIA','P tiene las bases nuevas escritas en las viejas. P⁻¹ hace el recorrido inverso.','purple','palePurple')
    p(c,53,722,501,'v = 3e₁ + 4e₂ = 2b′₁ + b′₂. Confundir v con sus coordenadas invierte fácilmente el sentido del pasaje.',11)
def pipeline(c):
    header(c,4,'Cómo recordar Q⁻¹AP sin memorizarlo','Seguí lo que le ocurre a una entrada escrita en la base nueva.')
    labels=[('[v]_B′','Entrada nueva'),('[v]_B','Entrada vieja'),('[T(v)]_C','Salida vieja'),('[T(v)]_C′','Salida nueva')]
    for i,(lab,desc) in enumerate(labels):
        x=39+i*139;rect(c,x,224,100,80,'palePurple' if i in [0,3] else 'paleBlue');p(c,x+9,242,84,lab,13,'ink',True);p(c,x+9,272,84,desc,8.8,'muted')
        if i<3:
            arrow(c,x+104,262,x+132,262,'teal',2)
            p(c,x+106,225,44,['P','A','Q⁻¹'][i],12,'teal',True)
    line(c,87,310,87,382,'purple',1.6);arrow(c,87,382,506,382,'purple',1.6);line(c,506,382,506,310,'purple',1.6)
    chip(c,191,365,218,'A′ = Q⁻¹ A P','purple','palePurple')
    steps(c,451,[('P: traducí la entrada a la base vieja','[v]_B = P[v]_B′.'),('A: aplicá la transformación','[T(v)]_C = A[v]_B.'),('Q⁻¹: traducí la salida a la base nueva','[T(v)]_C′ = Q⁻¹[T(v)]_C.')])
    note(c,699,'SI CAMBIÁS LA MISMA BASE A AMBOS LADOS','Para un operador V → V, Q = P y queda A′ = P⁻¹AP. Ese caso es la semejanza.','blue')
def rank(c):
    header(c,5,'Rango: contar direcciones independientes','Ejemplo del curso: cuatro columnas, pero solo dos aportan información nueva.')
    matrix(c,49,214,[[1,2,0,1],[0,0,1,1],[2,4,0,2]],'MATRIZ ORIGINAL',cols={0:'paleTeal',2:'paleCoral'},cellw=34,cellh=32,size=14)
    arrow(c,239,270,311,270,'ink');p(c,236,226,89,'F₃ - 2F₁',10,'muted',True)
    matrix(c,339,214,[[1,2,0,1],[0,0,1,1],[0,0,0,0]],'ESCALONADA',cols={0:'paleTeal',2:'paleCoral'},cellw=34,cellh=32,size=14)
    chip(c,46,366,228,'A₂ = 2A₁','teal','paleTeal');chip(c,321,366,228,'A₄ = A₁ + A₃','coral','paleCoral')
    card(c,44,441,250,115,'DOS PIVOTES → RANGO 2','Las columnas 1 y 3 originales forman una base de Im(A).','teal','paleTeal')
    card(c,313,441,240,115,'CUATRO VARIABLES → NULIDAD 2','dim N(A) = número de columnas - rango = 4 - 2.','blue','paleBlue')
    note(c,595,'NO CAMBIES LA BASE DE LA IMAGEN POR ERROR','Gauss conserva el rango y las dependencias entre columnas. Para Im(A), elegí las columnas pivote de la matriz ORIGINAL.','coral')
    p(c,54,712,492,'La imagen de A cumple z = 2x; la de la escalonada cumple z = 0. Tienen la misma dimensión, pero son subespacios diferentes.',10.8)
def similarity(c):
    header(c,5,'Semejanza: la representación cambia','Cambiar de base conserva características del mismo operador.')
    matrix(c,76,213,[[2,1],[0,2]],'A',cellw=40,cellh=35,size=16)
    arrow(c,211,260,370,260,'purple');p(c,223,213,150,'B = P⁻¹AP',13,'purple',True)
    matrix(c,411,213,[[2,0],[1,2]],'B',cellw=40,cellh=35,size=16)
    p(c,117,328,388,'Aquí P intercambia los dos vectores de la base.',10.7,'muted')
    rows=[('Propiedad','A','B'),('Traza','4','4'),('Determinante','4','4'),('Rango','2','2'),('Polinomio característico','(2-λ)²','(2-λ)²')]
    for i,row in enumerate(rows):
        y=390+i*42;rect(c,47,y,502,40,'palePurple' if i==0 else ('light' if i%2 else '#FFFFFF'),r=0)
        for x,w,s in zip([62,334,454],[250,100,85],row):p(c,x,y+11,w,s,11,'purple' if i==0 else 'ink',i==0)
    note(c,656,'MISMO INVARIANTE NO SIGNIFICA SEMEJANZA','I₂ y [[1,1],[0,1]] tienen igual traza, determinante, rango y polinomio, pero no son semejantes.','coral')
def eigen(c):
    header(c,6,'Un vector propio mantiene su recta','A = diag(2,-1). El resultado Av debe ser un único múltiplo de v.')
    cards=[('u = (1,0)','Au = 2u',(1,0),(2,0),'teal'),('v = (0,1)','Av = -v',(0,1),(0,-1),'blue'),('w = (1,1)','Aw = (2,-1)',(1,1),(2,-1),'coral')]
    for i,(t1,t2,v,av,col) in enumerate(cards):
        x=37+i*181;rect(c,x,170,164,313,'light');p(c,x+11,187,143,t1,12,col,True)
        pt=axes(c,x+20,238,121,163,-.6,2.6,-1.5,1.6)
        vec(c,pt,av,col,width=2.8);vec(c,pt,v,'muted',width=1.7,dash=[3,2]);circle(c,*pt(*v),3,'#FFFFFF','muted')
        p(c,x+11,431,145,t2,11,col,True)
    chip(c,42,508,157,'SÍ: λ = 2','teal','paleTeal');chip(c,220,508,157,'SÍ: λ = -1','blue','paleBlue');chip(c,398,508,157,'NO es propio','coral','paleCoral')
    steps(c,570,[('Calculá Av','En cada panel, el vector gris punteado es la entrada y el de color es la salida.'),('Compará todas las coordenadas','Para w, la primera exige λ = 2 y la segunda λ = -1. No sirve un único λ.'),('Describí el subespacio','E₂ es el eje x; E₋₁ es el eje y. El cero pertenece a ellos, pero no es vector propio.')])
def eigenspaces(c):
    header(c,6,'Las raíces dan valores; los sistemas dan vectores','Ejercicio 2.4(b): B(x,y,z) = (x,z,y).')
    matrix(c,65,185,[[1,0,0],[0,0,1],[0,1,0]],'B',cellw=29,cellh=25)
    arrow(c,205,224,269,224,'ink');card(c,292,176,260,107,'POLINOMIO CARACTERÍSTICO','χ_B(λ) = (1-λ)²(-1-λ). Raíces: 1 (dos veces) y -1.','purple','palePurple')
    line(c,407,292,407,324,'purple');line(c,163,324,432,324,'purple');arrow(c,163,324,163,358,'teal');arrow(c,432,324,432,358,'coral')
    card(c,40,369,250,176,'λ = 1: resolvé (B-I)v = 0','(x,z,y) = (x,y,z) → y = z. Quedan libres x e y. Base: (1,0,0), (0,1,1).','teal','paleTeal')
    card(c,307,369,250,176,'λ = -1: resolvé (B+I)v = 0','(x,z,y) = (-x,-y,-z) → x = 0, z = -y. Base: (0,1,-1).','coral','paleCoral')
    chip(c,53,568,223,'dim E₁ = 2: un plano','teal','paleTeal');chip(c,321,568,223,'dim E₋₁ = 1: una recta','coral','paleCoral')
    p(c,50,632,506,'No elijas solamente un vector para λ = 1: su sistema tiene dos parámetros libres. Necesitás dos vectores independientes para describir el plano propio completo.',11)
    note(c,704,'PUENTE HACIA DIAGONALIZACIÓN','Estas bases aportan 2 + 1 = 3 vectores propios L.I. Alcanzan para formar una base de R³.','purple')
def diagonal(c):
    header(c,7,'Una base propia separa las direcciones','Ejercicio 2.8(i): A = [[0,2],[2,0]]. P usa (1,1) y (1,-1).')
    left=axes(c,58,208,195,211,-2,3,-2,3);vec(c,left,(1,1),'teal',label='v₁',offset=(-31,-15));vec(c,left,(1,-1),'coral',label='v₂');vec(c,left,(2,2),'teal',label='Av₁ = 2v₁',offset=(-57,-23));vec(c,left,(-2,2),'coral',label='Av₂ = -2v₂',offset=(2,-25))
    card(c,337,198,218,104,'PRIMERA DIRECCIÓN','A multiplica por 2 a v₁=(1,1).','teal','paleTeal')
    card(c,337,320,218,104,'SEGUNDA DIRECCIÓN','A multiplica por -2 a v₂=(1,-1): invierte su sentido.','coral','paleCoral')
    matrix(c,63,491,[[1,1],[1,-1]],'P',cols={0:'paleTeal',1:'paleCoral'},cellw=32)
    p(c,190,514,196,'D = P⁻¹AP =',16,'purple',True)
    matrix(c,397,491,[[2,0],[0,-2]],cols={0:'paleTeal',1:'paleCoral'},cellw=36)
    chip(c,43,613,515,'(3,1)  → P⁻¹ →  (2,1)  → D →  (4,-2)  → P →  (2,6)','purple','palePurple')
    steps(c,685,[('Traducí, escalá y reconstruí','A(3,1)=(2,6). En coordenadas propias, D actúa por separado sobre cada componente.')])
def multiplicities(c):
    header(c,7,'Una raíz repetida no decide por sí sola','Compará cuántos vectores propios independientes tiene cada matriz.')
    matrix(c,92,188,[[2,0],[0,2]],'A = 2I',cellw=37)
    matrix(c,372,188,[[2,1],[0,2]],'J',cellw=37)
    chip(c,41,296,515,'Las dos tienen χ(λ) = (2-λ)²: multiplicidad algebraica 2','purple','palePurple')
    a=axes(c,72,363,180,166,-1.5,1.5,-1.5,1.5)
    for v in [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1)]:vec(c,a,v,'teal',width=1.8)
    b=axes(c,352,363,180,166,-1.5,1.5,-1.5,1.5);line(c,*b(-1.4,0),*b(1.4,0),'coral',3);vec(c,b,(1,0),'coral');vec(c,b,(-1,0),'coral')
    card(c,40,558,250,124,'E₂(A) = R²','m.g.(2)=2. Hay dos direcciones L.I. y A es diagonalizable.','teal','paleTeal')
    card(c,308,558,250,124,'E₂(J) = eje x','m.g.(2)=1. Falta una dirección propia: J no es diagonalizable.','coral','paleCoral')
    p(c,52,722,502,'m.a. cuenta repeticiones de una raíz. m.g. cuenta dimensiones de su subespacio propio. Para diagonalizar deben coincidir para cada raíz.',11)
def decision(c):
    header(c,7,'Árbol de decisión para diagonalizar','Usalo después de calcular el polinomio característico y fijar el cuerpo K.')
    rect(c,129,166,332,64,'palePurple');p(c,149,181,293,'¿χ_A tiene sus n raíces en K, contando multiplicidades?',12,'purple',True)
    arrow(c,129,200,65,200,'coral');line(c,65,200,65,276,'coral');arrow(c,65,276,139,276,'coral');p(c,77,236,48,'NO',10,'coral',True)
    chip(c,142,260,317,'No es diagonalizable sobre K','coral','paleCoral')
    arrow(c,461,200,527,200,'teal');line(c,527,200,527,348,'teal');arrow(c,527,348,454,348,'teal');p(c,529,268,30,'SÍ',10,'teal',True)
    rect(c,140,321,314,64,'paleBlue');p(c,158,336,278,'Para cada raíz λ: calculá E_λ = N(A-λI) y su dimensión.',12,'blue',True)
    arrow(c,297,389,297,427,'ink')
    rect(c,141,435,312,61,'palePurple');p(c,160,451,274,'¿m.g.(λ) = m.a.(λ) para TODAS las raíces?',12,'purple',True)
    arrow(c,142,466,68,466,'coral');line(c,68,466,68,556,'coral');arrow(c,68,556,138,556,'coral');p(c,76,506,47,'NO',10,'coral',True)
    chip(c,142,541,182,'No diagonalizable','coral','paleCoral')
    arrow(c,453,466,524,466,'teal');line(c,524,466,524,634,'teal');arrow(c,524,634,454,634,'teal');p(c,531,541,28,'SÍ',10,'teal',True)
    card(c,140,599,314,86,'CONSTRUÍ P Y D','P: bases propias como columnas. D: valores propios en el MISMO orden.','teal','paleTeal')
    note(c,716,'CONTROL FINAL','Verificá AP = PD y det(P) ≠ 0. Con parámetros, separá antes los valores que hacen coincidir las raíces.','blue')

VISUALS={1:[('Combinaciones lineales',combination),('Subespacio e independencia',subspace),('Suma e intersección',intersection)],2:[('Núcleo e imagen',kernel),('Tipos de transformaciones',maps)],3:[('Construir una matriz por columnas',columns),('Orden de composición',compose)],4:[('Dos bases, un vector',basis),('Recorrido del cambio de base',pipeline)],5:[('Rango y pivotes',rank),('Invariantes de semejanza',similarity)],6:[('Reconocer vectores propios',eigen),('De raíces a subespacios',eigenspaces)],7:[('La base propia',diagonal),('Multiplicidades comparadas',multiplicities),('Decidir si diagonaliza',decision)]}

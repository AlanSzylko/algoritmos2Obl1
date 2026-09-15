from pathlib import Path
from xml.sax.saxutils import escape
import re,json
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image,Preformatted,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parents[2]/'output'/'pdf'/'Resumen_completo_Ingenieria_de_Software_y_Git.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf'),('Mono','consola.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
CROPS={
 's48':(.12,.11,.91,.40),'s51':(.12,.11,.91,.36),'s53':(.12,.10,.93,.25),
 's56':(.10,.10,.93,.36),'s57':(.12,.11,.93,.44),'s63':(.12,.11,.93,.25),
 's67':(.12,.10,.93,.57),'s69':(.12,.10,.93,.25),'g17':(.075,.089,.925,.808),
 'g19':(.075,.500,.925,.736),'g21':(.075,.562,.925,.898),'g31':(.075,.253,.925,.507),
 'g67':(.075,.446,.925,.802),'g76':(.075,.310,.925,.602),'g77':(.075,.038,.925,.282),
 'g89':(.075,.038,.925,.483),'g96':(.075,.710,.925,.891)}
for key,box in CROPS.items():
 im=PILImage.open(ROOT/(key+'.png'));w,h=im.size
 im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(box))).save(ROOT/(key+'_crop.png'))

navy=HexColor('#153549');teal=HexColor('#087d88');ink=HexColor('#203442');muted=HexColor('#536879')
styles={
 'h1':ParagraphStyle('h1',fontName='Arial-Bold',fontSize=21,leading=25,textColor=navy,spaceAfter=14,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='Arial-Bold',fontSize=12,leading=16,textColor=teal,spaceBefore=8,spaceAfter=7,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=10.1,leading=14.0,textColor=ink,spaceAfter=8),
 'bullet':ParagraphStyle('bullet',fontName='Arial',fontSize=10,leading=13.7,textColor=ink,leftIndent=11,firstLineIndent=-8,spaceAfter=5),
 'caption':ParagraphStyle('caption',fontName='Arial-Italic',fontSize=8.3,leading=10.5,textColor=muted,spaceBefore=5,spaceAfter=10),
 'source':ParagraphStyle('source',fontName='Arial-Italic',fontSize=8.3,leading=11,textColor=muted,spaceBefore=5,spaceAfter=7),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=9,leading=12,textColor=navy,backColor=HexColor('#eef4f6'),borderPadding=8,spaceBefore=4,spaceAfter=12),
 'qa':ParagraphStyle('qa',fontName='Arial',fontSize=10,leading=14,textColor=ink,spaceAfter=13),
}
def inline(t):
 t=escape(t)
 t=re.sub(r'`([^`]+)`',lambda m:'<font name="Mono" size="9">'+m.group(1)+'</font>',t)
 t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
 return t

class Doc(SimpleDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='h1':
   text=f.getPlainText();key='section'+str(len(outlines));self.canv.bookmarkPage(key)
   self.canv.addOutlineEntry(text,key,0,False);outlines.append({'title':text,'page':self.page})
outlines=[]
def decorate(c,d):
 c.saveState();w,h=A4
 c.setFillColor(teal);c.rect(0,h-9,w,9,fill=1,stroke=0)
 c.setFont('Arial-Bold',8);c.setFillColor(muted)
 c.drawString(48,h-32,'INGENIERÍA DE SOFTWARE / SCM / GIT')
 c.setStrokeColor(HexColor('#d7e1e7'));c.line(48,43,w-48,43)
 c.setFont('Arial',8);c.drawString(48,28,'Guía de estudio · Sommerville 1-2 · Pro Git 1-3')
 c.drawRightString(w-48,28,str(d.page));c.restoreState()

story=[]
def parse_page(page):
 lines=page.strip().splitlines();i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('```'):
   block=[];i+=1
   while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
   story.append(Preformatted('\n'.join(block),styles['code']));i+=1;continue
  if line.startswith('@FIG '):
   key,caption=line[5:].split('|',1);path=ROOT/(key+'_crop.png')
   im=PILImage.open(path);iw,ih=im.size
   maxh={'g17':225,'s67':190,'g89':185,'g67':160,'g76':95,'g77':65}.get(key,130)
   scale=min(475/iw,maxh/ih)
   story.append(KeepTogether([Image(str(path),width=iw*scale,height=ih*scale),Paragraph(inline(caption),styles['caption'])]))
  elif line.startswith('# '):story.append(Paragraph(inline(line[2:]),styles['h1']))
  elif line.startswith('## '):story.append(Paragraph(inline(line[3:]),styles['h2']))
  elif line.startswith('- '):story.append(Paragraph('• '+inline(line[2:]),styles['bullet']))
  else:
   st='source' if line.startswith('Fuente:') else 'body'
   story.append(Paragraph(inline(line),styles[st]))
  i+=1

pages=(ROOT/'resumen.md').read_text(encoding='utf-8').strip().split('\n===\n')
for i,page in enumerate(pages):
 if i:story.append(PageBreak())
 parse_page(page)
groups=(ROOT/'preguntas.txt').read_text(encoding='utf-8').strip().split('\n---\n')
n=0
for j,g in enumerate(groups):
 lines=g.splitlines();story.append(PageBreak())
 parse_page('# '+str(27+j)+'. Preguntas: '+lines[0]+'\n\nTapá la respuesta e intentá justificarla antes de leer. Cada pregunta admite variantes de opción múltiple, verdadero/falso o respuesta breve.\n')
 for line in lines[1:]:
  q,a=line.split('|',1);n+=1
  story.append(Paragraph(f'<b>{n:02}. {inline(q)}</b><br/>{inline(a)}',styles['qa']))
assert n==100,n
for page in (ROOT/'practica.md').read_text(encoding='utf-8').strip().split('\n===\n'):
 story.append(PageBreak());parse_page(page.replace('16 recortes','17 recortes'))
doc=Doc(str(OUT),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=54,bottomMargin=55,
 title='Resumen completo - Ingeniería de Software, SCM y Git',author='Guía de estudio basada en Sommerville y Chacon/Straub',
 subject='Capítulos 1 y 2 de Sommerville y 1, 2 y 3 de Pro Git; preguntas y práctica',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
(ROOT/'outline.json').write_text(json.dumps(outlines,ensure_ascii=False,indent=2),encoding='utf-8')
r=PdfReader(OUT)
print(json.dumps({'output':str(OUT),'pages':len(r.pages),'questions':n,'figures':len(CROPS),'sections':outlines},ensure_ascii=False))

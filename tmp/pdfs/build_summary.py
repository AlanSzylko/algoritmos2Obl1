from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parent
OUT=Path('C:/Users/alans/ORT/Algoritmos2/Obl1/output/pdf/parcial 1 Algebra.pdf')
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Italic','ariali.ttf'),('Mono','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/'+file))
pdfmetrics.registerFont(TTFont('MathSymbols', 'C:/Windows/Fonts/seguisym.ttf'))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
styles={
 'title':ParagraphStyle('title',fontName='Bold',fontSize=28,leading=34,textColor=HexColor('#123348'),spaceAfter=20),
 'h':ParagraphStyle('h',fontName='Bold',fontSize=18,leading=23,textColor=HexColor('#123348'),spaceAfter=15,keepWithNext=True),
 'sub':ParagraphStyle('sub',fontName='Bold',fontSize=11.5,leading=15,textColor=HexColor('#087F8C'),spaceBefore=10,spaceAfter=6,keepWithNext=True),
 'p':ParagraphStyle('p',fontName='Body',fontSize=10.5,leading=15,spaceAfter=8),
 'eq':ParagraphStyle('eq',fontName='Body',fontSize=11,leading=16,backColor=HexColor('#EDF5F7'),borderPadding=8,spaceBefore=6,spaceAfter=13),
 'mono':ParagraphStyle('mono',fontName='Mono',fontSize=10,leading=13,spaceBefore=4,spaceAfter=10),
}
def para(t,style):
    t=escape(t)
    import re
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    cmap=pdfmetrics.getFont('Body').face.charToGlyph
    t=''.join(c if ord(c) in cmap or ord(c)<128 else '<font name="MathSymbols">'+c+'</font>' for c in t)
    return Paragraph(t,styles[style])
class NumberedCanvas(canvas.Canvas):
    def __init__(self,*a,**k): super().__init__(*a,**k);self.states=[]
    def showPage(self): self.states.append(dict(self.__dict__));self._startPage()
    def save(self):
        total=len(self.states)
        for state in self.states:
            self.__dict__.update(state)
            self.setStrokeColor(HexColor('#C5D8DE'));self.line(44,42,551,42)
            self.setFont('Body',8);self.setFillColor(HexColor('#526974'))
            self.drawString(44,28,'parcial 1 Algebra  |  Apunte completo: temas 1 a 7')
            self.drawRightString(551,28,f'{self._pageNumber} / {total}')
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

text=ROOT.joinpath('course_content.txt').read_text(encoding='utf-8')
story=[]
for pi,page in enumerate(text.split('\n===\n')):
    if pi: story.append(PageBreak())
    blocks=page.strip().split('\n\n')
    for b in blocks:
        if b.startswith('TITLE '):story.append(para(b[6:],'title'))
        elif b.startswith('# '):story.append(para(b[2:],'h'))
        elif b.startswith('## '):story.append(para(b[3:],'sub'))
        elif b.startswith('= '):story.append(para(b[2:].replace('\n','<br/>'),'eq'))
        elif b.startswith('MATRIX\n'):story.append(Preformatted(b[7:],styles['mono']))
        else:story.append(para(b.replace('\n',' '),'p'))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),rightMargin=44,leftMargin=44,topMargin=45,bottomMargin=57,title='parcial 1 Algebra',author='Apunte completo a partir de los materiales del curso')
doc.build(story,canvasmaker=NumberedCanvas)
import pymupdf
pdf=pymupdf.open(OUT)
import json
manifest=json.loads(ROOT.joinpath('course_manifest.json').read_text(encoding='utf-8'))
assert len(pdf)==manifest['pages'], f"Pagination differs: actual {len(pdf)}, expected {manifest['pages']}"
starts={v[0] for v in manifest['chapters'].values()}
toc=[]
for sec in manifest['sections']:
    page=sec['page']
    level=1 if page in starts or page<5 or page>manifest['chapters']['7'][1] else 2
    toc.append([level,sec['title'],page])
pdf.set_toc(toc)
pdf.saveIncr()
pdf.close()
print(OUT)

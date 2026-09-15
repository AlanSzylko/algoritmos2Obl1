import sympy as s
import pymupdf
from pathlib import Path
M=s.Matrix
A=M([[0,-1,0,0],[0,1,-2,0],[0,0,2,-3],[0,0,0,3]])
P=M([[1,-1,1,-1],[0,1,-2,3],[0,0,1,-3],[0,0,0,1]])
assert A*P==P*s.diag(0,1,2,3)
assert P.inv()==M([[1,1,1,1],[0,1,2,3],[0,0,1,3],[0,0,0,1]])
A=M([[2,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,2]])
P=M([[0,1,0,0],[1,0,1,0],[-1,0,1,0],[0,0,0,1]])
assert A*P==P*s.diag(0,2,2,2)
assert P.inv()==M([[0,s.Rational(1,2),-s.Rational(1,2),0],[1,0,0,0],[0,s.Rational(1,2),s.Rational(1,2),0],[0,0,0,1]])
cases=[(M([[0,2,1],[2,0,1],[1,1,1]]),M([[1,1,1],[-1,1,1],[0,-2,1]]),s.diag(-2,0,3),6),
       (M([[0,0,-2],[1,2,1],[1,0,3]]),M([[-2,0,-1],[1,1,0],[1,0,1]]),s.diag(1,2,2),-1),
       (M([[-s.I,0,2],[0,s.I,1],[0,0,-2*s.I]]),M([[1,0,6*s.I],[0,1,s.I],[0,0,3]]),s.diag(-s.I,s.I,-2*s.I),3)]
for A,P,D,det in cases:
    assert A*P==P*D and P.det()==det
alpha=s.symbols('alpha')
A=M([[0,0,1],[0,alpha,1],[1,0,0]])
P=M([[1-alpha,alpha+1,0],[1,1,1],[1-alpha,-alpha-1,0]])
assert s.simplify(A*P-P*s.diag(1,-1,alpha))==s.zeros(3)
assert s.expand(P.det()-2*(1-alpha**2))==0
assert (A.subs(alpha,1)-s.eye(3)).rank()==2
assert A.subs(alpha,0)**13==A.subs(alpha,0)
doc=pymupdf.open('output/pdf/parcial 1 Algebra.pdf')
import json
manifest=json.loads(Path('tmp/pdfs/course_manifest.json').read_text(encoding='utf-8'))
assert len(doc)==manifest['pages']
for A,P,D in [(M([[4,1-s.I],[1+s.I,5]]),M([[-1+s.I,1-s.I],[1,2]]),s.diag(3,6)),(M([[5,0,0],[0,-1,-1+s.I],[0,-1-s.I,0]]),M([[1,0,0],[0,1-s.I,-1+s.I],[0,1,2]]),s.diag(5,-2,1))]:
    assert s.simplify(A*P-P*D)==s.zeros(A.rows)
    assert P.det()!=0
B=M([[1,-s.I],[s.I,1]])
assert M([[-s.I,1],[0,0]])*B==s.zeros(2)
assert M([[0,0],[-s.I,1]])*B==s.zeros(2)
from reportlab.pdfbase.ttfonts import TTFont
cmap=TTFont('check','C:/Windows/Fonts/arial.ttf').face.charToGlyph
fmap=TTFont('fallback','C:/Windows/Fonts/seguisym.ttf').face.charToGlyph
content=Path('tmp/pdfs/course_content.txt').read_text(encoding='utf-8')
missing=[ord(c) for c in set(content) if ord(c)>127 and ord(c) not in cmap and ord(c) not in fmap]
assert not missing,missing
issues=[]
for i,p in enumerate(doc):
    for line in p.get_text('dict')['blocks']:
        if 'lines' not in line: continue
        for l in line['lines']:
            for sp in l['spans']:
                x0,y0,x1,y1=sp['bbox']
                if x0<35 or x1>560 or y0<30 or y1>825: issues.append((i+1,sp['text']))
    p.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(f'tmp/pdfs/final-{i+1}.png')
assert not issues,issues
from PIL import Image
ims=[]
for i in range(len(doc)):
    im=Image.open(f'tmp/pdfs/final-{i+1}.png').convert('RGB');im.thumbnail((358,506));ims.append(im)
for j in range(0,len(ims),8):
    contact=Image.new('RGB',(4*378,2*526),'#cbd5da')
    for k,im in enumerate(ims[j:j+8]): contact.paste(im,((k%4)*378+10,(k//4)*526+10))
    contact.save(f'tmp/pdfs/review-{j//8+1}.png')
Path('tmp/pdfs/course_qa.json').write_text(json.dumps({'pages':len(doc),'bounds_issues':issues,'missing_glyphs':missing,'toc_entries':len(doc.get_toc()),'status':'passed'},indent=2))
print('Verified symbolic changes of basis, diagonalizations, parameter cases, glyph coverage and',len(doc),'page layout bounds.')

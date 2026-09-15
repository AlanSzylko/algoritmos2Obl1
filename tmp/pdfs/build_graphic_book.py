from pathlib import Path
import json,re
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame,Paragraph,Preformatted,Spacer,Flowable
from reportlab.lib.styles import ParagraphStyle
from visual_algebra import *

ROOT=Path(__file__).resolve().parent
fonts()
manifest=json.loads((ROOT/'course_manifest.json').read_text(encoding='utf-8'))
content=(ROOT/'course_content.txt').read_text(encoding='utf-8').split('\n===\n')
starts={int(v[0]):int(k) for k,v in manifest['chapters'].items()}
entries=[];mapping={};newchap={}
for original in range(1,len(content)+1):
    if original in starts:
        ch=starts[original];newchap[ch]=[len(entries)+1,None]
        for title,fn in VISUALS[ch]:entries.append({'kind':'visual','title':title,'chapter':ch,'fn':fn})
    mapping[original]=len(entries)+1
    ch=next((int(k) for k,(a,b) in manifest['chapters'].items() if a<=original<=b),0)
    entries.append({'kind':'source','original':original,'title':manifest['sections'][original-1]['title'],'chapter':ch})
    if ch:newchap[ch][1]=len(entries)
total=len(entries)

def refs(s):
    s=re.sub(r'páginas (\d+)-(\d+)',lambda m:f"páginas {mapping[int(m[1])]}-{mapping[int(m[2])]}",s)
    s=re.sub(r'página (\d+)(?!\d)',lambda m:f"página {mapping[int(m[1])]}",s)
    return s
for i in [55,56]:content[i]=refs(content[i])
idx=content[1]
for ch,(a,b) in manifest['chapters'].items():
    idx=idx.replace(f'páginas {a}-{b}',f'páginas {newchap[int(ch)][0]}-{newchap[int(ch)][1]}')
idx=idx.replace('página 55',f'página {mapping[55]}').replace('páginas 56-58',f'páginas {mapping[56]}-{mapping[58]}')
idx=idx.replace('El panel de marcadores','Cada tema comienza con láminas visuales. El panel de marcadores')
content[1]=idx
content[0]=content[0].replace('Apunte completo para aprender los temas 1 a 7','Apunte visual completo | temas 1 a 7')
content[0]=content[0].replace('Cada capítulo contiene desarrollo teórico y aplicaciones.','Cada capítulo comienza con láminas visuales y contiene desarrollo teórico y aplicaciones.')

styles={
 'p':ParagraphStyle('p',fontName='Body',fontSize=10.4,leading=14.5,spaceAfter=7,textColor=color('ink')),
 'sub':ParagraphStyle('s',fontName='Bold',fontSize=11.1,leading=14.4,spaceBefore=8,spaceAfter=6,textColor=color('teal'),keepWithNext=True),
 'eq':ParagraphStyle('e',fontName='Body',fontSize=11,leading=15.8,spaceBefore=5,spaceAfter=13,borderPadding=8,backColor=color('paleBlue'),textColor=color('blue')),
 'matrix':ParagraphStyle('m',fontName='Mono',fontSize=10.3,leading=13.5,spaceBefore=5,spaceAfter=11,backColor=color('light'),borderPadding=7,textColor=color('ink')),
}
def story_for(text):
    blocks=text.strip().split('\n\n');story=[]
    for block in blocks[1:]:
        if block.startswith('## '):
            st='sub';txt=block[3:]
        elif block.startswith('= '):st='eq';txt=block[2:]
        elif block.startswith('MATRIX\n'):
            story.append(Preformatted(block[7:],styles['matrix']));continue
        else:st='p';txt=block
        html=markup(txt.replace('\n',' '))
        # Keep the wording intact while giving definitions and solution stages a visible lead-in.
        if st=='p' and txt.startswith('**'):
            html=html.replace('<b>','<b><font color="'+C['teal']+'">',1).replace('</b>','</font></b>',1)
        story.append(Paragraph(html,styles[st]))
    return story

def source(c,e):
    op=e['original'];ch=e['chapter'];title=e['title']
    rect(c,0,0,W,8,'teal',r=0)
    label=f'TEMA {ch}  /  DESARROLLO Y EJERCICIOS' if ch else 'PARCIAL 1 ALGEBRA  /  APUNTE VISUAL'
    p(c,38,28,519,label,8.7,'teal',True)
    fs=26 if op==1 else 19
    used=p(c,38,49,519,title,fs,'ink',True,leading=fs*1.13)
    top=59+used
    line(c,38,top,557,top,'line',.8)
    fr=Frame(38,55,519,H-top-69,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,showBoundary=0)
    story=story_for(content[op-1]);fr.addFromList(story,c)
    if story:raise RuntimeError(f'Overflow on original page {op}: {len(story)} blocks left')

def footer(c,n,e):
    line(c,38,804,557,804,'line',.8)
    p(c,38,814,438,'parcial 1 Algebra  |  '+('LÁMINA VISUAL' if e['kind']=='visual' else 'TEORÍA COMPLETA Y PRÁCTICA'),7.7,'muted')
    p(c,503,812,54,f'{n} / {total}',8.5,'muted')

OUT=ROOT/'graphic_draft.pdf'
c=Canvas(str(OUT),pagesize=(W,H));c.setTitle('parcial 1 Algebra - Apunte visual completo');c.setAuthor('Apunte de los temas 1 a 7')
toc=[]
for n,e in enumerate(entries,1):
    if e['kind']=='visual':e['fn'](c)
    else:source(c,e)
    footer(c,n,e);c.showPage()
    ismain=(n in {v[0] for v in newchap.values()}) or e['chapter']==0
    title=(f"{e['chapter']}. " if ismain and e['chapter'] else '')+e['title']
    toc.append([1 if ismain else 2,('Visual: ' if e['kind']=='visual' else '')+title,n])
c.save()
import pymupdf
doc=pymupdf.open(OUT);doc.set_toc(toc);doc.saveIncr();doc.close()
(ROOT/'graphic_manifest.json').write_text(json.dumps({'total':total,'original_mapping':mapping,'chapters':newchap,'pages':[{k:v for k,v in e.items() if k!='fn'} for e in entries]},ensure_ascii=False,indent=2),encoding='utf-8')
print('Generated',total,'pages, with',sum(e['kind']=='visual' for e in entries),'full visual lessons.')

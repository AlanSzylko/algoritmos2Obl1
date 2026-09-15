from pathlib import Path
import pymupdf,json,re
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
M=json.loads((R/'graphic_manifest.json').read_text(encoding='utf-8'))
doc=pymupdf.open(R/'graphic_draft.pdf')
out=R/'graphic_qa';out.mkdir(exist_ok=True)
issues=[];overlaps=[];figs=[];texts=[]
for i,page in enumerate(doc):
    typ=M['pages'][i]['kind']
    spans=[]
    for b in page.get_text('dict')['blocks']:
        if 'lines' not in b:continue
        for l in b['lines']:
            for s in l['spans']:
                x0,y0,x1,y1=s['bbox']
                if x0<20 or x1>577 or y0<14 or y1>838:issues.append((i+1,s['text'],s['bbox']))
                spans.append(s)
    if typ=='visual':
        for j,a in enumerate(spans):
            for b in spans[j+1:]:
                r=pymupdf.Rect(a['bbox'])&pymupdf.Rect(b['bbox'])
                if r.width>3 and r.height>3 and r.get_area()>25:overlaps.append((i+1,a['text'],b['text'],list(r)))
    pix=page.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25))
    pix.save(out/f'page-{i+1:02}.png')
    (figs if typ=='visual' else texts).append(i+1)
def sheets(nums,name,cols,rows,tw):
    th=int(tw*842/595)
    for start in range(0,len(nums),cols*rows):
        sheet=Image.new('RGB',(cols*(tw+18),rows*(th+40)),'#DFE7EB');draw=ImageDraw.Draw(sheet)
        for j,n in enumerate(nums[start:start+cols*rows]):
            im=Image.open(out/f'page-{n:02}.png').convert('RGB');im.thumbnail((tw,th));x=(j%cols)*(tw+18)+9;y=(j//cols)*(th+40)+25
            sheet.paste(im,(x,y));draw.text((x,y-17),f'PAGINA {n}',fill='black')
        sheet.save(out/f'{name}-{start//(cols*rows)+1}.png')
sheets(figs,'visual',2,2,480)
sheets(texts,'text',4,2,280)
report={'pages':len(doc),'visual_pages':figs,'out_of_bounds':issues,'possible_text_overlaps':overlaps}
(out/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))

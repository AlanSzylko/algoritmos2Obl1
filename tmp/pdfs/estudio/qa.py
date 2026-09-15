from pathlib import Path
from PIL import Image,ImageDraw
from pypdf import PdfReader
R=Path(__file__).resolve().parent
for offset in (0,16,32):
 files=sorted(R.glob('qa-*.png'))[offset:offset+16]
 sheet=Image.new('RGB',(1000,1440),'#dae3e9')
 for k,p in enumerate(files):
  im=Image.open(p);im.thumbnail((242,330))
  x=(k%4)*250;y=(k//4)*360
  sheet.paste(im,(x+4,y+22));ImageDraw.Draw(sheet).text((x+7,y+5),p.stem,fill='black')
 sheet.save(R/('qa_sheet_'+str(offset)+'.png'))
files=sorted(R.glob('*_crop.png'))
sheet=Image.new('RGB',(1500,1100),'#dae3e9')
for k,p in enumerate(files):
 im=Image.open(p);im.thumbnail((285,240));x=(k%5)*300;y=(k//5)*275
 sheet.paste(im,(x+5,y+25));ImageDraw.Draw(sheet).text((x+7,y+5),p.stem,fill='black')
sheet.save(R/'qa_crops.png')
r=PdfReader(R.parents[2]/'output/pdf/Resumen_completo_Ingenieria_de_Software_y_Git.pdf')
for i,p in enumerate(r.pages):
 t=p.extract_text()
 if len(t)<300:print('SHORT',i+1,len(t),t)
print('pages',len(r.pages),'images',sum(len(p.images) for p in r.pages))

from pathlib import Path
import subprocess
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parent
POP=r'C:/Users/alans/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
S=r'C:/Users/alans/ORT/Bases de datos/ingdelsoftwarelibro9_compressed.pdf'
G=r'C:/Users/alans/Downloads/pro-git-edicion-en-espanol.pdf'
PAGES={'s48':(S,48),'s51':(S,51),'s53':(S,53),'s56':(S,56),'s57':(S,57),'s63':(S,63),'s67':(S,67),'s69':(S,69),'g17':(G,17),'g19':(G,19),'g21':(G,21),'g31':(G,31),'g67':(G,67),'g74':(G,74),'g76':(G,76),'g77':(G,77),'g89':(G,89),'g96':(G,96)}
for name,(src,page) in PAGES.items():
 out=ROOT/name
 if not out.with_suffix('.png').exists():
  subprocess.run([POP,'-f',str(page),'-l',str(page),'-scale-to','1500','-singlefile','-png',src,str(out)],check=True,capture_output=True)
thumbs=[]
for name in PAGES:
 im=Image.open(ROOT/(name+'.png')).convert('RGB');im.thumbnail((240,330))
 cell=Image.new('RGB',(260,360),'#e8edf1');cell.paste(im,((260-im.width)//2,24));ImageDraw.Draw(cell).text((10,5),name,fill='black');thumbs.append(cell)
sheet=Image.new('RGB',(260*6,360*3),'white')
for i,im in enumerate(thumbs):sheet.paste(im,((i%6)*260,(i//6)*360))
sheet.save(ROOT/'sources_contact.png')

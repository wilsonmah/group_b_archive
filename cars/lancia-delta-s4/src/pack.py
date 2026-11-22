from pathlib import Path
from base64 import b64encode
r=Path(__file__).resolve().parent.parent
(r/'index.html').write_text((r/'src/view.html').read_text(encoding='utf-8-sig').replace('__LOCALE__',(r/'src/locale.js').read_text(encoding='utf8')).replace('__DATA__',b64encode((r/'models/Lancia_Delta_S4.glb').read_bytes()).decode()),encoding='utf-8')

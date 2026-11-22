# Lancia Delta S4 (1986) · Martini Racing Nº 1. Procedural GLB generator.
from pathlib import Path
SRC=Path(__file__).resolve().parent
def run(name):exec(compile((SRC/name).read_text(encoding='utf-8'),name,'exec'),globals())
run('core.py')
drive_extras={}
for module in ['body.py','lamps.py','chassis.py','mech.py','livery.py']:
    if (SRC/module).exists():run(module)
# Drop parts that ended up with no geometry so every mesh has primitives.
for k in [k for k,v in parts.items() if not v]:del parts[k]
blob=bytearray();views=[];accessors=[]
def bv(data,target=None):
    while len(blob)%4:blob.append(0)
    d=dict(buffer=0,byteOffset=len(blob),byteLength=len(data))
    if target:d['target']=target
    views.append(d);blob.extend(data);return len(views)-1
def acc(data,kind,typ,target=None,bounds=False):
    dim={'SCALAR':1,'VEC3':3,'VEC2':2}[kind];d=dict(bufferView=bv(data.tobytes(),target),componentType=typ,count=len(data)//dim,type=kind)
    if bounds:
        d['min']=[min(data[i::dim]) for i in range(dim)];d['max']=[max(data[i::dim]) for i in range(dim)]
    accessors.append(d);return len(accessors)-1
nodes=[];roots=[];meshes=[];channels=[];samplers=[]
time=acc(array.array('f',[0,3]),'SCALAR',5126,bounds=True)
internal_clips={}
for key,info in groups.items():
    info['key']=key
    idx=len(nodes);roots.append(idx)
    node=dict(name=info['zh']+' | '+info['en'],children=[],extras=info);nodes.append(node)
    if any(info['vec']):
        samplers.append(dict(input=time,output=acc(array.array('f',[0,0,0,*info['vec']]),'VEC3',5126),interpolation='LINEAR'))
        channels.append(dict(sampler=len(samplers)-1,target=dict(node=idx,path='translation')))
    for (g,n),v in parts.items():
        if g!=key:continue
        prims=[];meta=component_meta.get((g,n));pivot=(0,0,0)
        if meta:
            pivot=tuple((min(min(data[0][i::3]) for data in v.values())+max(max(data[0][i::3]) for data in v.values()))/2 for i in range(3))
        for m,(pos,nor,tex,ind) in v.items():
            P=array.array('f');N=array.array('f');T=array.array('f');ids={};mapping=[]
            for j in range(len(pos)//3):
                p=pos[j*3:j*3+3];normal=nor[j*3:j*3+3];t=tex[j*2:j*2+2];k=p.tobytes()+normal.tobytes()+t.tobytes()
                if k not in ids:
                    ids[k]=len(P)//3;P.extend(sub(p,pivot) if meta else p);N.extend(normal);T.extend(t)
                mapping.append(ids[k])
            indices=array.array('H' if len(mapping) and max(mapping)<65536 else 'I',(mapping[i] for i in ind))
            attr=dict(POSITION=acc(P,'VEC3',5126,34962,True),NORMAL=acc(N,'VEC3',5126,34962))
            if T:attr['TEXCOORD_0']=acc(T,'VEC2',5126,34962)
            prims.append(dict(attributes=attr,indices=acc(indices,'SCALAR',5123 if indices.typecode=='H' else 5125,34963),material=mids[m]))
        child=dict(name=n,mesh=len(meshes));childID=len(nodes)
        if (key,n) in drive_extras:child['extras']=drive_extras[(key,n)]
        if meta:
            meta.update(child.get('extras', {}))
            child.update(name=meta['zh']+' | '+n,translation=pivot,extras=meta)
            clip=internal_clips.setdefault(key,dict(name=info['en']+' - components',samplers=[],channels=[]))
            clip['channels'].append(dict(sampler=len(clip['samplers']),target=dict(node=childID,path='translation')))
            clip['samplers'].append(dict(input=time,output=acc(array.array('f',[*pivot,*add(pivot,meta['vec'])]),'VEC3',5126),interpolation='LINEAR'))
        node['children'].append(childID);nodes.append(child);meshes.append(dict(name=n,primitives=prims))
imageview=bv((ROOT/'src/decals.png').read_bytes())
gltf=dict(asset=dict(version='2.0',generator='Procedural Lancia Delta S4 study'),scene=0,scenes=[dict(name='Lancia Delta S4',nodes=roots)],nodes=nodes,meshes=meshes,materials=materials,accessors=accessors,bufferViews=views,buffers=[dict(byteLength=len(blob))],images=[dict(name='Rally markings',bufferView=imageview,mimeType='image/png')],textures=[dict(source=0,sampler=0)],samplers=[dict(magFilter=9729,minFilter=9987,wrapS=33071,wrapT=33071)],animations=[dict(name='Exploded view',channels=channels,samplers=samplers)])
gltf['animations'].extend(internal_clips.values())
j=json.dumps(gltf,separators=(',',':'),ensure_ascii=False).encode();j+=b' '*((-len(j))%4)
blob.extend(b'\0'*((-len(blob))%4))
glb=struct.pack('<4sII',b'glTF',2,28+len(j)+len(blob))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(blob),b'BIN\0')+blob
(OUT/'Lancia_Delta_S4.glb').write_bytes(glb)
print(len(groups),'assemblies,',len(meshes),'parts,',sum(accessors[p['indices']]['count']//3 for mesh in meshes for p in mesh['primitives']),'triangles,',len(glb),'bytes')



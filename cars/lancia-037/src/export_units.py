import json,struct,copy
from pathlib import Path
root=Path(__file__).resolve().parent.parent/'models'
def read(path):
    raw=path.read_bytes();jl=struct.unpack_from('<I',raw,12)[0]
    return json.loads(raw[20:20+jl]),raw[28+jl:]
def write(path,g,bin):
    j=json.dumps(g,ensure_ascii=False,separators=(',',':')).encode();j+=b' '*((-len(j))%4);bin+=b'\0'*((-len(bin))%4)
    path.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(j)+len(bin))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(bin),b'BIN\0')+bin)
g,raw=read(root/'Lancia_037.glb')
for key,filename in [('engine','Lancia_037_Engine.glb'),('gearbox','Lancia_037_Transaxle.glb'),('susp','Lancia_037_Suspension.glb')]:
    idx=next(i for i in g['scenes'][0]['nodes'] if g['nodes'][i]['extras']['key']==key)
    source=g['nodes'][idx]
    h={'asset':g['asset'],'scene':0,'scenes':[{'nodes':[0],'name':source['extras']['zh']}],
       'nodes':[{'name':source['name'],'children':[],'extras':source['extras']}],'meshes':[],'materials':[],'animations':[],
       'accessors':[],'bufferViews':[],'buffers':[]}
    blob=bytearray();mapA={};mapMat={};mapNode={}
    def moveacc(i):
        if i in mapA:return mapA[i]
        a=copy.deepcopy(g['accessors'][i]);v=copy.deepcopy(g['bufferViews'][a['bufferView']])
        blob.extend(b'\0'*((-len(blob))%4));off=v['byteOffset']
        v['byteOffset']=len(blob);blob.extend(raw[off:off+v['byteLength']]);a['bufferView']=len(h['bufferViews'])
        h['bufferViews'].append(v);mapA[i]=len(h['accessors']);h['accessors'].append(a);return mapA[i]
    mins=[float('inf')]*3;maxs=[-float('inf')]*3
    for old in source['children']:
        node=copy.deepcopy(g['nodes'][old]);mesh=copy.deepcopy(g['meshes'][node['mesh']])
        for prim in mesh['primitives']:
            mi=prim['material']
            if mi not in mapMat:
                mat=copy.deepcopy(g['materials'][mi]);assert 'baseColorTexture' not in mat['pbrMetallicRoughness']
                mapMat[mi]=len(h['materials']);h['materials'].append(mat)
            pos=g['accessors'][prim['attributes']['POSITION']]
            for k in range(3):
                mins[k]=min(mins[k],pos['min'][k]+node['translation'][k]);maxs[k]=max(maxs[k],pos['max'][k]+node['translation'][k])
            prim['material']=mapMat[mi];prim['attributes']={n:moveacc(a) for n,a in prim['attributes'].items()};prim['indices']=moveacc(prim['indices'])
        mapNode[old]=len(h['nodes']);h['nodes'][0]['children'].append(mapNode[old]);node['mesh']=len(h['meshes']);h['meshes'].append(mesh);h['nodes'].append(node)
    h['nodes'][0]['translation']=[-(mins[0]+maxs[0])/2,-mins[1],-(mins[2]+maxs[2])/2]
    animation=copy.deepcopy(next(a for a in g['animations'] if all(c['target']['node'] in mapNode for c in a['channels'])))
    for sam in animation['samplers']:
        sam['input']=moveacc(sam['input']);sam['output']=moveacc(sam['output'])
    for chan in animation['channels']:chan['target']['node']=mapNode[chan['target']['node']]
    h['animations'].append(animation);h['buffers']=[{'byteLength':len(blob)}]
    write(root/filename,h,blob)
    test,chunk=read(root/filename)
    assert len(test['meshes'])==len(source['children'])==len(test['animations'][0]['channels'])
    for i,node in enumerate(test['nodes'][1:],1):
        sampler=next(animation['samplers'][c['sampler']] for c in animation['channels'] if c['target']['node']==i)
        a=test['accessors'][sampler['output']];v=test['bufferViews'][a['bufferView']];first=struct.unpack_from('<6f',chunk,v['byteOffset'])
        assert all(abs(first[k]-node['translation'][k])<1e-6 and abs(first[k+3]-first[k]-node['extras']['vec'][k])<1e-6 for k in range(3))
    print(filename,len(h['meshes']),'components checked')

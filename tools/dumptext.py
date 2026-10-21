import struct,sys
from resdump import read_dir
def items(d,e):
    rid,size,fl,cs,typ,pos=e; blob=d[pos:pos+size]
    if not fl&2: return [blob]
    n=struct.unpack_from('<H',blob,0)[0]
    offs=struct.unpack_from('<%dI'%(n+1),blob,2)
    return [blob[offs[i]:offs[i+1]] for i in range(n)]
if __name__=='__main__':
    d,ents=read_dir(sys.argv[1]); want=[int(x) for x in sys.argv[2:]]
    for e in ents:
        if e[0] in want or (not want and e[4]==1):
            for i,it in enumerate(items(d,e)):
                print(e[0],i,repr(it[:300].decode('latin1')))

import struct,sys
def read_dir(path):
    d=open(path,'rb').read()
    off=struct.unpack_from('<I',d,0x7C)[0]
    n,dataoff=struct.unpack_from('<HI',d,off)
    p=off+6; pos=dataoff; out=[]
    for i in range(n):
        rid,a,b=struct.unpack_from('<HII',d,p); p+=10
        size=a&0xFFFFFF; flags=a>>24; csize=b&0xFFFFFF; typ=b>>24
        out.append((rid,size,flags,csize,typ,pos)); pos+=(csize+3)&~3
    return d,out
if __name__=='__main__':
    d,ents=read_dir(sys.argv[1])
    print(d[:0x40].split(b'\0')[0])
    for e in ents: print('id %5d size %7d fl %02x csize %7d type %2d off %x'%e[:6], d[e[5]:e[5]+24])

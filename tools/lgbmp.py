"""Looking Glass bitmap decoding (FrameDesc: 28-byte header, then pixels; optional palette)."""
import struct
def rsd(b,p,n):
    out=bytearray()
    while len(out)<n and p<len(b):
        op=b[p]; p+=1
        if op==0: c,v=b[p],b[p+1]; p+=2; out+=bytes([v])*c
        elif op<128: out+=b[p:p+op]; p+=op
        elif op>128: out+=bytes(op-128)
        else:
            c=struct.unpack_from('<H',b,p)[0]; p+=2
            if c==0: break
            if c<0x8000: out+=bytes(c)
            elif c<0xc000: c&=0x3fff; out+=b[p:p+c]; p+=c
            else: c&=0x3fff; out+=bytes([b[p]])*c; p+=1
    return bytes(out[:n]).ljust(n,b'\0')
def decode(b, whole=None):
    """b = frame bytes; whole = the whole compound resource (palette offsets are relative to it)."""
    typ,align,flags,w,h,row=struct.unpack_from('<BBHHHH',b,4)
    pal_off=struct.unpack_from('<I',b,24)[0]
    if typ==4: px=rsd(b,28,w*h)
    else: px=b''.join(b[28+y*row:28+y*row+w] for y in range(h))
    pal=None
    if pal_off:
        wh=whole if whole is not None else b'\0'*10+b  # palette block: u16 first index, u16 count, RGB bytes
        start,cnt=struct.unpack_from("<HH",wh,pal_off)
        rgb=wh[pal_off+4:pal_off+4+cnt*3]
        if len(rgb)==cnt*3: pal=(start,rgb)
    return dict(type=typ,w=w,h=h,flags=flags,px=px,pal=pal)

import numpy as np, wave
sr=44100; T=120; n=sr*T; t=np.arange(n)/sr; rng=np.random.RandomState(1)
out=np.zeros(n)
chords=[(220,261.6,329.6),(174.6,220,261.6),(261.6,329.6,392),(196,246.9,293.7)]
for k in range(T//6):
    f=chords[k%4]; seg=np.zeros(sr*6); tt=np.arange(sr*6)/sr
    for fr in f: seg+=np.sin(2*np.pi*fr*tt)+0.4*np.sin(2*np.pi*fr*2.003*tt)
    env=np.minimum(1,tt/1.5)*np.minimum(1,(6-tt)/1.5); seg*=env
    out[k*sr*6:(k+1)*sr*6]+=seg*0.05
def vol(a,b,c,d): return np.interp(t,[a,b,c,d],[0.4,0.6,1.0,1.0]) 
out*=np.interp(t,[0,36,100,114,120],[0.5,0.7,1.1,1.2,0.4])
# ticks 6-36
for s in range(6,36):
    i=s*sr; k=int(0.03*sr); out[i:i+k]+=np.sin(2*np.pi*1800*np.arange(k)/sr)*np.exp(-np.arange(k)/(0.004*sr))*0.08
# pulse from 36 to 112
for b in np.arange(36,112,0.5):
    i=int(b*sr); k=int(0.25*sr); tt=np.arange(k)/sr; out[i:i+k]+=np.sin(2*np.pi*(55+40*np.exp(-tt*30))*tt)*np.exp(-tt*12)*(0.25 if b>66 else 0.15)
# whoosh at 0 and 114 hit, chime at 78/84, chalk 60-64
def noise(a,b,amp):
    i,j=int(a*sr),int(b*sr); x=rng.randn(j-i); x=np.convolve(x,np.ones(30)/30,'same'); out[i:j]+=x*np.hanning(j-i)*amp
noise(0,2,0.25); noise(60.5,64,0.05); noise(108,114,0.25)
for c in (78.2,84.3,90.5,102):
    i=int(c*sr); tt=np.arange(int(2.5*sr))/sr; out[i:i+len(tt)]+=(np.sin(2*np.pi*1318*tt)+0.5*np.sin(2*np.pi*1975*tt))*np.exp(-tt*2.5)*0.12
i=114*sr; tt=np.arange(6*sr)/sr; out[i:]+=sum(np.sin(2*np.pi*f*tt) for f in(220,330,440,660))*np.exp(-tt*.7)*0.07
out/=np.max(np.abs(out))*1.15
w=wave.open('score.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()

import json, numpy as np
from chain import ground_corr, entropy
from ball3d import radial_V
XI=1/6
def pieces(n, c, wf, X0, P0, N, lam=1e-3):
    j=np.arange(1,N+1.); R=n+0.5
    beta=np.pi*(R*R-j**2)/R
    u=np.exp(-((j-c*R)**2)/(2*(wf*R)**2)); u/=np.linalg.norm(u); uu=np.outer(u,u)
    v={}
    for s in (1,-1):
        A=np.eye(N)+(np.exp(s*lam)-1)*uu; B=np.eye(N)+(np.exp(-s*lam)-1)*uu
        X=A@X0@A.T; P=B@P0@B.T
        d=np.diag(X); off=np.diag(X,1); jj,jn=j[:-1],j[1:]
        link=0.5*(jj+0.5)**2*(d[:-1]/jj**2+d[1:]/jn**2-2*off/(jj*jn))
        Kc=np.sum(beta[:n]*0.5*np.diag(P)[:n])+np.sum(np.pi*(R*R-(j[:n-1]+0.5)**2)/R*link[:n-1])
        v[s]=(entropy(X[:n,:n],P[:n,:n]),Kc,d/(4*np.pi*j**2))
    dS=(v[1][0]-v[-1][0])/2; dKc=(v[1][1]-v[-1][1])/2; f=(v[1][2]-v[-1][2])/2
    lap=np.zeros(N)
    for k in range(N):
        fp=f[k+1] if k+1<N else 0.; fm=f[k-1] if k>0 else f[k]
        lap[k]=((j[k]+0.5)**2*(fp-f[k])-(j[k]-0.5)**2*(f[k]-fm))/j[k]**2
    vol=4*np.pi*j**2
    L=np.sum(beta[:n]*lap[:n]*vol[:n])            # int_ball beta Lap f
    I1=np.sum(f[:n]*vol[:n])                      # int_ball f
    I2=0.5*(f[n-1]+f[n])*4*np.pi*R*R              # surface integral of f at R
    return dict(n=n,c=c,wf=wf,dS=dS,dKc=dKc,L=L,I1=I1,I2=I2)
rows=[]
for n in (16,32,64):
    N=8*n; X0,P0=ground_corr(radial_V(N,0,0.0))
    for c in (0.7,0.8,0.9,1.0,1.1,1.2):
        for wf in (0.1,0.15,0.25):
            rows.append(pieces(n,c,wf,X0,P0,N))
json.dump(rows,open('results/ball3d_fit.json','w'),indent=1)
r=np.array([[q['dS']-q['dKc'],q['L'],q['I1'],q['I2']] for q in rows])
y=r[:,0]
for name,cols in (('xi*L (sign free)',[1]),('I1,I2',[2,3]),('L,I1,I2',[1,2,3])):
    A=r[:,cols]; coef,res,_,_=np.linalg.lstsq(A,y,rcond=None)
    pred=A@coef; rel=np.max(np.abs(pred-y))/np.max(np.abs(y))
    print(name,'coef',np.round(coef,5),'max rel resid',round(rel,4))
print('2*pi*xi =',2*np.pi*XI,' xi=',XI)
# ratios with candidate K's
for q in rows:
    q['r_can']=q['dS']/q['dKc']; q['r_minus']=q['dS']/(q['dKc']-XI*q['L']); q['r_plus']=q['dS']/(q['dKc']+XI*q['L'])
import statistics
for k in ('r_can','r_minus','r_plus'):
    vals=[q[k] for q in rows if abs(q['dS'])>1e-5]
    print(k,'median',round(statistics.median(vals),4),'min',round(min(vals),4),'max',round(max(vals),4),'count',len(vals))
# Ratio with the theoretical coefficients (no fitting): improved energy density
# plus the Wald surface term,  dS - 2*pi*xi*I2  vs  dKc - xi*L.
print('--- corrected ratio (dS - 2*pi*xi*I2) / (dKc - xi*L), by ball radius ---')
summary = {}
for n in (16, 32, 64):
    sel = [q for q in rows if q['n'] == n and abs(q['dKc'] - XI*q['L']) > 1e-6]
    rw = [(q['dS'] - 2*np.pi*XI*q['I2'])/(q['dKc'] - XI*q['L']) for q in sel]
    rc = [q['dS']/q['dKc'] for q in sel]
    summary[f'R={n+0.5}'] = {'corrected_median': statistics.median(rw), 'corrected_min': min(rw), 'corrected_max': max(rw),
                             'plain_median': statistics.median(rc), 'plain_min': min(rc), 'plain_max': max(rc)}
    print('R=%.1f corrected median %.4f (%.4f to %.4f) | plain median %.3f (%.2f to %.2f)' % (
        n+0.5, statistics.median(rw), min(rw), max(rw), statistics.median(rc), min(rc), max(rc)))
json.dump(summary, open('results/ball3d_fit_summary.json', 'w'), indent=1)

m = torch.from_numpy(m0)
d = torch.from_numpy(d0)
o = torch.from_numpy(o0)
if dostdp:
    w = torch.from_numpy(w0)
wfast = torch.from_numpy(w0)
s = torch.from_numpy(s0)
u = torch.from_numpy(u0)
rtarg = torch.from_numpy(rtarg0)
sbar = torch.from_numpy(sbar0)
dastdpbar = torch.from_numpy(dastdpbar0)
baselineinds = (np.sum(s0,1,keepdims=True) == 0) & (np.sum(u0,1,keepdims=True) == 0)
baselineinds_d = torch.from_numpy(np.repeat(baselineinds,D,axis=1).astype(np.float32))

ma = np.zeros([T,M,B])
da = np.zeros([T,D,B])
oa = np.zeros([T,O,B])
if dostdp:
    wa = np.zeros([T,M,S,B])

r = torch.zeros(T,R,B)
dacost = torch.zeros(1)

for ti in range(T):
    if ti in resettimes:
        mnew = torch.from_numpy(m0)
        dnew = torch.from_numpy(d0)
        onew = torch.from_numpy(o0)
        sbar = torch.from_numpy(sbar0)
        dastdpbar = torch.from_numpy(dastdpbar0)
    else:
        if dostdp:
            mnew = (1-dt)*m + dt*torch.relu(torch.tanh(Jmm.mm(m) + Jmo.mm(o) + torch.einsum('ijb,jb->ib',(w,s[ti,:,:])) + bm))
        else:
            mnew = (1-dt)*m + dt*torch.relu(torch.tanh(Jmm.mm(m) + Jmo.mm(o) + w.mm(s[ti,:,:]) + bm))
        dnew = (1-dt)*d + dt*torch.relu(torch.tanh(Jdm.mm(m) + Jdd.mm(d) + Jdo.mm(o) + bd))
        onew = (1-dt)*o + dt*torch.relu(torch.tanh(Jom.mm(m) + Jod.mm(d) + Joo.mm(o) + wou.mm(u[ti,:]) + bo))
    m = mnew
    d = dnew
    o = onew
    ma[ti,:,:] = m.detach()
    da[ti,:,:] = d.detach()
    oa[ti,:,:] = o.detach()
    if dostdp:
        wa[ti,:,:,:] = w.detach()

    r[ti,:,:] = wrm.mm(m)


    if dostdp:
        dastdp = torch.relu(Jmd.mm(d))
        stdp_update = stdpfac * (-torch.einsum('ib,jb->ijb',(dastdp,sbar)) + torch.einsum('ib,jb->ijb',(dastdpbar,s[ti,:,:]))) #anti-Hebbian
        wfast = torch.relu(w + dt*(stdp_update - torch.relu(stdp_update - (wmax - w)))) #update that does not exceed wmax
        w = w + (dt/tauw)*(wfast - w)

        dastdpbar = (1. - dt/tau)*dastdpbar + (dt/tau)*dastdp
        sbar = (1. - dt/tau)*sbar + (dt/tau)*s[ti,:,:]
        dacost += torch.sum(torch.pow(torch.relu(d*baselineinds_d[ti,:,:]-dinit),2))

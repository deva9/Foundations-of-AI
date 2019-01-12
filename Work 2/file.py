import signal
import time
def myinput(fr):
    global clen, splen
    alreadyL, alreadyS, newApplicants, common, spla, lahsa, splaUn, lahsaUn = ([] for i in range(8))         # lists part 1
    indices = [0, 5, 6, 9, 10, 11, 12, 13, 20]
    parts = []
    nbeds = int(fr.readline())
    npark = int(fr.readline())
    beds = [nbeds]*7
    park = [npark]*7
    nL = int(fr.readline())
    for _ in range(nL):
        alreadyL.append(fr.readline().strip())
    nS = int(fr.readline())
    for _ in range(nS):
        alreadyS.append(fr.readline().strip())
    nA = int(fr.readline())
    for _ in range(nA):
        line = fr.readline().strip()
        x = line[0:5]
        if x in alreadyL:
            for j in range(7):
                    beds[j] -= (int(line[13+j]))
        elif x in alreadyS:
            for j in range(7):
                    park[j] -= (int(line[13+j]))
        else:
            newApplicants.append(line)
            if line[10] == 'N' and line[11] == 'Y' and line[12] == 'Y':
                spla.append([x, line[13:]])
                splaUn.append([x, line[13:]])
            if line[5] == 'F' and int(line[6:9]) >= 18 and line[9] == 'N':
                lahsa.append([x, line[13:]])
                lahsaUn.append([x, line[13:]])
            parts.append([line[indices[i]:indices[i+1]] for i in xrange(len(indices)-1)])

    for x in spla[:]:
        if x in lahsa:
            common.append(x)
            spla.remove(x)
            lahsa.remove(x)
    return nbeds, npark, parts, beds, park, common, spla, lahsa, splaUn, lahsaUn


def countones(str):
    return str.count('1')


def terminalstate(common):
    if not common:
        return True
    return False


def evaluateScore(beds, park, spla, lahsa, nbeds, npark, agent, splaUn, lahsaUn):
    global effspla, efflahsa
    effspla, efflahsa = 0, 0
    if agent == 0:
        copysp = spla[:]
        copyla = lahsa[:]
    else:
        copysp = splaUn[:]
        copyla = lahsaUn[:]
    if agent != 2:
        z = []
        if len(copysp) != 0:
            for x, y in copysp:
                c = []
                for j in range(7):
                    c.append(park[j]-int(y[j]))
                if -1 not in c:
                    park = c
                    z.append([x, y])
        for i in park:
            effspla += (npark - i)
        if agent != 0:
            for i in beds:
                efflahsa += (nbeds - i)

        if len(z) != 0:
            for x, y in z:
                for j in range(7):
                    park[j] += int(y[j])

    if agent != 1:
        p = []
        if len(copyla) != 0:
            for x, y in copyla:
                c = []
                for j in range(7):
                    c.append(beds[j]-int(y[j]))
                if -1 not in c:
                    beds = c
                    p.append([x, y])
        for i in beds:
            efflahsa += (nbeds - i)
        if agent != 0:
            for i in park:
                effspla += (npark - i)
        if len(p) != 0:
            for x, y in p:
                for j in range(7):
                    beds[j] += int(y[j])

    return effspla, efflahsa


def maxSpla(common, beds, park, nbeds, npark, lahsa, spla, currentDepth):
    if terminalstate(common):
        # print "Calling from empty SPLA", currentDepth
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 0, splaUn, lahsaUn)
    global t
    vs = -float('inf')
    vl = -float('inf')
    vsprev = vs
    vlprev = vl
    for i in common[:]:
        q = i   # storing popped value
        c = []
        for j in range(7):
            c.append(park[j]-int(q[1][j]))
        if -1 not in c:
            park = c
        else:
            continue
        common.pop(common.index(i))
        # print park, "SPLA removes ", q
        s, l = maxLahsa(common, beds, park, nbeds, npark, lahsa, spla, currentDepth+1)
        if s > vs:
            vl = l
            vs = s
        common.append(q)    # adding popped value
        if len(common) == clen:
            t.append([common[-1][0], common[-1][1], s, l])
        for j in range(7):
            park[j] += int(q[1][j])
    if vs == vsprev and vl == vlprev:
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 0, splaUn, lahsaUn)
    # print park, "SPLA adds ", q
    # print vs, vl, "<- SPLA", currentDepth
    return vs, vl


def maxLahsa(common, beds, park, nbeds, npark, lahsa, spla, currentDepth):
    if terminalstate(common):
        # print "Calling from empty LAHSA", currentDepth
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 0, splaUn, lahsaUn)
    vs = -float('inf')
    vl = -float('inf')
    vsprev = vs
    vlprev = vl
    for i in common[:]:
        q = i     # storing popped value
        # print q, common, "FROM LA"
        c = []
        for j in range(7):
            c.append(beds[j]-int(q[1][j]))
        if -1 not in c:
            beds = c
        else:
            continue
        common.pop(common.index(i))
        # print beds, "LAHSA removes ", q
        s, l = maxSpla(common, beds, park, nbeds, npark, lahsa, spla, currentDepth+1)
        if l > vl:
            vs = s
            vl = l
        common.append(q)
        for j in range(7):
            beds[j] += int(q[1][j])
        # print beds, "LAHSA  adds ", q
    if vs == vsprev and vl == vlprev:
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 0, splaUn, lahsaUn)
    # print vs, vl, "<- LAHSA", currentDepth
    return vs, vl


def maxSplaNew(beds, park, nbeds, npark, lahsaUn, splaUn, currentDepth):
    global tdash
    vs = -float('inf')
    vl = -float('inf')
    vsprev = vs
    vlprev = vl
    if terminalstate(lahsaUn):
        # print "Calling from empty SPLA", currentDepth
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 1, splaUn, lahsaUn)
    if not splaUn:
        s, l = maxLahsaNew(beds, park, nbeds, npark, lahsaUn, splaUn, currentDepth)
        if s > vs:
            vs = s
            vl = l
    for i in splaUn[:]:
        q = i   # storing popped value
        c = []
        ctr = 0
        if q in lahsaUn:
            ctr = 1
        for j in range(7):
            c.append(park[j]-int(q[1][j]))
        if -1 not in c:
            park = c
        else:
            continue
        if ctr == 0:
            splaUn.pop(splaUn.index(i))
        else:
            lahsaUn.pop(lahsaUn.index(i))
            splaUn.pop(splaUn.index(i))
        # print park, "SPLA removes ", q
        s, l = maxLahsaNew(beds, park, nbeds, npark, lahsaUn, splaUn, currentDepth+1)
        if s > vs:
            vl = l
            vs = s
        # splaUn.append(q)    # adding popped value
        if ctr == 1:
            lahsaUn.append(q)
            splaUn.append(q)
        else:
            splaUn.append(q)
        if len(splaUn) == splen:
            tdash.append([splaUn[-1][0], splaUn[-1][1], s, l])
        ctr = 0
        for j in range(7):
            park[j] += int(q[1][j])
    if vs == vsprev and vl == vlprev:
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 2, splaUn, lahsaUn)
    # print park, "SPLA adds ", q
    # print vs, vl, "<- SPLA", currentDepth
    return vs, vl


def maxLahsaNew(beds, park, nbeds, npark, lahsaUn, splaUn, currentDepth):
    vs = -float('inf')
    vl = -float('inf')
    vsprev = vs
    vlprev = vl
    if terminalstate(splaUn):
        # print "Calling from empty SPLA", currentDepth
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 2, splaUn, lahsaUn)
    if not splaUn:
        s, l = maxLahsaNew(beds, park, nbeds, npark, lahsaUn, splaUn, currentDepth)
        if l > vl:
            vs = s
            vl = l
    for i in lahsaUn[:]:
        q = i   # storing popped value
        c = []
        ctr = 0
        if q in splaUn:
            ctr = 1
        for j in range(7):
            c.append(beds[j]-int(q[1][j]))
        if -1 not in c:
            beds = c
        else:
            continue
        if ctr == 0:
            lahsaUn.pop(lahsaUn.index(i))
        else:
            splaUn.pop(splaUn.index(i))
            lahsaUn.pop(lahsaUn.index(i))
        # print beds, "LAHSA removes ", q
        s, l = maxSplaNew(beds, park, nbeds, npark, lahsaUn, splaUn, currentDepth+1)
        if l > vl:
            vl = l
            vs = s
        if ctr == 1:
            lahsaUn.append(q)
            splaUn.append(q)
        else:
            lahsaUn.append(q)
        ctr = 0
        for j in range(7):
            beds[j] += int(q[1][j])
    if vs == vsprev and vl == vlprev:
        return evaluateScore(beds, park, spla, lahsa, nbeds, npark, 1, splaUn, lahsaUn)
    # print beds, "LAHSA adds ", q
    # print vs, vl, "<- LAHSA", currentDepth
    return vs, vl


def handler2(signum, frame):
    global fw
    fw.write(str(output))
    fw.close()
    exit()


def calculate(ans, sp, la):
    ans.sort(key=lambda y: countones(y[1]), reverse=True)
    for x in ans:
        if sp == x[2] and la == x[3]:
            return x[0]


global output
global start_time
start_time = time.time()
# signal.signal(signal.SIGALRM, handler2)
# signal.alarm(175)
fr = open('input0.txt', 'r')
fw = open('output.txt', 'w')
t, tdash = [], []
nbeds, npark, parts, beds, park, common, spla, lahsa, splaUn, lahsaUn = myinput(fr)
clen, splen = len(common), len(splaUn)
spla.sort(key=lambda x: countones(x[1]), reverse=True)
lahsa.sort(key=lambda x: countones(x[1]), reverse=True)
splaUn.sort(key=lambda x: countones(x[1]), reverse=True)
lahsaUn.sort(key=lambda x: countones(x[1]), reverse=True)
# print spla, lahsa, common
for i in spla:
    check = []
    for j in range(7):
        check.append(park[j] - int(i[1][j]))
    if -1 in check:
        continue
    output = str(i[0])
    break
# print output
if not spla and common:
    for i in common:
        check = []
        for j in range(7):
            check.append(park[j] - int(i[1][j]))
        if -1 in check:
            continue
        output = str(i[0])
        break
starttime = time.time()
print output
print common
if len(common) > 0:
    print "Going"
    common.sort(key=lambda x: countones(x[1]), reverse=True)
    sp, la = maxSpla(common, beds, park, nbeds, npark, lahsa, spla, 0)
    # print t
    if t:
        output = str(calculate(t, sp, la))
    print sp, la, output, "<--COMMON ONLY"
# print output, sp, la
length = len(common) + len(spla) + len(lahsa)
if length >= nbeds or length > npark or not t:
    sp, la = maxSplaNew(beds, park, nbeds, npark, lahsaUn, splaUn, 0)    
    print sp, la, calculate(tdash, sp, la), "<--BOTHH"
    output = str(calculate(tdash, sp, la))
print output
fw.write(output)
print time.time()-starttime

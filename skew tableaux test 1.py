import threading
import time
def clean_t(l):
    global skew_t
    skew_t[l] = []
    skew_t[l].append([0 for i in range(lam[0])])
    for i in range(len(lam)):
        if i >= len(mu):
            skew_t[l].append([0 for i in range(lam[i])])
        else:
            skew_t[l].append([-1 for i in range(mu[i])] + [0 for i in range(mu[i], lam[i])])
    return skew_t

def origin_t(): #找skew ableaux的接點
    global origin
    origin = (len(mu), mu[len(mu) - 1] + 1)
    return origin

def pos_t():
    global  pos, origin
    for i in range(len(skew_t)):
        for j in range(len(skew_t[i])):
            if skew_t[i][j] == 0:
                pos.append((i + 1, j + 1))
    return pos

def check(l):
    global pos, skew_t, stat
    clean_t(l)
    pos_t()
    for i in range(len(pos)):
        x = pos[i][0]
        y = pos[i][1]
        skew_t[l][x][y] = stat[l][i]
        if skew_t[l][x][y] < skew_t[l][x-1][y] or skew_t[l][x][y] < skew_t[l][x][y-1]:
            return 0

    return 1

def DFS(num, m):
    global n, stat, count, canperm, total

    if num == n - 2:
        slot = stat[m].index(0)
        stat[m][slot] = canperm[m][num]
        plus = check(m)
        total += plus
        for i in range(n):
            print(skew_t[m][origin[0]][origin[1]])
            count[skew_t[m][origin[0]][origin[1]]-1] += plus
        stat[m][slot] = 0
        return
    else:
        #print(num, m)
        for i in range(stat[m].index(0), n):
            if stat[m][i] == 0:
                stat[m][i] = canperm[m][num]
                DFS(num + 1, m)
                stat[m][i] = 0


def job(k):
    global count
    DFS(0, k)
    done_list[k-1] = True
    if all(done_list):
        t_1 = time.time()
        print(count)
        print(total)
        print(t_1 - t_0)

lam = [int(i) for i in input('lam=').strip().split()]
mu = [int(i) for i in input('mu=').strip().split()]
n = sum(lam)-sum(mu)

#n = int(input('n='))
t_0 = time.time()
t = []
count = [0 for i in range(n)]
total = 0
stat = [[0 for i in range(n)] for j in range(n)]
canperm = [[i + 1 for i in range(n)] for j in range(n)]
origin = (0, 0)
origin_t()
skew_t = [[] for i in range(n)]
for i in range(n):
    clean_t(i)
#print(skew_t[0])
pos = []
pos_t()
done_list = [False for i in range(n)]

for i in range(n):
    stat[i][0] = i + 1
    canperm[i].remove(i + 1)
    #print(stat[i])
    #print(canperm[i])
for i in range(n):
    t.append(threading.Thread(target=job, args=(i,)))
    t[i].start()

for i in range(n):
    t[i].join()

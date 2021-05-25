import threading
import time

t_0 = time.time()


def check(m):
    global pos, skew_t, stat

    for i, _pos in enumerate(pos):
        x = _pos[0]
        y = _pos[1]
        skew_t[m][x][y] = stat[m][i]
        if skew_t[m][x][y] < skew_t[m][x - 1][y] or skew_t[m][x][y] < skew_t[m][x][y - 1]:
            return 0
    return 1


def DFS(num, m):
    global n, stat, count, canperm, total

    if num == n - 2:
        slot = stat[m].index(0)
        stat[m][slot] = canperm[m][num]
        count += check(m)
        stat[m][slot] = 0
        return
    else:
        # print(num, m)
        for i in range(stat[m].index(0), n):
            if stat[m][i] == 0:
                stat[m][i] = canperm[m][num]
                DFS(num + 1, m)
                stat[m][i] = 0


def job(k):
    global count, done_list
    DFS(0, k)
    done_list[k - 1] = True
    if all(done_list):
        t_1 = time.time()
        print(count)
        print(t_1 - t_0)


lam = [int(i) for i in input('lam=').strip().split()]
mu = [int(i) for i in input('mu=').strip().split()]
n = sum(lam) - sum(mu)

count = 0
stat = [[0 for i in range(n)] for j in range(n)]
canperm = [[i + 1 for i in range(n)] for j in range(n)]
origin = (len(mu), mu[len(mu) - 1] + 1)

width = max(lam)
mu = mu + [0 for i in range(len(lam) - len(mu))]
p_lam = [(lam[i], mu[i]) for i in range(len(lam))]

skew_t = [[-1 for i in range(width + 2)]]
for i in p_lam:
    skew_t.append(
        [-1] +
        [-1 for _ in range(i[1])] + [0 for _ in range(i[0] - i[1])] + [-1 for _ in range(width - i[0])] +
        [-1]
    )
skew_t.append([-1 for i in range(width + 2)])

skew_t = [skew_t for _ in range(n)]


pos = []

for i, line in enumerate(skew_t[0]):
    for j, num in enumerate(line):
        if num == 0:
            pos.append((i, j))

done_list = [False for i in range(n)]

for i in range(n):
    stat[i][0] = i + 1
    canperm[i].remove(i + 1)


for i in range(n):
    t.append(threading.Thread(target=job, args=(i,)))
    t[i].start()


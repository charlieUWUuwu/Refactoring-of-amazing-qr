
def evaluation1(m):
    def ev1(ma):
        sc = 0
        for mi in ma:
            j = 0
            while j < len(mi)-4:
                n = 4
                while mi[j:j+n+1] in [[1]*(n+1), [0]*(n+1)]:
                    n += 1
                (sc, j) = (sc+n-2, j+n) if n > 4 else (sc, j+1)
        return sc
    return ev1(m) + ev1(list(map(list, zip(*m))))

def evaluation2(m):
    sc = 0
    for i in range(len(m)-1):
        for j in range(len(m)-1):
            sc += 3 if m[i][j] == m[i+1][j] == m[i][j+1] == m[i+1][j+1] else 0
    return sc

def evaluation3(m):
    def ev3(ma):
        sc = 0
        for mi in ma:
            j = 0
            while j < len(mi)-10:
                if mi[j:j+11] == [1,0,1,1,1,0,1,0,0,0,0]:
                    sc += 40
                    j += 7
                elif mi[j:j+11] == [0,0,0,0,1,0,1,1,1,0,1]:
                    sc += 40
                    j += 4
                else:
                    j += 1
        return sc
    return ev3(m) + ev3(list(map(list, zip(*m))))

def evaluation4(m):
    darknum = 0
    for i in m:
        darknum += sum(i)
    percent = darknum  / (len(m)**2) * 100
    s = int((50 - percent) / 5) * 5
    return 2*s if s >=0 else -2*s


class Scorer:
    @staticmethod
    def compute_score(m):
        score = evaluation1(m) + evaluation2(m)+ evaluation3(m) + evaluation4(m)
        return score
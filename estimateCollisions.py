import hashlib

def findCollision(x):
    h, n = set(), 1
    while True:
        v = hashlib.sha256(str(n).encode()).hexdigest()[:x]
        if v in h:
            return n
        h.add(v)
        n += 1

def findCollisions(s, i, y, t):
    c, h, n = 0, set(), 0
    while c < t:
        v = hashlib.sha256(str(s).encode()).hexdigest()
        b = bin(int(v, 16))[2:].zfill(256)[:y]
        if b in h:
            c += 1
        else:
            h.add(b)
        s += i
        n += 1
    return n

def calcTries(d, t, a):
    r = []
    d = [i + a for i in d]
    for y, i in enumerate(d, start=1):
        r.append(findCollisions(0, i, y, t))
    return r

def extendExp(a, n):
    r = [a[i+1] / a[i] for i in range(len(a)-1)]
    avg = sum(r) / len(r)
    for _ in range(n):
        a.append(int(a[-1] * avg))
    return a

def getValue(a, n):
    r = [a[i+1] / a[i] for i in range(len(a)-1)]
    avg = sum(r) / len(r)
    while len(a) < n:
        a.append(int(a[-1] * avg))
    return a[n-1]

def findMatch(t, x, r, iterations, stopLimit, exTo): 
    h, m = [], 0
    r = 1 if r < 1 else r
    print(f"\n# Match Finder Results\n\n```\nExtrapolated Bit = {exTo}\nStart Value = {t}\nIncrement Value = {x} * {r}\nMax Iterations = {iterations} or\nMax Bits = {stopLimit}\n```\n")
    print("| Matched Bits | Index | Hash | Bits | Formula |")
    print("|--------------|-------|------|------|---------|")
    for i in range(iterations): 
        formula1 = f"x * {r} * {i}"
        e = hashlib.sha256(str(t).encode()).hexdigest()
        b = bin(int(e, 16))[2:].zfill(256)
        for j, item in enumerate(h):
            c = 0
            for a, z in zip(b, item['b']):
                if a == z:
                    c += 1
                else:
                    break
            if c > m:
                matching = b[:c+1]
                differing1 = matching
                differing2 = matching
                print(f"| {c + 1} | {i} | {e} | {differing1} | {formula1} |")
                print(f"| {c + 1} | {j} | {item['e']} | {differing2} | {item['s']} |")
                m = c
                if m > stopLimit:  # Stop the loop if match exceeds stopLimit
                    print(f"\nStopping early as match exceeded stopLimit: {stopLimit}\n\nRemaining Iterations = {iterations - i}")
                    return
                print("| | | | | |")
        h.append({'s': f"x * {r} * {len(h)}", 'e': e, 'b': b})
        t += (x * r)

def generateCollisionReport(d, r, ed, er, t):
    print("# Collision Data Analysis Report\n")
    print("## Introduction\n")
    print(f"This report examines collision data derived from four key variables. The data explores the generations required to identify the first collision, the attempts needed to reach a defined number of conflicts (`t = {t}`), and extended datasets that offer a broader perspective on collision patterns.\n")

    print("## Data Overview\n")
    print("- **Data `d`**: Generations needed to find the first collision, incrementing sequentially from 0.")
    print(f"- **Results `r`**: Attempts required to add `d[n]` values to 0 to reach `{t}` conflicts.")
    print("- **Extended Data `ed`**: A more detailed dataset for further analysis.")
    print(f"- **Extended Results `er`**: Attempts required to find `{t}` conflicts in the extended dataset.\n")

    print("## Analysis\n")
    print("### Main Data\n")
    print(f"| Bits | Collision Value | Tries to {t} Conflicts |")
    print("|-------|---------------|--------------------|")
    for i in range(len(d)):
        tries = r[i] if i < len(r) else "extended"
        print(f"| {i+1} | {d[i]} | {tries} |")

    print("\n### Extended Data\n")
    print(f"| Bits | Collision Value | Tries to {t} Conflicts |")
    print("|-------|------------------|--------------------|")
    for i in range(len(ed)):
        extTries = er[i] if i < len(er) else "N/A"
        print(f"| {i+1} | {ed[i]} | {extTries} |")

    print("\n## Supplementary\n")
    print(f"This analysis offers detailed insights into collision patterns across primary and extended datasets. The main dataset highlights the initial collision generations and attempts required for `{t}` conflicts, while the extended data reveals additional trends over broader ranges. Such insights are crucial for refining collision detection algorithms and assessing their scalability.")

bits = 10
data = data if 'data' in globals() and len(data) == (bits - 1) else [findCollision(x) for x in range(1, bits)]

print("```\n Raw Data\n")
print(data)

t = 3 # target
a = 0 # add number to each value for further analysis
e = 24 # extend table by how many (this will generate an exponential amount)
exTo = 256 # extrapolate bit value to exTo to try with findMatch

res = calcTries(data, t, a)
print(res)

extData = extendExp(data, e)
print(extData)

extRes = calcTries(extData, t, a)
print(extRes)

print("\n End Raw Data\n```\n")
print(f"\n- Target Collisions Per Value = {t}\n- Manipulate Value By = {a}\n- Extend Bit Prediction = {e}\n- Extrapolate Bit Value = {exTo}\n")

generateCollisionReport(data, res, extData, extRes, t)
exValue = getValue(data, exTo)

multiplier = 1
maxBits = 16
maxIterations = 10000

findMatch(0, exValue, multiplier, maxIterations, maxBits, exTo)

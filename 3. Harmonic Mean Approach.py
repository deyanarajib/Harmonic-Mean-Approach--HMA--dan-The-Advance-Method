import numpy as np, pandas as pd

def line():
    print('-'*70)

def frame(data,dem,sup,lc,lr,spc):
    x = np.copy(data)
    x = np.vstack((x,dem))
    x = np.vstack((x.T,list(sup)+[0])).T
    df = pd.DataFrame(x)
    df.columns = list(lc)+['supply']
    df.index   = [' '*spc+i for i in lr]+[' '*spc+'demand']
    print(df,'\n')

raws1 = np.asarray([[489,  350,  142,  365,  424,  272,  272,  2314],
                    [272,  410,  350,  489,  365,  489,  253,  2628],
                    [424,  489,  365,  253,  410,  410,  142,  2493],
                    [365,  257,  472,  272,  350,  410,  142,  2268],
                    [350,  272,  365,  472,  410,  257,  272,  2398],
                    [1900, 1778, 1694, 1851, 1959, 1838, 1081, 0]])

raws2 = np.asarray([[12, 4,  13,  18, 9,  2,  120],
                    [9,  16, 10,  7,  15, 11, 80],
                    [4,  9,  10,  8,  9,  7,  50],
                    [9,  3,  12,  6,  4,  5,  90],
                    [7,  11, 5,   18, 2,  7,  100],
                    [16, 8,  4,   5,  1,  10, 60],
                    [75, 85, 140, 40, 95, 65, 0]])

raws3 = np.asarray([[60,   120,  75,    180,  8000],
                    [58,   100,  60,    165,  9200],
                    [62,   110,  65,    170,  6250],
                    [65,   115,  80,    175,  4900],
                    [70,   135,  85,    195,  6100],
                    [5000, 2000, 10000, 6000, 0]])

raws4 = np.asarray([[10,  2,   16,  14,  10,  300],
                    [6,   18,  12,  13,  16,  500],
                    [8,   4,   14,  12,  10,  825],
                    [14,  22,  20,  8,   18,  375],
                    [350, 400, 250, 150, 400, 0]])

print('Pilih Data')
print('1. Contoh Kasus 1')
print('2. Contoh Kasus 2')
print('3. Contoh Kasus 3')
print('4. Contoh Kasus 4')
print('5. Data Random')
cks = input('input opsi: '); print('')
cks = cks if cks in '12345' else '5'

print('CONTOH KASUS '+cks if cks in '1234' else 'DATA RANDOM',
      'MENGGUNAKAN HARMONIC MEAN APPROACH\n')

if cks in '1234':
    raws = eval('raws'+cks)
else:
    read = open('data_random.txt').read()
    raws = []
    for i in read.splitlines():
        raws.append(i.split('\t'))
    raws = np.int32(raws)
    
data = raws[:-1][:,:-1]
sups = raws[:,-1][:-1]
dems = raws[-1][:-1]
lc = ['D'+str(i+1) for i in range(len(dems))]
lr = ['S'+str(i+1) for i in range(len(sups))]

print('DATA AWAL')
frame(data,dems,sups,lc,lr,0)

if sum(dems) != sum(sups):
    diff = np.abs(sum(dems)-sum(sups))
    if sum(dems) < sum(sups):
        data = np.vstack((data.T,[1]*len(data))).T
        dems = np.hstack((dems,[diff]))
        lc   = np.hstack((lc,['dummy']))
    else:
        data = np.vstack((data,[1]*len(data[0])))
        sups = np.hstack((sups,[diff]))
        lr   = np.hstack((lr,['dummy']))
    print('PENAMBAHAN DUMMY')
    frame(data,dems,sups,lc,lr,0)

dori = np.copy(data)
aloc = []; I = 1
while True:

    try:
        hmdem = [round(len(data)/sum(1/data[:,i]),2) for i in range(len(data[0]))]
        hmsup = [round(len(data[0])/sum(1/data[i]),2) for i in range(len(data))]
    except:
        break

    print('ITERASI',I); line()
    frame(data,dems,sups,lc,lr,3)
    print('   HM Kolom',hmsup)
    print('   HM Baris',hmdem,'\n')
    
    maxhmdem = max(hmdem)
    maxhmsup = max(hmsup)

    print('>> Maksimum Harmonic Mean =>',end=' ')
    if maxhmdem >= maxhmsup:
        col = np.argmax(hmdem)
        row = np.argmin(data[:,col])
        print('Kolom',lc[col]+':',max(hmdem))
        print('>> Biaya Minimum Pada Kolom',lc[col],'=> Baris',lr[row])
    else:
        row = np.argmax(hmsup)
        col = np.argmin(data[row])
        print('Baris',lr[row]+':',max(hmsup))
        print('>> Biaya Minimum Pada Baris',lr[row],'=> Kolom',lc[col])

    
    if dems[col] <= sups[row]:
        print('>> Demand',lc[col],'(',dems[col],')','< Supply',lr[row],'(',sups[row],')')
        aloc.append((lr[row],lc[col],dems[col]))
        sups[row] = sups[row]-dems[col]
        data = np.delete(data,col,1)
        dems = np.delete(dems,col)
        hmdem = np.delete(hmdem,col)
        print('>> Maka Hapus Kolom',lc[col],'\n')
        lc = np.delete(lc,col)
    else:
        print('>> Demand',lc[col],'(',dems[col],')','> Supply',lr[row],'(',sups[row],')')
        aloc.append((lr[row],lc[col],sups[row]))
        dems[col] = dems[col]-sups[row]
        data = np.delete(data,row,0)
        sups = np.delete(sups,row)
        hmsup = np.delete(hmsup,row)
        print('>> Maka Hapus Baris',lr[row],'\n')
        lr = np.delete(lr,row)

    I += 1

print('HASIL HARMONIC MEAN APPROACH:'); line()
jumlah = 0
mystr = []
for a,b,c in aloc:
    x = int(a[-1])-1 if a != 'dummy' else -1
    y = int(b[-1])-1 if b != 'dummy' else -1
    jumlah += dori[x,y]*c
    mystr.append((a+','+b,str(dori[x,y]),str(c),dori[x,y]*c))

for a,b,c,d in mystr:
    a = a+' '*(max([len(i) for i,j,k,l in mystr])-len(a))
    b = b+' '*(max([len(j) for i,j,k,l in mystr])-len(b))
    c = c+' '*(max([len(k) for i,j,k,l in mystr])-len(c))
    strings = ' = '.join([a,' x '.join([b,c]),''])
    print(strings+str(d))
    
print(' '*len(strings)+'-'*10+' +')
print(' '*len(strings)+str(jumlah))

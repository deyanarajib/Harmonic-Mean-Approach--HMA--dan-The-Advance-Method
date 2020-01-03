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

def minscol(data,aloc,dems,sups,lc,col):
    print('>> Kolom',lc[col],'Memiliki Supply/Demand Paling Kecil:',dems[col])
    arr = data[:,col]
    if list(arr).count(min(arr)) == 1:
        row = np.argmin(arr)
    else:
        idx = np.arange(len(arr))[np.isin(arr,min(arr))]
        row = idx[np.argmin([sups[i] for i in idx])]
    print('>> Biaya Paling Kecil pada Kolom',lc[col],'=> Baris',lr[row]+':',sups[row])
    print('>> Sehingga Diperoleh:',lr[row],lc[col])
    print('>> Total Muatan',lc[col],'Sudah Terpenuhi, Hapus Kolom',lc[col],'\n')
    aloc.append((lr[row],lc[col],dems[col]))
    
    data = np.delete(data,col,1)
    sups[row] = sups[row]-dems[col]
    dems = np.delete(dems,col)
    lc  = np.delete(lc,col)
    frame(data,dems,sups,lc,lr,3)
    return data,aloc,dems,sups,lc

def minsrow(data,aloc,dems,sups,lr,row):
    print('>> Baris',lr[row],'Memiliki Supply/Demand Paling Kecil:',sups[row])
    arr = data[row]
    if list(arr).count(min(arr)) == 1:
        col = np.argmin(arr)
    else:
        idx = np.arange(len(arr))[np.isin(arr,min(arr))]
        col = idx[np.argmin([dems[i] for i in idx])]
    print('>> Biaya Paling Kecil pada Baris',lr[row],'=> Kolom',lc[col]+':',dems[col])
    print('>> Sehingga Diperoleh:',lr[row],lc[col])
    print('>> Total Muatan',lr[row],'Sudah Terpenuhi, Hapus Baris',lr[row],'\n')
    
    aloc.append((lr[row],lc[col],sups[row]))
    data = np.delete(data,row,0)
    dems[col] = dems[col]-sups[row]
    sups = np.delete(sups,row)
    lr  = np.delete(lr,row)
    frame(data,dems,sups,lc,lr,3)
    return data,aloc,dems,sups,lr

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
      'MENGGUNAKAN THE ADVANCE METHOD\n')

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

bols = np.asarray([True]*(len(data)*len(data[0]))).reshape(len(data),len(data[0]))

print('LANGKAH 1: MENYUSUN TABEL TRANSPORTASI'); line()

if sum(dems) != sum(sups):
    
    print('>> Tabel Awal Masalah Tidak Seimbang')
    frame(data,dems,sups,lc,lr,0)
    
    diff = np.abs(sum(dems)-sum(sups))
    if sum(dems) < sum(sups):
        adds = 1
        data = np.vstack((data.T,[1]*len(data))).T
        bols = np.vstack((bols.T,[False]*len(bols))).T
        dems = np.hstack((dems,[diff]))
        lc   = np.hstack((lc,['dummy']))
    else:
        adds = 0
        data = np.vstack(data,[1]*len(data[0]))
        bols = np.vstack(bols,[False]*len(bols[0]))
        sups = np.hstack((sups,[diff]))
        lr   = np.hstack((lr,['dummy']))
    print('>> Penambahan Dummy')

dori = np.copy(data)
frame(data,dems,sups,lc,lr,0)

print('LANGKAH 2: MEMILIH BIAYA GANJIL TERKECIL');line()
idx_odd = (data%2 == 1) & bols
min_odd = min(data[idx_odd])
print('>> Biaya Ganjil Terkecil:',min_odd,'\n')

print('LANGKAH 3: MENGURANGI BIAYA GANJIL DENGAN BIAYA GANJIL TERKECIL'); line()
data[idx_odd] = data[idx_odd]-min_odd
frame(data,dems,sups,lc,lr,0)

print('LANGKAH 4: MEMBANDINGKAN SUPPLY DAN DEMAND YANG MEMILIKI BIAYA 0'); line()
if list(np.concatenate(data)).count(0) == 1:
    x,y = [i[0] for i in np.where(data==0)]
else:
    indx = np.asarray(np.where(data==0)).T
    temp = [min(sups[x],dems[y]) for x,y in indx]
    x,y  = indx[np.argmin(temp)]

aloc = []
if dems[y] <= sups[x]:
    data,aloc,dems,sups,lc = minscol(data,aloc,dems,sups,lc,y)
else:
    data,aloc,dems,sups,lr = minsrow(data,aloc,dems,sups,lr,x)


print('LANGKAH 5: ULANGI LANGKAH 4 HINGGA SUPPLY DAN DEMAND TERPENUHI'); line(); print('')
I = 1
while True:
    
    try:
        mindems = min(dems)
        minsups = min(sups)
    except:
        break

    print('ITERASI',I); line()
    if mindems <= minsups:
        data,aloc,dems,sups,lc = minscol(data,aloc,dems,sups,lc,np.argmin(dems))
    else:
        data,aloc,dems,sups,lr = minsrow(data,aloc,dems,sups,lr,np.argmin(sups))

    I += 1

print('HASIL MENGGUNAKAN THE ADVANCE METHOD'); line()
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

import numpy as np, pandas as pd

def line():
    print('-'*70)

print('MEMBUAT RANDOM DATA')
line()

row = input('input banyak baris: '); row = int(row)
col = input('input banyak kolom: '); col = int(col)
print('')

print('Pilih Data')
print('1. Data Seimbang')
print('2. Data Tidak Seimbang')
opt = input('input opsi: '); print('')

lim1 = 100
lim2 = 10000

while True:
    data = [np.random.randint(1,lim1) for i in range(row*col)]
    data = np.asarray(data).reshape(row,col)

    if opt == '1':
        while True:
            sups = [np.random.randint(lim2) for i in range(row)]
            dems = [np.random.randint(lim2) for i in range(col)]
            if sum(sups) == sum(dems):
                break
    else:
        sups = [np.random.randint(lim2) for i in range(row)]
        dems = [np.random.randint(lim2) for i in range(col)]

    data = np.vstack((data,dems))
    data = np.vstack((data.T,list(sups)+[0])).T

    df = pd.DataFrame(data)
    df.columns = ['D'+str(i+1) for i in range(col)]+['Supply']
    df.index   = ['S'+str(i+i) for i in range(row)]+['Demand']
    print(df,'\n')
    print('1. Buat Ulang')
    print('2. Simpan Data')
    pil = input('input opsi: '); print('')

    if pil == '2':
        f = open('data_random.txt','w')
        for i in data:
            temp = []
            for j in i:
                temp.append(str(j))
            f.write('\t'.join(temp)+'\n')
        f.close()
        print('Data Berhasil Disimpan!')
        break

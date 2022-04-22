#menggunakan library numpy sebagai operasi matrix
import numpy as nump

#fungsi iTerminal digunakan untuk input matrix dari Terminal
def iTerminal():
    print('================================')
    n=int(input("Masukkan ukuran Matriks : "))
    a=nump.zeros((n,n),float)
    b=nump.zeros(n,float)
    print("================================")
    print("Masukkan Matriks A : ")
    for i in range (n):
        for j in range(n):
            a[i][j]=float(input("[Baris %d][Kolom %d] = " %(i+1,j+1)))
    print("Matriks A")
    print (a)
    print("================================")
    print("Masukkan Matriks B : ")
    for i in range (n):
        b[i]=float(input("b[%d] = " %(i+1)))

    return a,b

#Fungsi iFile digunakan untuk menginput matrix dari file
#Edit file iMatrixA.txt dan iMatrixB.txt jika ingin mengganti isi matrix
def iFile():
    a = nump.loadtxt("bin\iMatrixA.txt", dtype='f', delimiter=' ')
    #dtype untuk menafsirkan blok memori berukuran tetap dalam array, f sebagai floating point
    #delimiter sebagai pemisah sesuai yang diberikan
    b = nump.loadtxt("bin\iMatrixB.txt", dtype='f', delimiter=' ')
    return a,b


#Fungsi SPL Gauss
def gauss():
    a,b=menuInput()
    n=len(b) #menentukan panjang input var b
    A=nump.column_stack((a,b))
    x=nump.zeros(n,float)

    #Eliminasi Pivoting
    for i in range(0, n):
       # Mencari kolom dengan nilai Maximal
       maxE = abs(A[i][i])
       maxBar = i
       for k in range(i+1, n):
           # mengecek perbaris dan baris pertama tidak boleh 0
           if abs(A[k][i]) < maxE or maxE == 0:
               maxE = abs(A[k][i])
               maxBar = k
       # menukar baris terakhir dengan baris bernilai 0 dilakukan kolom per kolom
       for k in range(i, n+1):
           tmp = A[maxBar][k]
           A[maxBar][k] = A[i][k]
           A[i][k] = tmp
       # membuat semua baris dibawah 1 utama menjadi nilai 0
       for k in range(i+1, n):
           c = -A[k][i]/A[i][i]
           for j in range(i, n+1):
               if i == j:
                   A[k][j] = 0
               else:
                   A[k][j] = A[k][j] + c * A[i][j]

    #Melakukan subtitusi mundur

    for i in range(n-1, -1, -1):
        if A[i][i] == 0:
            return [0 for i in range(n)]
        else:
            x[i] = A[i][n]/A[i][i]
            for k in range(i-1, -1, -1):
                A[k][n] = A[k][n] - A[k][i]*x[i]
    a,b=nump.hsplit(A,[n])
    return a,x

#Fungsi gauss-Jordan
def gaussJordan():
    a,b=menuInput()
    n=len(b)

    for i in range(n):
        #Pivoting
        if nump.fabs(a[i,i]) == 0:
            for j in range(i+1,n):
                if nump.fabs(a[j,i]) > nump.fabs(a[i,i]):
                    for k in range(i,n):
                        a[i,k],a[j,k] = a[j,k],a[i,k]
                    b[i],b[j] = b[j],b[i]
                    break

        pivot = a[i,i]
        for j in range(i,n):
            a[i,j] /= pivot
        b[i] /= pivot

        #Substitusi
        for j in range(n):
            if j == i or a[j,i] == 0: continue
            factor = a[j,i]
            for k in range(i,n):
                a[j,k] -= factor * a[i,k]
            b[j] -= factor*b[i]
    return a,b


#Fungsi ini untuk mengecek apakah tidak ada solusi atau memiliki banyak solusi
def Hasil(A,B):
    i=len(B)-1

    #jika tidak ada solusi/ memiliki banyak solusi maka program menampilakan pesan
    #hasil yang bukan solusi tunggal/unik
    if nump.all(nump.isinf(B)):
        print('Hasil Eliminasi :\nTidak ada Solusi')
        #Menyimpan output kedalam file
        with open('bin\output.txt', 'a') as out:
            print('Hasil Eliminasi :\nTidak ada Solusi',file=out) #pesan yang ditampilkan
            print('================================================',file=out)
        return
    
    elif nump.all(nump.isnan(B)):
        print('Hasil Eliminasi :\nMemiliki Banyak solusi') #pesan yang ditampilkan
        #Menyimpan output kedalam file
        with open('bin\output.txt', 'a') as out:
            print('Hasil Eliminasi :\nMemiliki Solusi Banyak',file=out)
            print('================================================',file=out)
        return

    #Syntax dibawah berjalan karena matrix memiliki solusi dan tidak memiliki banyak solusi
    print("================================")
    print("Matrix setelah OBE : ")
    print(A)
    print("================================")
    print("Hasil Eliminasi  : ")
    for j in range(len(B)):
        print("X%d = %0.1f" %(j+1,B[j]) , end='\n')
    print("================================")
    
    #menyimpan hasil ke file output.txt
    with open('bin\output.txt', 'ab') as out:
        nump.savetxt(out,A,fmt='%0.1f',delimiter=' ',header='Matrix Setelah OBE')
        nump.savetxt(out,B,fmt='%0.1f',delimiter='\n',header='Hasil Eliminasi',footer='=========================================================')
    
#Index Menu merupakan menu awal yang ditampilkan di layar
def Indexmenu():
    print('================================')
    print('          Program')
    print('   Gauss & Gauss Jordan')
    print('================================')
    print('        Pilih Menu Index')
    print('1). SPL Gauss')
    print('2). SPL Gauss Jordan')
    print('999). Hentikan Program')
    switch=int(input('Input Angka : '))
    if switch==999:
        print('Program Dihentikan!')
        exit()
    elif switch==1 :
        a,b = gauss()
    elif switch==2 :
        a,b = gaussJordan()
    else:
        print('Inputan tidak ada dalam List!') 
        Indexmenu()
    return a,b

#Pemilihan input menu
def menuInput():
    print('================================')
    print('        Pilih Cara Input')
    print('1). Input dari Terminal')
    print('2). Input dari File')
    print('999). Hentikan Program')
    switch=int(input('Input Angka : '))
    
    if switch==999:
        print('Program Dihentikan!')
        exit()
    elif(switch==1):
        a,b = iTerminal()
    elif(switch==2):
        a,b = iFile()
    else:
        print('Inputan tidak ada dalam List! ')
        menuInput()
    return a,b

#Program mulai !!
A,X = Indexmenu()
Hasil(A,X)
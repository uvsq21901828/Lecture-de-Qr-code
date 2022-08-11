import PIL as pil
from PIL import Image



def nbrCol(matrice):
    return len(matrice[0])

def nbrLig(matrice):
    return len(matrice)


def lire_mat(matrice):
    for i in range(nbrLig(matrice)):
        print(matrice[i])

def printQR(mat) :
    def symbol(cell) :
        if cell==1 : return '██'
        if cell==0 : return '  '
    mat = [[symbol(cell) for cell in l] for l in mat]
    print('\n'.join([''.join(line) for line in mat]))
    return

#Sauvegarde et ecrit le qr code
def saving(matPix, filename):
    toSave= pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrCol(matPix)):
        for j in range(nbrLig(matPix)):
            toSave.putpixel((i,j),matPix[j][i])
    toSave.save(filename)

matVB=[[(1) for j in range(25)] for i in range(25)]

saving(matVB,"QRcODE.png")

#Charge la matrice du qr code
def loading(filename):
    toLoad=pil.Image.open(filename)
    return [[1 if toLoad.getpixel((j,i)) else 0 for j in range(toLoad.size[0])] for i in range(toLoad.size[1])]






#Question 1
def coin(matrice, i, j):
    return True if ((j == 1 or j == 5) and (i > 1 and i < 6)) or ((i == 1 or i == 5) and (j > 1 and j < 6)) or (i == 1 and j == 1) or (i == 7 or j == 7) else False

def symbole():
    symb = [[0 for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            symb[i][j]= 1 if coin(matrice, i , j) else 0
    return symb
                
def rotation(matrice):
    return list(reversed(list(zip(*matrice))))

def position(matrice):
    x, y = nbrCol(matrice), nbrLig(matrice)
    p = []
    for i in range(7):
        p.append((symbole()[i])[:7])
    coin_d = [[matrice[i][j] for j in range(x-7, x)] for i in range(y-7, y)]
    while (coin_d == p):
        matrice = rotation(matrice)
        coin_d = [[matrice[i][j] for j in range(x-7, x)] for i in range(y-7, y)]
    return matrice


#Question 2
def verif_ligne(matrice):
    for i in range(7, nbrLig(matrice)-7):
        if (i%2) != matrice[i][6]:
            return False
    for j in range(7, nbrCol(matrice)-7):
        if (j%2) != matrice[6][j]:
            return False
    return True


# Question 3
def lecture_bit(bits):
    d1, d2, d3, d4, p1, p2, p3 = bits
    c1 = "0" if (d1 + d2 + d4) % 2 == p1 else "1"
    c2 = "0" if (d1 + d3 + d4) % 2 == p2 else "1"
    c3 = "0" if (d2 + d3 + d4) % 2 == p3 else "1"
    e = int(c3 + c2 + c1, 2)

    if e:
        bits[e-1] = 1 - bits[e-1]
        d1, d2, d3, d4, _, _, _ = bits
    return d1, d2, d3, d4



#Question 4

def lectureBlocGaD(m):
    bit = []
    for j in range(nbrCol(m)):
        for i in range(nbrLig(m)-1, -1, -1):
            bit.append(m[i][j])

    return bit

def lectureBlocDaG(m):
    bit = []
    for j in range(nbrCol(m)-1, -1, -1):
        for i in range(nbrLig(m)-1, -1, -1):
            bit.append(m[i][j])

    return bit


def get_bloc(matrice):
    x, y = nbrLig(matrice), nbrCol(matrice)
    list_bloc = []
    for _ in range(4):
        b_bloc = [[(x, y), (x, y-7)], [(x-2, y-7), (x-2, y)]]
        for w in b_bloc:
            for a, b in w:
                list_bloc.append([[matrice[i][j] for j in range(b-7, b)] for i in range(a-2, a)])
            x -= 4
    return list_bloc

def lectQR(matrice, n=16):
    code = []
    listeb = get_bloc(matrice)
    for i in range(n):
        x = lectureBlocDaG(listeb[i]) if (i%4 == 0) or (i%4 ==1) else lectureBlocGaD(listeb[i])
        code.append(x)
    return code

#Question 5

def conv_ascii(tab):
    return chr(int(tab, 2))

def conv_hexa(tab):
    return hex(int(tab, 2)).strip("0x")

def bloc_lire(t):
    msg1, msg2 = [], []
    for i in t:
        msg1.append(i) if len(msg1)<7 else msg2.append(i)
    return ("".join(map(str,lecture_bit(msg1))), "".join(map(str,lecture_bit(msg2))))

def affiche_content(matrice, n):
    if matrice[24][8]:
        for i in lectQR(matrice, n):
            x, y = bloc_lire(i)
            print(conv_ascii(x+y), end='')
        print("\n")
    else :
        for i in lectQR(matrice, n):
            x, y = bloc_lire(i)
            print(conv_hexa(x+y), end='')
        print("\n")

# Question 6

def damier(matrice):
    mat  = [[0 for j in range(nbrCol(matrice))] for i in range(nbrLig(matrice))]
    for i in range(nbrLig(matrice)):
        for j in range(nbrCol(matrice)):
            if matrice[i][j]:
                mat[i][j] = 1 if (i+j)%2 else 0
            else :
                mat[i][j] = 0 if (i+j)%2 else 1
    return mat

def ligne_h(matrice):
    mat  = [[0 for j in range(nbrCol(matrice))] for i in range(nbrLig(matrice))]
    for i in range(nbrLig(matrice)):
        for j in range(nbrCol(matrice)):
            if matrice[i][j]:
                mat[i][j] = 1 if (i)%2 else 0
            else :
                mat[i][j] = 0 if (i)%2 else 1
    return mat

def ligne_v(matrice):
    mat  = [[0 for j in range(nbrCol(matrice))] for i in range(nbrLig(matrice))]
    for i in range(nbrLig(matrice)):
        for j in range(nbrCol(matrice)):
            if matrice[i][j]:
                mat[i][j] = 1 if (j)%2 else 0
            else :
                mat[i][j] = 0 if (j)%2 else 1
    return mat

def filtre(matrice):
    if matrice[22][8]:
        if matrice[23][8]:
            #(1,1)
            return ligne_v(matrice)
        else:
            #(1,0)
            return ligne_h(matrice)
    else :
        if matrice[23][8]:
            #(0,1)
            return damier(matrice)
        else:
            #(0,0)
            return matrice

#Question 7

def decodage(matrice):
    code = ""
    for i in range(13, 18):
        code += str(matrice[i][0])
    x = int(code, 2)
    affiche_content(matrice, x-1)

if __name__ == "__main__":
    matrice=loading("Exemples/qr_code_ssfiltre_ascii.png")

    matrice = position(matrice)
    printQR(matrice)
    print(verif_ligne(matrice))
    print("")

   
    decodage(matrice)


    saving(matrice,"QRcODE.png")
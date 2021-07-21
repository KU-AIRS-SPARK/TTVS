#RoTA Marmara -> RoTa_Marmara olarak değiştir.
#SUBÜ_AISET   -> SUBU_AISET   olarak değiştir.
#RACLAB-Sigun klasöründe classes.txt var, silinmeli.
#commonPath'i kendi dizininize göre değiştirin.

# encoding:utf-8

import os 
import shutil


# Dosya ismi başına ön ek koyma
def PrefixFileName(folderPath, prefix): 
    if not folderPath.endswith("/"):
        folderPath = folderPath + "/"
    for subdir, dirs, files in os.walk(folderPath):
        for file in files:
            if not file.startswith(prefix):
                os.rename(folderPath + file, folderPath + prefix + file)
        break


# Dosya isimlerinin başına yoksa ön ek konarak tekilleştirilmesi sağlanıyor
commonPath = "/Users/onderakacik/SPARK/Training/TTVS/" # Veri yolu. Bu kısmı kendinize göre değiştirin.


PrefixFileName(commonPath + "BURST", "BUR")
PrefixFileName(commonPath + "BURST/labels", "BUR")
PrefixFileName(commonPath + "YTU-AESK", "YTU")
PrefixFileName(commonPath + "YTU-AESK/labels", "YTU")
PrefixFileName(commonPath + "ITU-RacingDriverless", "ITU")
PrefixFileName(commonPath + "ITU-RacingDriverless/yoloLabels", "ITU")
PrefixFileName(commonPath + "GTU/Dataset1", "GTU1_")
PrefixFileName(commonPath + "GTU/Dataset1/labels", "GTU1_")
PrefixFileName(commonPath + "GTU/Dataset2", "GTU2_")
PrefixFileName(commonPath + "GTU/Dataset2/labels", "GTU2_")
PrefixFileName(commonPath + "Basarsoft/Sag", "BSR")
PrefixFileName(commonPath + "Basarsoft/Sag/labels", "BSR")
PrefixFileName(commonPath + "Basarsoft/Sol", "BSR")
PrefixFileName(commonPath + "Basarsoft/Sol/labels", "BSR")


# Alt bölümdeki kod ile Başaroft CSV dosyasındaki etiket isimlerinin tekil bir listesi oluşturulur.

# file = open(commonPath + "Basarsoft/bsr_sag_labels.csv", "r")
# file2 = open(commonPath + "Basarsoft/AllList.txt", "a")
# SplitData = []
# ListData = []
# data = file.readlines()
#
# for i in range(len(data)):
#     SplitData.append(list(data[i].split(",")))
#     ListData.append(SplitData[i][3])
# for x in range(len(ListData)):
#     unionlist = list(set().union(ListData))
# for x in range(len(unionlist)):    
#     file2.write(unionlist[x]+ "\n\n",)


#Kolay inceleme için etiket dosyalarını tek bir dosyada birleştirir
def CombineYolo(rootdir): 
    f = open(rootdir + 'all.txt','a')
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if not file.endswith('.txt') : continue
            file1 = open(rootdir+file, 'r')
            Lines = file1.readlines()
                
            for line in Lines:
                    
                f.write(file)
                f.write(' ')
                f.write(line)
    f.close()


#CombineYolo(commonPath + 'GTU/Dataset1/labels/')


# İndeksleri standartları ile değiştirip yeni bir dosyaya kaydeder
def ConvertYolo(path, dictionary): # Etiket İndeksi Dönüştürülecek Dosyaların Yolu ve Eşleştirilmiş Sözlük
    path = path + "/"
    
    standartPath = path + "standart/" #Mevcutsa önce klasörü sil
    if os.path.exists(standartPath) and os.path.isdir(standartPath):
        shutil.rmtree(standartPath)
    os.mkdir(standartPath)  #Klasörü oluştur
    
    for subdir, dirs, files in os.walk(path):
        for file in files:
            FileControl = os.path.isfile(standartPath + file) 
            if not FileControl:
                f = open(standartPath + file, 'a') # Belirtilen isimde klasör oluşturur
                if not file.endswith('.txt') : continue # Dosya tipi kontrolü
                file1 = open(path +"/" + file, 'r') #Dosyayı okumak için açar
                Lines = file1.readlines() # Dosya içindeki verileri satır satır okur
                for i in range(len(Lines)): # Dosya içindeki satır kadar okuma yapar
                    splitDataTag = Lines[i].split(" ") # Satır içindeki verileri boşluklara göre ayırır
                    print(file) #debuggggggGG
                    if int(splitDataTag[0]) < 0:
                        print("Tanımlanamayan tag => " + path + "/" + file + " geçersiz değer= (" + splitDataTag[0] +")\n")
                    else:
                        splitDataTag[0] = str(dictionary[int(splitDataTag[0])][1]) # Dictionary sırası ile Basarsoft etiketini eşleştirir. 
                        Lines[i] = " ".join(splitDataTag) # Orjinal etiketi TC_Karayolları etiketi ile değiştirir
                        f.write(str(Lines[i])) # Dosyaya yazar.
                f.close()


# Başarsoft csv dosyası yolo formatına çevrilir
def ConvertCsvtoYolo(path):
    path = path + "/" 
    labelsPath = path + "labels/"
    if os.path.exists(labelsPath) and os.path.isdir(labelsPath):
        shutil.rmtree(labelsPath)
    os.mkdir(labelsPath)
    
    for subdir, dirs, files in os.walk(path):
        for file in files:            
            if not file.endswith('.csv') : continue # Dosya tipi kontrolü
            file1 = open(path + file, encoding="UTF-8") #Dosyayı okumak için açar
            Lines = file1.readlines() # Dosya içindeki verileri satır satır okur
            for i in range(len(Lines)): # Dosya içindeki satır kadar okuma yapar
                splitDataTag = Lines[i].split(",") # Satır içindeki verileri boşluklara göre ayırır
                if not splitDataTag[0] == "filename":
                    _fileName = splitDataTag[0].rsplit('.', 1) # Dosya ismi ile dosya formatının ismini ayırır
                    f = open(path + 'labels/BSR' + _fileName[0] +'.txt','a') # Belirtilen isimde klasör oluşturur
                    x1 = ((int(splitDataTag[4])+int(splitDataTag[6]))/2)/int(splitDataTag[1]) # Hesaplamalar
                    y1 = ((int(splitDataTag[5])+int(splitDataTag[7]))/2)/int(splitDataTag[2])
                    x2 = (int(splitDataTag[6])-int(splitDataTag[4]))/int(splitDataTag[1])
                    y2 = (int(splitDataTag[7])-int(splitDataTag[5]))/int(splitDataTag[2])  
                    f.write(str(TC_Karayolları[splitDataTag[3]]))
                    f.write(" ")                    
                    f.write(str(round(x1, 6))) # Virgül kontrolü ile dosyaya yazar.
                    f.write(" ")
                    f.write(str(round(y1, 6)))
                    f.write(" ")
                    f.write(str(round(x2, 6)))
                    f.write(" ")
                    f.write(str(round(y2, 6)))
                    f.write("\n")
                    f.close()
        break


# Türkiye Cumhuriyeti Karayolları Genel Müdürlüğü Yönetmeliğindeki isimlerle oluşturulmuş trafik işaretleri sınıf listesi
TC_Karayolları = {
    "Kasisli Yol":0,
    "İleri Ve Sağa Mecburi Yön":1,
    "Okul Geçidi (B-14b)":2,
    "Ana Yol Tali Yol (T-22b)":3,
    "Sola Tehlikeli Viraj":4,
    "Yaya Geçidi (B-14a)":5,
    "U Dönüşü Yapılmaz":6,
    "Hastane":7,
    "Akaryakıt İstasyonu":8,
    "Ana Yol Tali Yol (T-22a)":9,
    "Ana Yol Tali Yol Sağ":10,
    "Yaya Geçidi (T-11)":11,
    "Sola Dönülmez":12,
    "Okul Geçidi (T-12)":13,
    "İleri Ve Sola Mecburi Yön":14,
    "Gizli Buzlanma":15,
    "Ana Yol Tali Yol(T-22a)":16,
    "Sağa Tehlikeli Viraj":17,
    "Sağdan Gidiniz":18,
    "Gabari":19,
    "Tek Yönlü Yol":20,
    "Sağa Dönülmez":21,
    "Ana Yol Tali Yol Kavşağı (T-22a)":22,
    "Yön Levhası":23,
    "Ana Yol Tali Yol Kavşağı (T-22b)":24,
    "Park Etmek Yasaktır":25,
    "Işıklı İşaret Cihazı":26,
    "Ada Etrafında Dönünüz":27,
    "Ana Yol Tali Yol Kavşağı (T-22d)":28,
    "İleri Çıkmaz Yol":29,
    "Girişi Olmayan Yol":30,
    "Ana Yol Tali Yol (T-22d)":31,
    "Sağdan Daralan Kaplama":32,
    "Ana Yol Tali Yol (T-22c)":33,
    "Yol Ver":34,
    "Ana Yol":35,
    "Yük Taşıtlarının Öndeki Taşıtı Geçmesi Yasaktır":36,
    "Öndeki Taşıtı Geçmek Yasaktır":37,
    "Tehlike":38,
    "Yolda Çalışma":39,
    "Dur":40,
    "İleri Mecburi Yön":41,
    "Kaygan Yol":42,
    "Sağa Mecburi Yön":43,
    "Taşıt Trafiğine Kapalı Yol":44,
    "Trafik Lambası":45,
    "Kamyonlar için Geçme Yasağı Sonu":46,
    "Kamyon Giremez":47,
    "Geçme Yasağı Sonu":48,
    "Bisiklet Geçebilir":49,
    "Çıkmaz Yol":50,
    "İki Taraftan Daralan Kaplama":51,
    "Sınırlama Sonu":52,
    "Soldan Gidiniz":53,
    "Tehlikeli Viraj Yön Levhası":54,
    "Vahşi Hayvanlar Geçebilir":55,
    "Park Yeri":56, 
    "Durak":57,
    "Azami Hız Sınırlaması 10":58,
    "Azami Hız Sınırlaması 20":59,
    "Azami Hız Sınırlaması 30":60, 
    "Azami Hız Sınırlaması 40":61, 
    "Azami Hız Sınırlaması 50":62, 
    "Azami Hız Sınırlaması 60":63, 
    "Azami Hız Sınırlaması 70":64, 
    "Azami Hız Sınırlaması 82":65, 
    "Hız Sınırlaması Sonu 20":66,
    "Yeşil Işık":67,
    "Kırmızı Işık":68,
    "Sarı Işık":69,
    "İleriden Sola Mecburi Yön":70,
    "İleriden Sağa Mecburi Yön":71,  
    "Sağdan Ana Yola Giriş":72,
    "Her İki Yandan Gidiniz":73,
    "Duraklamak ve Park Etmek Yasaktır":74,
    "Sola Mecburi Yön":75,
    "Dönüş Adası Ek Levhası":76,
    "Refüj Başı Ek Levhası (Sol)":77,
    "Refüj Başı Ek Levhası (Sağ)":78,
    "Dönel Kavşak":79,
    "Yaya Üst Geçidi":80,
    "Sağa ve Sola Mecburi Yön":81,
    "Mecburi Bisiklet Yolu":82,
    "Engelli Park Yeri":83,
    "Elektronik Denetleme Sistemi":84,
    "Azami Hız Sınırlaması 120":85,
    "Mecburi Asgari Hız 40":86,
    "Onarım Yaklaşım Levhası":87,
    "Kontrolsüz Kavşak":88,
    "Mecburi Bisiklet Yolu Sonu":89,
    "U Dönüşü Levhası":90,
    "Sola Tehlikeli Devamlı Virajlar":91,
    "Bütün Yasaklama Ve Kısıtlamaların Sonu":92,
    "Hız Sınırlaması Sonu 80":93,
    "Azami Hız Sınırlaması 80":94,
    "Azami Hız Sınırlaması 100":95
}

DTSIS = {
    0: ["otuz", 60],
    1: ["elli", 62],
    2: ["yetmis", 64],
    3: ["trafik", 45],
    4: ["yaya", 11],
    5: ["ada", 76],
}

Btu_Elektronomi = {
    0: ["Park yeri", 56],  # 0  Park Yeri
    2: ["Saga donulmez", 21],  # 2  Sağa Dönülmez
    3: ["Durak", 57],  # 3  Durak
    5: ["Tasit trafigine kapali yol", 44],  # 5  Taşıt Trafiğine Kapalı Yol
    7: ["Azami hiz sinirlamasi (30 km/saat)", 60],  # 7  Azami Hız Sınırlaması 30
    8: ["Ileri ve saga mecburi yon", 1],  # 8  İleri ve Sağa Mecburi Yön
    9: ["Giris olmayan yol", 30],  # 9  Girişi Olmayan Yol
    10: ["Ileri ve sola mecburi yon", 14],  # 10 İleri ve Sola Mecburi Yön
    11: ["Dur", 40],  # 11 Dur
    12: ["Sola donulmez", 12],  # 12 Sola Dönülmez
    13: ["Park etmek yasaktir", 25],  # 13 Park Etmek Yasaktır
}

GTU1 = {
    0: ["Sola donulmez", 12],  # 0 Sola Dönülmez
    1: ["Saga donulmez", 21],  # 1 Sağa Dönülmez
    2: ["Giris olmayan yol", 30],  # 2 Girişi Olmayan Yol
    3: ["Park yeri", 56],  # 3 Park Yeri
    4: ["Park etmek yasaktir", 25],  # 4 Park Etmek Yasaktır
    5: ["Dur", 40],  # 5 Dur
    6: ["Durak", 57],  # 6 Durak
    7: ["Tasit trafigine kapali yol", 44],  # 7 Taşıt Trafiğine Kapalı Yol
    8: ["Kirmizi", 68],  # 8 Kırmızı Işık
    9: ["Yesil", 67],  # 9 Yeşil Işık
    10: ["Ileriden sola mecburi yon", 70],  # 10 İleriden Sola Mecburi Yön
    11: ["Ileriden saga mecburi yon", 71],  # 11 İleriden Sağa Mecburi Yön
    12: ["Ileri ve saga mecburi yon", 1],  # 12 İleri Ve Sağa Mecburi Yön
    13: ["Ileri ve sola mecburi yon", 14],  # 13 İleri Ve Sola Mecburi Yön
    14: ["Azami hiz sinirlamasi (20 km/saat)", 59],  # 14 Azami Hız Sınırlaması 20
    15: ["Hiz sinirlamasi sonu (20 km/saat)", 66],  # 15 Hız Sınırlaması Sonu 20
    16: ["Azami hiz sinirlamasi (30 km/saat)", 60],  # 16 Azami Hız Sınırlaması 30
    17: ["Sola donulmez", 12],  # 17 Sola Dönülmez
}

ITU_RacingDriverless = {
    0: ["dur", 40],  # 0 Dur
    1: ["durak", 57],  # 1 Durak
    2: ["sagaDonulmez", 21],  # 2 Sağa Dönülmez
    3: ["solaDonulmez", 12],  # 3 Sola Dönülmez
    4: ["girilmez", 30],  # 4 Girişi Olmayan yol
    5: ["tasitGiremez", 44],  # 5 Taşıt Trafiğine Kapalı Yol
    6: ["parkYasak", 25],  # 6 Park Etmek Yasaktır
    7: ["park", 56],  # 7 Park yeri
    8: ["trafikIsigi", 45],  # 8 Trafik Lambası
}

KU_AIRS_Spark = {
    0: ["Giris olmayan yol", 30],  # 0 Girişi Olmayan Yol
    1: ["Tasit trafigine kapali yol", 44],  # 1 Taşıt Trafiğine Kapalı Yol
    2: ["Ileri ve sola mecburi yön", 14],  # 2 İleri Ve Sola Mecburi Yön
    3: ["Ileri ve saga mecburi yön", 1],  # 3 İleri Ve Sağa Mecburi Yön
    4: ["Ilerden sola mecburi yön", 70],  # 4 İleriden Sola Mecburi Yön
    5: ["Hiz sinirlamasi sonu (20 km/saat)", 66],  # 5 Hız Sınırlaması Sonu 20
    6: ["Azami hiz sinirlamasi (30 km/saat)", 60],  # 6 Azami Hız Sınırlaması 30
    7: ["Azami hiz sinirlamasi (20 km/saat)", 59],  # 7 Azami Hız Sınırlaması 20
    8: ["Ileriden saga mecburi yön", 71],  # 8 İleriden Sağa Mecburi Yön
    9: ["Saga dönülmez", 21],  # 9 Sağa Dönülmez
    10: ["Sola dönülmez", 12],  # 10 Sola Dönülmez
    11: ["Dur", 40],  # 11 Dur
    12: ["kirmizi isik", 68],  # 12 Kırmızı Işık
    13: ["yesil isik", 67],  # 13 Yeşik Işık
    14: ["durak", 57],  # 14 Durak
    15: ["park yasak", 25],  # 15 Park Etmek Yasaktır
    16: ["park edilebilir", 56],  # 16 Park Yeri
    17: ["dumduz gidiniz", 41],  # 17 İleri Mecburi Yön
}

YTU_AESK = {
    0: ["girilmez", 30],  # 0 Girişi Olmayan Yol
    1: ["tasit_trafigine_kapali", 44],  # 1 Taşıt Trafiğine Kapalı Yol
    2: ["duz_veya_sola", 14],  # 2 İleri Ve Sola Mecburi Yön
    3: ["duz_veya_saga", 1],  # 3 İleri Ve Sağa Mecburi Yön
    4: ["yalnizca_sola", 70],  # 4 İleriden Sola Mecburi Yön
    5: ["20_hiz_limiti_sonu", 66],  # 5 Hız Sınırlaması Sonu 20
    6: ["30_limit", 60],  # 6 Azami Hız Sınırlaması 30
    7: ["20_limit", 59],  # 7 Azami Hız Sınırlaması 20
    8: ["yalnizca_saga", 71],  # 8 İleriden Sağa Mecburi Yön
    9: ["saga_donulmez", 21],  # 9 Sağa Dönülmez
    10: ["sola_donulmez", 12],  # 10 Sola Dönülmez
    11: ["dur", 40],  # 11 Dur
    12: ["park_yapilmaz", 25],  # 12 Park Etmek Yasaktır
    13: ["park", 56],  # 13 Park Yeri
    14: ["durak", 57],  # 14 Durak
    15: ["kirmizi_isik", 68],  # 15 Kırmızı Işık
    16: ["sari_isik", 69],  # 16 Sarı Işık
    17: ["yesil_isik", 67],  # 17 Yeşil Işık
}

savhascelik = {
    0: ["Dur Tabelası", 40],  # 0 Dur
    1: ["Durak Tabelası", 57],  # 1 Durak
    2: ["Hız Limiti 30 Tabelası", 60],  # 2 Azami Hız Sınırlaması 30
    3: ["Sağa Dönülebilir Veya İleri Gidilebilir Tabelası", 1],  # 3 İleri Ve Sağa Mecburi Yön
    4: ["Sağa Dönüş Yasak Tabelası", 21],  # 4 Sağa Dönülmez
    5: ["Sola Dönülebilir Veya İleri Gidilebilir Tabelası", 14],  # 5 İleri Ve Sola Mecburi Yön
    6: ["Sola Dönüş Yasak Tabelası", 12],  # 6 Sola Dönülmez
    7: ["Kırmızı Işık Tabelası", 68],  # 7 Kırmızı Işık
    8: ["Yeşil Işık Tabelası", 67],  # 8 Yeşik Işık
    9: ["Park Tabelası", 56],  # 9 Park Yeri
    10: ["Park Yasak Tabelası", 25],  # 10 Park Etmek Yasaktır
    11: ["Hız Limiti 20 Tabelası", 59],  # 11 Azami Hız Sınırlaması 30
    12: ["Geçiş Yok Tabelası", 30],  # 12 Girişi Olmayan Yol
    13: ["Hız Limiti 50 Tabelası", 62],  # 13 Azami Hız Sınırlaması 50
    14: ["Yol Ver Tabelası", 34],  # 14 Yol Ver
    15: ["Işıklı İşaret Cihazı", 26],  # 15 Işıklı İşaret Cihazı
    16: ["Dönüş Adası Tabelası", 27],  # 16 Ada Etrafında Dönünüz
    17: ["Yön Tabelası", 23],  # 17 Yön Levhası
    18: ["Sağdan Anayol Girişi", 72],  # 18 Sağdan Ana Yola Giriş
    19: ["Sağa Mecburi Yön", 43],  # 19 Sağa Mecburi Yön
    20: ["Sola Mecburi Yön", 75],  # 20 Sola Mecburi Yön
    21: ["Sağdan Gidiniz", 18],  # 21 Sağdan Gidiniz
    22: ["Soldan Gidiniz", 53],  # 22 Soldan Gidiniz
    23: ["Ada Etrafında Dönene Kadar Yol Ver", 27],  # 23 Ada Etrafında Dönünüz
    24: ["Hız Limiti 40 Tabelası", 61],  # 24 Azami Hız Sınırlaması 40
    25: ["Tehlikeli Viraj Tabelası", 54],  # 25 Tehlikeli Viraj Yön Levhası
    26: ["Tümsek Uyarı Tabelası", 0],  # 26 Kasisli Yol
    27: ["Hız Limiti 10 Tabelası", 58],  # 27 Azami Hız Sınırlaması 10
    28: ["Yaya Geçidi", 5],  # 28 Yaya Geçidi
    29: ["Hız Limiti 70 Tabelası", 64],  # 29 Azami Hız Sınırlaması 70
    30: ["U Dönüşü Yasak Tabelası", 6],  # 30 U Dönüşü Yapılmaz
    31: ["Kamyon Giremez", 47],  # 31 Kamyon Giremez
    32: ["Her İki Yandan Gidiniz", 73],  # 32 Her İki Yandan Gidiniz
    33: ["Hız Limiti 60 Tabelası", 63],  # 33 Azami Hız Sınırlaması 60
    34: ["Okul Geçidi", 13],  # 34 Okul Geçidi
    35: ["Hız Limiti 82 Tabelası", 65],  # 35 Azami Hız Sınırlaması 82
    36: ["Duraklama ve Park Etme Yasak", 74],  # 36 Duraklamak Ve Park Etmek Yasaktır
}

GumusArge = {
    0: ["sola_donulmez", 12],
    1: ["hiz_siniri_30", 60],
    2: ["sola_mecburi", 75],
    3: ["duraklamak_yasak", 74],
    4: ["ileri_saga_mecburi", 71],
    5: ["hiz_siniri_20", 59],
    6: ["saga_mecburi", 43],
    7: ["saga_donulmez", 21],
    8: ["dur", 40],
    9: ["girisi_olmayan_yol", 30],
    10: ["ileri_sola_mecburi", 70],
    11: ["durak", 57],
}

Kızıl_Elma = {
    0: ["kirmizi isik", 68],
    1: ["park", 56],
    2: ["durak", 57],
    3: ["park yapilamaz", 74],
    4: ["ileriden saga mecburi", 71],
    5: ["ileriden sola mecburi", 70],
    6: ["ileriden veya saga mecburi yon", 1],
    7: ["ileriden veya sola mecburi yon", 14],
    8: ["dur", 40],
    9: ["saga donulemez", 21],
    10: ["sola donulmez", 12],
    11: ["girilmez", 30],
    12: ["tasit trafigine kapali yol", 44],
    13: ["sari isik", 69],
    14: ["yeşil ışık", 67],
    15: ["20 hiz siniri", 59],
    16: ["30 hiz siniri", 60],
    17: ["düz git", 41],
}

RACLAB_Sigun = {
    0: ["dur", 40],
    1: ["durak", 57],
    2: ["sagaDonulmez", 21],
    3: ["solaDonulmez", 12],
    4: ["girilmez", 30],
    5: ["tasitGiremez", 30],
    6: ["parkYasak", 74],
    7: ["park", 56],
    8: ["trafikIsigi", 45],
    9: ["sinir20son", 59], #?
    10: ["sinir30", 60],
    11: ["sinir20", 59],
}

Yeditepe_Automotive = {
    0: ["dur", 40],
    1: ["mecburi sag", 43], #Hatalıydı
    2: ["mecburi sol", 75],
    3: ["ileri ve sag", 1],
    4: ["ileri ve sol", 14],
    5: ["kirmizi isik", 68],
    6: ["durak", 57],
    7: ["girilmez", 30],
    8: ["saga donulmez", 21],
    9: ["sola donulmez", 12],
    10: ["park edilebilir", 56],
    11: ["park edilemez", 74],
}


#ConvertCsvtoYolo(commonPath + "Basarsoft/Sag")
#ConvertCsvtoYolo(commonPath + "Basarsoft/Sol")

ConvertYolo(commonPath + "DTSIS/labels", DTSIS)

#ConvertYolo(commonPath + "AITT/labels", AITT)

#ConvertYolo(commonPath + "BURST/labels", BURST)

ConvertYolo(commonPath + "Btu-Elektronomi/labels", Btu_Elektronomi)

#ConvertYolo(commonPath + "Cukurova_Hidromobil/labels", Cukurova_Hidromobil)

#ConvertYolo(commonPath + "EVA-Otonom/labels", EVA_Otonom)

#ConvertYolo(commonPath + "Feslegen/labels", Feslegen)

ConvertYolo(commonPath + "GTU/Dataset1/labels", GTU1)
ConvertYolo(commonPath + "GTU/Dataset2/labels", GTU1)

ConvertYolo(commonPath + "ITU-RacingDriverless/yoloLabels", ITU_RacingDriverless)

ConvertYolo(commonPath + "KU-AIRS-Spark/Dataset", KU_AIRS_Spark)

ConvertYolo(commonPath + "YTU-AESK/labels", YTU_AESK)

ConvertYolo(commonPath + "savhascelik/Labels-YOLO", savhascelik)

#ConvertYolo(commonPath + "Acar/labels", Acar)

#ConvertYolo(commonPath + "GobeklitepeOSAT/labels", GobeklitepeOSAT)

ConvertYolo(commonPath + "GumusArge/labels", GumusArge)

#ConvertYolo(commonPath + "ITU-GAE/labels", ITU_GAE)   Dataset classlarında hata var. 

# ConvertYolo(commonPath + "Kasva/gercekdata1-labels/labels", Kasva)
# ConvertYolo(commonPath + "Kasva/gercekdata2-labels/labels", Kasva)
# ConvertYolo(commonPath + "Kasva/sim_labels/labels", Kasva)

ConvertYolo(commonPath + "Kızıl-Elma/Etiketler", Kızıl_Elma)

ConvertYolo(commonPath + "RACLAB-Sigun/labels", RACLAB_Sigun)

# ConvertYolo(commonPath + "ROTA_Akdeniz/labels", ROTA_Akdeniz)

# ConvertYolo(commonPath + "RoTa_Marmara/labels", RoTaMarmara)  # Standart için klasör isminde boşluk, "_" ile değiştirildi.

# ConvertYolo(commonPath + "SUBU-AISET/labels", SUBU_AISET)  #Klasör ismindeki "Ü"  "U" olarak değiştirildi.

# ConvertYolo(commonPath + "TEAM-IMU/labels", TEAM_IMU)

# ConvertYolo(commonPath + "TTTechAuto/labels", TTTechAuto)

ConvertYolo(commonPath + "Yeditepe-Automotive/labels", Yeditepe_Automotive)

# ConvertYolo(commonPath + "YTU-Astrid/labels", YTU_Astrid)
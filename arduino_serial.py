import serial
import time

# 1. BAĞLANTIYI KUR
def connect_arduino() :
    print("Arduino'ya bağlanılıyor...")
    try:
        # COM11 portunu ve Arduino kodundaki aynı hız olan 9600 baud rate'i seçiyoruz
        arduino = serial.Serial('COM11', 9600, timeout=1)
        
        # ÇOK ÖNEMLİ: Seri port açıldığında Arduino kendini otomatik resetler.
        # Uyanması ve komut dinlemeye hazır hale gelmesi için 2 saniye beklemeliyiz.
        time.sleep(2) 
        print("Bağlantı Başarılı!")
        return arduino
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        print("Arduino'nun takılı olduğundan ve Seri Port Ekranı'nın kapalı olduğundan emin ol.")
        exit()

# 2. KOMUT GÖNDERME FONKSİYONU
def motora_aci_gonder(ListAngles, arduino):
    # Mesajı Arduino'nun beklediği "motor,açı\n" formatına çeviriyoruz
    length = len(ListAngles)
    for i in range (length):
        mesaj = f"{ListAngles[i]["motor_no"]},{ListAngles[i]["aci"]}\n"
        
    # Python string'leri doğrudan gönderemez, onları byte formatına çevirmeliyiz (encode)
        arduino.write(mesaj.encode('utf-8'))
        print(f"Gönderildi -> Motor: {ListAngles[i]["motor_no"]}, Açı: {ListAngles[i]["aci"]}")
        
        # İsteğe Bağlı: Arduino'nun işlemi yapıp yapmadığını teyit etmek için ondan gelen cevabı oku
        time.sleep(0.1) # Cevabın gelmesi için çok kısa bir süre tanı
        while arduino.in_waiting > 0:
            cevap = arduino.readline().decode('utf-8').strip()
            print(f"Arduino'dan Gelen Onay: {cevap}")

        time.sleep(1) 

# 3. TEST ZAMANI
# Motor 0'ı (taban motoru) 90 dereceye (merkeze) gönder
#motora_aci_gonder(0, 90)

# Motorun fiziksel olarak o noktaya gitmesi için biraz zaman tanı
time.sleep(1) 

# Şimdi aynı motoru 120 dereceye gönder
""" motora_aci_gonder(0, 120)
time.sleep(1) """

# İşimiz bittiğinde portu serbest bırakıyoruz
#arduino.close()
print("Bağlantı kapatıldı.")
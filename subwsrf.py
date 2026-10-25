class KarakterSurfer:
    def __init__(self, nama):
        self.nama = nama
        self.skor = 0
        self.koin = 0
        self.is_running = True

    def berlari(self):
        self.is_running = True
        print(self.nama, "mulai berlari!")

    def ambil_koin(self, jumlah):
        self.koin = self.koin + jumlah
        self.skor = self.skor + jumlah * 10
        print(self.nama, "mengambil", jumlah, "koin")

    def tabrak_rintangan(self):
        self.is_running = False
        print("GAME OVER! Kamu menabrak rintangan")

    def info_player(self):
        print("Nama   :", self.nama)
        print("Skor   :", self.skor)
        print("Koin   :", self.koin)
        print("Berlari:", self.is_running)


player1 = KarakterSurfer("Jake")
player1.berlari()
player1.ambil_koin(5)
player1.ambil_koin(3)
player1.info_player()
player1.tabrak_rintangan()
player1.info_player()
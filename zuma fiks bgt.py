import math
import random

import pygame


lebar, tinggi = 900, 700
fps = 60
radius = 18
jarak = radius * 2
pusat = (lebar // 2, tinggi // 2)

rush = 3.0
mundur = 6.0
push = 10.0
kpeluru = 14.0


Warna = {
    "Merah": (255, 148, 170),   
    "Hijau": (150, 224, 172),   
    "Biru": (144, 186, 255),    
    "Kuning": (255, 229, 140),  
    "Ungu": (206, 166, 244),    
}


ungkyu = (96, 62, 128)        
pita = (255, 140, 178)
piteu = (224, 96, 140)


def buat_jalur():
    cx, cy = pusat
    kasar = []

    for y in range(cy - 130, cy + 1, 2):
        kasar.append((cx + 400.0, float(y)))
    putaran = 2.6
    langkah = 4000
    for i in range(langkah + 1):
        t = i / langkah
        th = putaran * 2 * math.pi * t
        rx = 400 * (1 - t) + 135 * t
        ry = 300 * (1 - t) + 105 * t
        kasar.append((cx + rx * math.cos(th), cy + ry * math.sin(th)))

    jalur = [kasar[0]]
    target = 1.0
    akum = 0.0
    for i in range(1, len(kasar)):
        x0, y0 = kasar[i - 1]
        x1, y1 = kasar[i]
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg == 0:
            continue
        while akum + seg >= target:
            f = (target - akum) / seg
            jalur.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f))
            target += 1.0
        akum += seg
    return jalur


class Jalur:
    def __init__(self):
        self.titik = buat_jalur()
        self.panjang = len(self.titik) - 1

    def pos(self, d):
        i = max(0, min(self.panjang, int(d)))
        return self.titik[i]

    def arah(self, d):
        a = self.pos(d - 4)
        b = self.pos(d + 4)
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1.0
        return dx / n, dy / n
    
def gambar_bola(layar, nama, x, y, r=radius):
    w = Warna[nama]
    tepi = tuple(int(c * 0.66) for c in w)
    tengah = tuple(min(255, int(c * 0.5 + 130)) for c in w)
    x, y = int(x), int(y)
    pygame.draw.circle(layar, tepi, (x, y), r)
    pygame.draw.circle(layar, w, (x, y), max(1, r - 2))
    pygame.draw.circle(layar, tengah, (x - r // 6, y - r // 6), max(1, int(r * 0.62)))
    pygame.draw.circle(layar, (255, 255, 255), (x - r // 3, y - r // 3), max(1, r // 4))


class Bola:

    def __init__(self, Warna, d):
        self.Warna = Warna
        self.d = float(d)
        self.off_x = 0.0
        self.off_y = 0.0


class Peluru:
    def __init__(self, x, y, vx, vy, Warna):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.Warna = Warna


class kodokzumzum:

    def __init__(self, Warna_awal, Warna_berikut=None):

        self.Warna_peluru = Warna_awal
        self.skor = 0
        self.is_active = True

        self.Warna_berikut = Warna_berikut or Warna_awal
        self.sudut = -math.pi / 2
        self.gambar = None
        self.load_gambar(Warna_awal)

    def ganti_Warna(self, Warna_baru):
        self.Warna_peluru = Warna_baru
        self.load_gambar(Warna_baru)

    def load_gambar(self, Warna):
        ukuran = 120
        c = ukuran // 2
        img = pygame.Surface((ukuran, ukuran), pygame.SRCALPHA)

        ungu_tepi = (150, 110, 200)
        ungu_badan = (192, 158, 236)
        ungu_kepala = (214, 184, 248)
        ungu_bintik = (226, 204, 252)

        for sx in (-1, 1):
            belakang = pygame.Rect(c - 34, c + sx * 26 - 10, 30, 20)
            depan = pygame.Rect(c + 6, c + sx * 30 - 8, 26, 16)
            for rect in (belakang, depan):
                pygame.draw.ellipse(img, ungu_tepi, rect)
                pygame.draw.ellipse(img, ungu_badan, rect.inflate(-4, -4))


        pygame.draw.circle(img, ungu_tepi, (c - 4, c), 38)
        pygame.draw.circle(img, ungu_badan, (c - 4, c), 34)

        for bx, by, br in ((-22, -14, 5), (-24, 8, 4), (-12, 21, 4), (-30, -2, 3)):
            pygame.draw.circle(img, ungu_bintik, (c + bx, c + by), br)


        pygame.draw.circle(img, ungu_tepi, (c + 16, c), 26)
        pygame.draw.circle(img, ungu_kepala, (c + 16, c), 23)


        for sy in (-1, 1):
            pygame.draw.circle(img, (255, 170, 205), (c + 30, c + sy * 17), 4)

        for sy in (-1, 1):
            ex, ey = c + 18, c + sy * 16
            pygame.draw.circle(img, (255, 255, 255), (ex, ey), 8)
            pygame.draw.circle(img, (80, 52, 112), (ex + 1, ey), 6)
            pygame.draw.circle(img, (255, 255, 255), (ex + 3, ey - 2), 2)
            pygame.draw.circle(img, (255, 255, 255), (ex - 1, ey + 2), 1)


        gambar_bola(img, Warna, c + 36, c, 12)

        ekor_kiri = [(c, c - 2), (c - 14, c - 9), (c - 10, c + 1)]
        ekor_kanan = [(c, c + 2), (c - 14, c + 9), (c - 10, c - 1)]
        for ekor in (ekor_kiri, ekor_kanan):
            pygame.draw.polygon(img, pita, ekor)
            pygame.draw.polygon(img, piteu, ekor, 2)
        for s in (-1, 1):
            loop = pygame.Rect(0, 0, 17, 14)
            loop.center = (c + 1, c + s * 10)
            pygame.draw.ellipse(img, piteu, loop)
            pygame.draw.ellipse(img, pita, loop.inflate(-4, -4))
            pygame.draw.circle(img, (255, 205, 222), (loop.centerx - 2, loop.centery - 2), 2)
        pygame.draw.circle(img, piteu, (c + 1, c), 6)
        pygame.draw.circle(img, (255, 170, 200), (c + 1, c), 4)

        self.gambar = img

    def bidik(self, pos):
        self.sudut = math.atan2(pos[1] - pusat[1], pos[0] - pusat[0])

    def tukar_Warna(self):
        lama = self.Warna_peluru
        self.ganti_Warna(self.Warna_berikut)
        self.Warna_berikut = lama

    def dor(self, Warna_berikut_baru):
        if not self.is_active:
            return None
        ax, ay = math.cos(self.sudut), math.sin(self.sudut)
        peluru = Peluru(pusat[0] + ax * 46, pusat[1] + ay * 46,
                        ax * kpeluru, ay * kpeluru, self.Warna_peluru)
        self.ganti_Warna(self.Warna_berikut)
        self.Warna_berikut = Warna_berikut_baru
        return peluru

    def tambah_skor(self, poin):
        self.skor += poin

    def info_status(self):
        status = "Aktif" if self.is_active else "Tidak aktif"
        print(f"Warna peluru: {self.Warna_peluru}")
        print(f"Skor: {self.skor}")
        print(f"Status: {status}")


class playeuu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Zuma - Tugas OOP")
        self.layar = pygame.display.set_mode((lebar, tinggi))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.font_kecil = pygame.font.Font(None, 24)
        self.font_besar = pygame.font.Font(None, 76)

        self.jalur = Jalur()
        self.latar = self.buat_latar()
        self.overlay = pygame.Surface((lebar, tinggi), pygame.SRCALPHA)
        self.overlay.fill((96, 62, 128, 110))
        self.jalan = True
        self.restart()

    def buat_latar(self):
        s = pygame.Surface((lebar, tinggi))

        for y in range(tinggi):
            k = y / tinggi
            Warna = (int(255 - 41 * k), int(224 + 2 * k), int(238 + 17 * k))
            pygame.draw.line(s, Warna, (0, y), (lebar, y))

        rng = random.Random(7)
        hias = pygame.Surface((lebar, tinggi), pygame.SRCALPHA)
        for _ in range(38):
            pygame.draw.circle(hias, (255, 255, 255, 70),
                               (rng.randint(0, lebar), rng.randint(0, tinggi)),
                               rng.randint(6, 28))
        for _ in range(16):
            x, y, k = rng.randint(10, lebar - 10), rng.randint(10, tinggi - 10), rng.randint(5, 9)
            bintang = [(x, y - k), (x + k // 3, y - k // 3), (x + k, y), (x + k // 3, y + k // 3),
                       (x, y + k), (x - k // 3, y + k // 3), (x - k, y), (x - k // 3, y - k // 3)]
            pygame.draw.polygon(hias, (255, 255, 255, 190), bintang)
        s.blit(hias, (0, 0))

        t = self.jalur.titik
        for i in range(0, len(t), 3):
            pygame.draw.circle(s, (206, 172, 218), (int(t[i][0]), int(t[i][1])), radius + 9)
        for i in range(0, len(t), 3):
            pygame.draw.circle(s, (246, 236, 252), (int(t[i][0]), int(t[i][1])), radius + 5)

        pygame.draw.circle(s, (176, 138, 208), pusat, 68)
        pygame.draw.circle(s, (255, 242, 250), pusat, 64)
        pygame.draw.circle(s, (240, 224, 250), pusat, 56)

        for (hx, hy), rad in ((t[0], 30), (t[-1], 32)):
            pygame.draw.circle(s, (150, 112, 182), (int(hx), int(hy)), rad + 5)
            pygame.draw.circle(s, (92, 62, 124), (int(hx), int(hy)), rad)
            pygame.draw.circle(s, (70, 44, 100), (int(hx), int(hy)), rad - 8)
        return s

    def restart(self):
        self.katak = kodokzumzum("Merah")
        self.mulai_level(1)

    def mulai_level(self, level):
        self.level = level
        n_Warna = 4 if level == 1 else 5
        self.Warna_aktif = list(Warna.keys())[:n_Warna]
        self.sisa_spawn = min(30 + 8 * level, 80)
        self.kecepatan = min(0.55 + 0.08 * level, 1.3)
        self.rantai = []
        self.peluru = []
        self.partikel = []
        self.popup = []
        self.kombo = 1
        self.cooldown = 0
        self.status = "main"
        self.katak.is_active = True
        self.katak.ganti_Warna(random.choice(self.Warna_aktif))
        self.katak.Warna_berikut = random.choice(self.Warna_aktif)

    def Warna_tersedia(self):
        ada = {b.Warna for b in self.rantai}
        return sorted(ada) if ada else list(self.Warna_aktif)

    def Warna_baru_rantai(self):
        r = self.rantai
        while True:
            w = random.choice(self.Warna_aktif)
            if len(r) >= 2 and r[-1].Warna == r[-2].Warna == w:
                continue
            return w

    def sinkron_Warna(self):
        ada = self.Warna_tersedia()
        if self.katak.Warna_peluru not in ada:
            self.katak.ganti_Warna(random.choice(ada))
        if self.katak.Warna_berikut not in ada:
            self.katak.Warna_berikut = random.choice(ada)

    def tangani_event(self, e):
        if e.type == pygame.QUIT:
            self.jalan = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.jalan = False
            elif e.key == pygame.K_r:
                self.restart()
            elif e.key == pygame.K_SPACE and self.status == "main":
                self.katak.tukar_Warna()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if self.status == "main":
                if e.button == 1:
                    self.dor(e.pos)
                elif e.button == 3:
                    self.katak.tukar_Warna()
            elif self.status == "level_selesai":
                self.mulai_level(self.level + 1)
            elif self.status == "kalah":
                self.restart()

    def dor(self, pos):
        if self.cooldown > 0 or not self.katak.is_active:
            return
        self.katak.bidik(pos)
        p = self.katak.dor(random.choice(self.Warna_tersedia()))
        if p:
            self.peluru.append(p)
            self.cooldown = 10

    def posisi_bola(self, b):
        x, y = self.jalur.pos(b.d)
        return x + b.off_x, y + b.off_y

    def terhubung(self, i):

        return self.rantai[i].d - self.rantai[i + 1].d <= jarak + 2

    def update_rantai(self):
        r = self.rantai

        while self.sisa_spawn > 0 and (not r or r[-1].d >= 0):
            d = 0.0 if not r else r[-1].d - jarak
            r.append(Bola(self.Warna_baru_rantai(), d))
            self.sisa_spawn -= 1

        if not r:
            return

        lama = [b.d for b in r]
        n = len(r)
        kec = self.kecepatan if self.sisa_spawn == 0 else rush

        segmen = []
        awal = 0
        for i in range(1, n):
            if lama[i - 1] - lama[i] - jarak > 1.0:
                segmen.append((awal, i - 1))
                awal = i
        segmen.append((awal, n - 1))

        temu = []

        a, z = segmen[-1]
        for i in range(a, z + 1):
            r[i].d = lama[i] + kec

        for s in range(len(segmen) - 2, -1, -1):
            a, z = segmen[s]
            a_belakang = segmen[s + 1][0]
            celah = lama[z] - r[a_belakang].d - jarak
            if celah <= mundur:
                m = -max(celah, 0.0)
                temu.append(a_belakang)
            else:
                m = -mundur
            for i in range(a, z + 1):
                r[i].d = lama[i] + m

        for i in range(n - 2, -1, -1):
            butuh = r[i + 1].d + jarak
            if r[i].d < butuh:
                r[i].d = min(butuh, r[i].d + push)

        for b in r:
            b.off_x *= 0.78
            b.off_y *= 0.78
            if abs(b.off_x) < 0.5:
                b.off_x = 0.0
            if abs(b.off_y) < 0.5:
                b.off_y = 0.0

        for a in sorted(temu, reverse=True):
            if 0 < a < len(r) and r[a - 1].Warna == r[a].Warna:
                self.cek_cocok(a, lanjutan=True)

    def cek_cocok(self, idx, lanjutan=False):
        r = self.rantai
        Warna = r[idx].Warna
        kiri = idx
        while kiri > 0 and r[kiri - 1].Warna == Warna and self.terhubung(kiri - 1):
            kiri -= 1
        kanan = idx
        while kanan < len(r) - 1 and r[kanan + 1].Warna == Warna and self.terhubung(kanan):
            kanan += 1
        jumlah = kanan - kiri + 1
        if jumlah < 3:
            return False

        if lanjutan:
            self.kombo += 1
        poin = jumlah * 10 * self.kombo + (jumlah - 3) * 15

        px = py = 0.0
        for b in r[kiri:kanan + 1]:
            x, y = self.posisi_bola(b)
            px += x
            py += y
            for _ in range(5):
                ang = random.uniform(0, 2 * math.pi)
                sp = random.uniform(1.0, 4.0)
                self.partikel.append([x, y, math.cos(ang) * sp, math.sin(ang) * sp,
                                      random.randint(18, 32), b.Warna])
        del r[kiri:kanan + 1]

        self.katak.tambah_skor(poin)
        teks = f"+{poin}" if self.kombo == 1 else f"+{poin}  KOMBO x{self.kombo}"
        self.popup.append([px / jumlah, py / jumlah, teks, 55])
        return True

    def cari_tabrakan(self, p):
        terbaik = None
        jarak_min = (jarak - 4) ** 2
        for j, b in enumerate(self.rantai):
            if b.d < 0:
                continue
            bx, by = self.posisi_bola(b)
            dd = (bx - p.x) ** 2 + (by - p.y) ** 2
            if dd < jarak_min:
                jarak_min = dd
                terbaik = j
        return terbaik

    def sisipkan(self, p, j):
        r = self.rantai
        b = r[j]
        bx, by = self.jalur.pos(b.d)
        tx, ty = self.jalur.arah(b.d)
        depan = (p.x - bx) * tx + (p.y - by) * ty > 0
        k = j if depan else j + 1

        if k < len(r):
            d_baru = r[k].d + jarak
        else:
            d_baru = r[k - 1].d - jarak

        px, py = self.jalur.pos(d_baru)
        bola = Bola(p.Warna, d_baru)
        bola.off_x = p.x - px
        bola.off_y = p.y - py
        r.insert(k, bola)

        self.kombo = 1
        self.cek_cocok(k)
        self.sinkron_Warna()

    def update_peluru(self):
        for p in self.peluru[:]:
            p.x += p.vx
            p.y += p.vy
            if p.x < -60 or p.x > lebar + 60 or p.y < -60 or p.y > tinggi + 60:
                self.peluru.remove(p)
                continue
            kena = self.cari_tabrakan(p)
            if kena is not None:
                self.peluru.remove(p)
                self.sisipkan(p, kena)

    def update_efek(self):
        for q in self.partikel[:]:
            q[0] += q[2]
            q[1] += q[3]
            q[3] += 0.15
            q[4] -= 1
            if q[4] <= 0:
                self.partikel.remove(q)
        for t in self.popup[:]:
            t[1] -= 0.8
            t[3] -= 1
            if t[3] <= 0:
                self.popup.remove(t)

    def update(self):
        if self.status != "main":
            self.update_efek()
            return
        if self.cooldown > 0:
            self.cooldown -= 1

        self.update_rantai()
        self.update_peluru()
        self.update_efek()

        if self.rantai:
            if self.rantai[0].d >= self.jalur.panjang - 2:
                self.status = "kalah"
                self.katak.is_active = False
                print("=== GAME OVER ===")
                self.katak.info_status()
        elif self.sisa_spawn == 0:
            self.status = "level_selesai"
            self.katak.tambah_skor(100 * self.level)
            print(f"=== LEVEL {self.level} SELESAI ===")
            self.katak.info_status()

    def tulis(self, teks, pos, font, Warna, bayang, anchor="center", off=2):
        img = font.render(teks, True, Warna)
        sh = font.render(teks, True, bayang)
        rect = img.get_rect(**{anchor: pos})
        self.layar.blit(sh, rect.move(off, off))
        self.layar.blit(img, rect)

    def teks_tengah(self, teks, y, font, Warna=(255, 255, 255)):
        self.tulis(teks, (lebar // 2, y), font, Warna, ungkyu, off=3)

    def gambar(self):
        self.layar.blit(self.latar, (0, 0))

        for b in self.rantai:
            if b.d >= 0:
                x, y = self.posisi_bola(b)
                gambar_bola(self.layar, b.Warna, x, y)

        for p in self.peluru:
            gambar_bola(self.layar, p.Warna, p.x, p.y)

        if self.status == "main":
            ax, ay = math.cos(self.katak.sudut), math.sin(self.katak.sudut)
            for k in range(70, 300, 18):
                pygame.draw.circle(self.layar, (255, 255, 255),
                                   (int(pusat[0] + ax * k), int(pusat[1] + ay * k)), 4)
                pygame.draw.circle(self.layar, (178, 140, 214),
                                   (int(pusat[0] + ax * k), int(pusat[1] + ay * k)), 2)

        img = pygame.transform.rotate(self.katak.gambar, -math.degrees(self.katak.sudut))
        self.layar.blit(img, img.get_rect(center=pusat))

        for q in self.partikel:
            pygame.draw.circle(self.layar, Warna[q[5]], (int(q[0]), int(q[1])),
                               max(1, q[4] // 8))
        for t in self.popup:
            self.tulis(t[2], (int(t[0]), int(t[1])), self.font, (255, 110, 160), (255, 255, 255))

        sisa = len(self.rantai) + self.sisa_spawn
        hud = [f"Skor: {self.katak.skor}", f"Level: {self.level}", f"Bola: {sisa}"]
        for i, h in enumerate(hud):
            self.tulis(h, (14, 12 + i * 28), self.font, ungkyu, (255, 255, 255), anchor="topleft")
        self.tulis("Berikut:", (14, tinggi - 52), self.font_kecil, ungkyu, (255, 255, 255),
                   anchor="topleft", off=1)
        gambar_bola(self.layar, self.katak.Warna_berikut, 96, tinggi - 42, 13)
        self.tulis("Klik kiri: lempar | Klik kanan/Spasi: tukar",
                   (lebar - 14, tinggi - 14), self.font_kecil, ungkyu, (255, 255, 255),
                   anchor="bottomright", off=1)

        if self.status != "main":
            self.layar.blit(self.overlay, (0, 0))

        if self.status == "level_selesai":
            self.teks_tengah(f"LEVEL {self.level} SELESAI!", tinggi // 2 - 150,
                             self.font_besar, (255, 238, 140))
            self.teks_tengah("Klik untuk lanjut ke level berikutnya", tinggi // 2 - 100, self.font)
        elif self.status == "kalah":
            self.teks_tengah("GAME OVER", tinggi // 2 - 150, self.font_besar, (255, 160, 184))
            self.teks_tengah(f"Skor akhir: {self.katak.skor}", tinggi // 2 - 100, self.font)
            self.teks_tengah("Klik atau tekan R untuk main lagi", tinggi // 2 - 70, self.font)

        pygame.display.flip()

    def jalankan(self):
        while self.jalan:
            for e in pygame.event.get():
                self.tangani_event(e)
            if self.status == "main":
                self.katak.bidik(pygame.mouse.get_pos())
            self.update()
            self.gambar()
            self.clock.tick(fps)
        pygame.quit()


def main():
    playeuu().jalankan()


if __name__ == "__main__":
    main()

"""
models.py
Berisi semua class untuk Sistem Penghitung IPK.

Konsep OOP yang dipakai:
1. Class & Object          -> MataKuliah, NilaiMatkul, Mahasiswa, SistemIPK
2. Constructor (__init__)  -> semua class
3. Encapsulation           -> atribut private (_sks, _nilai_angka) + property
4. Property (getter/setter)-> sks, nilai_angka, nama
5. Abstraction             -> class abstrak Orang (ABC + abstractmethod)
6. Inheritance (pewarisan) -> Mahasiswa(Orang), MahasiswaBeasiswa(Mahasiswa)
7. Polymorphism/Overriding -> peran() dan status_akademik()
8. Class method            -> Mahasiswa.dari_string()
9. Static method           -> NilaiMatkul.konversi()
10. Class variable         -> MataKuliah.total_matkul
11. Magic method           -> __str__, __repr__, __eq__, __lt__
12. Composition            -> Mahasiswa punya banyak NilaiMatkul
13. Custom Exception       -> NilaiTidakValidError
"""
from abc import ABC, abstractmethod


# ---------- Custom Exception ----------
class NilaiTidakValidError(Exception):
    """Dipanggil jika nilai di luar rentang 0 - 100."""
    pass


# ---------- Class Mata Kuliah ----------
class MataKuliah:
    total_matkul = 0  # class variable (dipakai bersama semua object)

    def __init__(self, kode, nama, sks):
        self.kode = kode
        self.nama = nama
        self.sks = sks  # otomatis lewat setter (validasi)
        MataKuliah.total_matkul += 1

    @property
    def sks(self):
        return self._sks

    @sks.setter
    def sks(self, nilai):
        if nilai <= 0:
            raise ValueError("SKS harus lebih dari 0")
        self._sks = nilai

    def __str__(self):
        return f"{self.kode} - {self.nama} ({self.sks} SKS)"


# ---------- Class Nilai Mata Kuliah (Composition) ----------
class NilaiMatkul:
    def __init__(self, matkul, nilai_angka):
        self.matkul = matkul              # object MataKuliah
        self.nilai_angka = nilai_angka    # lewat setter (validasi)

    @property
    def nilai_angka(self):
        return self._nilai_angka

    @nilai_angka.setter
    def nilai_angka(self, nilai):
        if not 0 <= nilai <= 100:
            raise NilaiTidakValidError("Nilai harus antara 0 sampai 100")
        self._nilai_angka = nilai

    @staticmethod
    def konversi(nilai_angka):
        """Mengubah nilai angka menjadi (huruf, bobot)."""
        if nilai_angka >= 80:
            return "A", 4.0
        elif nilai_angka >= 70:
            return "B", 3.0
        elif nilai_angka >= 60:
            return "C", 2.0
        elif nilai_angka >= 50:
            return "D", 1.0
        return "E", 0.0

    @property
    def nilai_huruf(self):
        return self.konversi(self._nilai_angka)[0]

    @property
    def bobot(self):
        return self.konversi(self._nilai_angka)[1]

    @property
    def mutu(self):
        """Mutu = bobot x SKS."""
        return self.bobot * self.matkul.sks


# ---------- Abstract Class ----------
class Orang(ABC):
    def __init__(self, nama):
        self._nama = nama

    @property
    def nama(self):
        return self._nama

    @abstractmethod
    def peran(self):
        """Wajib di-override oleh class turunan."""
        pass


# ---------- Class Mahasiswa (Inheritance) ----------
class Mahasiswa(Orang):
    def __init__(self, nama, nim, semester):
        super().__init__(nama)
        self.nim = nim
        self.semester = semester
        self.daftar_nilai = []  # list berisi object NilaiMatkul

    def peran(self):  # overriding
        return "Mahasiswa Reguler"

    def tambah_nilai(self, matkul, nilai_angka):
        self.daftar_nilai.append(NilaiMatkul(matkul, nilai_angka))

    def total_sks(self):
        return sum(n.matkul.sks for n in self.daftar_nilai)

    def hitung_ipk(self):
        total_sks = self.total_sks()
        if total_sks == 0:
            return 0.0
        total_mutu = sum(n.mutu for n in self.daftar_nilai)
        return total_mutu / total_sks

    def predikat(self):
        ipk = self.hitung_ipk()
        if ipk >= 3.51:
            return "Dengan Pujian (Cum Laude)"
        elif ipk >= 3.00:
            return "Sangat Memuaskan"
        elif ipk >= 2.50:
            return "Memuaskan"
        return "Cukup"

    def status_akademik(self):
        return "Aman" if self.hitung_ipk() >= 2.0 else "Peringatan Akademik"

    @classmethod
    def dari_string(cls, teks):
        """Buat object dari string 'nama,nim,semester'."""
        nama, nim, semester = teks.split(",")
        return cls(nama.strip(), nim.strip(), int(semester))

    # ----- magic methods -----
    def __str__(self):
        return f"{self.nama} ({self.nim}) - Semester {self.semester}"

    def __repr__(self):
        return f"Mahasiswa('{self.nama}', '{self.nim}', {self.semester})"

    def __eq__(self, other):
        return isinstance(other, Mahasiswa) and self.nim == other.nim

    def __lt__(self, other):
        return self.hitung_ipk() < other.hitung_ipk()


class MahasiswaBeasiswa(Mahasiswa):
    def __init__(self, nama, nim, semester, ipk_minimum=3.5):
        super().__init__(nama, nim, semester)
        self.ipk_minimum = ipk_minimum

    def peran(self):  # overriding
        return "Mahasiswa Beasiswa"

    def status_akademik(self):  # overriding (polymorphism)
        if self.hitung_ipk() >= self.ipk_minimum:
            return "Beasiswa Aman"
        return f"Beasiswa Terancam (IPK minimal {self.ipk_minimum})"


# ---------- Class Pengelola ----------
class SistemIPK:
    def __init__(self):
        self.daftar_mahasiswa = []

    def tambah_mahasiswa(self, mhs):
        if mhs in self.daftar_mahasiswa:  # memakai __eq__
            raise ValueError(f"NIM {mhs.nim} sudah terdaftar")
        self.daftar_mahasiswa.append(mhs)

    def cari(self, nim):
        for mhs in self.daftar_mahasiswa:
            if mhs.nim == nim:
                return mhs
        return None

    def ranking(self):
        return sorted(self.daftar_mahasiswa, reverse=True)  # memakai __lt__

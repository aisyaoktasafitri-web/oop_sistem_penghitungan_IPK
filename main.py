"""main.py - Program utama Sistem Penghitung IPK (menu berbasis teks)."""
from models import (MataKuliah, Mahasiswa, MahasiswaBeasiswa,
                    SistemIPK, NilaiTidakValidError)


def input_angka(pesan, tipe=int):
    while True:
        try:
            return tipe(input(pesan))
        except ValueError:
            print("  [!] Input harus berupa angka, coba lagi.")


def tambah_mahasiswa(sistem):
    print("\n--- Tambah Mahasiswa ---")
    nama = input("Nama     : ")
    nim = input("NIM      : ")
    semester = input_angka("Semester : ")
    jenis = input("Beasiswa? (y/n) : ").lower()
    if jenis == "y":
        mhs = MahasiswaBeasiswa(nama, nim, semester)
    else:
        mhs = Mahasiswa.dari_string(f"{nama},{nim},{semester}")
    try:
        sistem.tambah_mahasiswa(mhs)
        print(f"Berhasil menambahkan: {mhs}")
    except ValueError as e:
        print(f"[!] {e}")


def input_nilai(sistem):
    print("\n--- Input Nilai ---")
    mhs = sistem.cari(input("NIM mahasiswa : "))
    if mhs is None:
        print("[!] Mahasiswa tidak ditemukan.")
        return
    jumlah = input_angka("Jumlah mata kuliah : ")
    for i in range(1, jumlah + 1):
        print(f"\nMata kuliah ke-{i}")
        kode = input("  Kode : ")
        nama = input("  Nama : ")
        try:
            sks = input_angka("  SKS  : ")
            nilai = input_angka("  Nilai (0-100) : ", float)
            mhs.tambah_nilai(MataKuliah(kode, nama, sks), nilai)
        except (ValueError, NilaiTidakValidError) as e:
            print(f"  [!] Gagal: {e}")


def lihat_transkrip(sistem):
    print("\n--- Transkrip ---")
    mhs = sistem.cari(input("NIM mahasiswa : "))
    if mhs is None:
        print("[!] Mahasiswa tidak ditemukan.")
        return
    print(f"\n{mhs}  [{mhs.peran()}]")
    print("-" * 60)
    print(f"{'Mata Kuliah':<28}{'SKS':<5}{'Nilai':<8}{'Huruf':<7}{'Bobot'}")
    for n in mhs.daftar_nilai:
        print(f"{n.matkul.nama:<28}{n.matkul.sks:<5}"
              f"{n.nilai_angka:<8}{n.nilai_huruf:<7}{n.bobot}")
    print("-" * 60)
    print(f"Total SKS : {mhs.total_sks()}")
    print(f"IPK       : {mhs.hitung_ipk():.2f}")
    print(f"Predikat  : {mhs.predikat()}")
    print(f"Status    : {mhs.status_akademik()}")


def lihat_ranking(sistem):
    print("\n--- Ranking Mahasiswa berdasarkan IPK ---")
    if not sistem.daftar_mahasiswa:
        print("Belum ada data.")
        return
    for i, mhs in enumerate(sistem.ranking(), start=1):
        print(f"{i}. {mhs.nama:<20} IPK {mhs.hitung_ipk():.2f}  ({mhs.status_akademik()})")


def main():
    sistem = SistemIPK()
    menu = {"1": tambah_mahasiswa, "2": input_nilai,
            "3": lihat_transkrip, "4": lihat_ranking}
    while True:
        print("\n=== SISTEM PENGHITUNG IPK ===")
        print("1. Tambah Mahasiswa")
        print("2. Input Nilai")
        print("3. Lihat Transkrip & IPK")
        print("4. Ranking IPK")
        print("0. Keluar")
        pilihan = input("Pilih menu : ")
        if pilihan == "0":
            print("Terima kasih!")
            break
        aksi = menu.get(pilihan)
        if aksi:
            aksi(sistem)
        else:
            print("[!] Menu tidak valid.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Aplikasi CLI Manajemen Keuangan Sederhana
- Bahasa: Python (standar library saja)
- Fitur: tambah pemasukan, tambah pengeluaran, lihat saldo, lihat riwayat transaksi
- Penyimpanan: file JSON (`data.json`)

Nama fungsi penting (bahasa Indonesia):
- tambah_pemasukan()
- tambah_pengeluaran()
- lihat_saldo()
- lihat_riwayat()

Kodenya ditulis sederhana dan diberi komentar singkat agar mudah dipahami pemula.
"""

import json
import os
from datetime import datetime
import sys

# ----- Konstanta file -----
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# ----- Warna (ANSI escape codes) -----
RESET = "\033[0m"
BOLD = "\033[1m"
FG_GREEN = "\033[32m"
FG_CYAN = "\033[36m"
FG_YELLOW = "\033[33m"
FG_RED = "\033[31m"
FG_MAGENTA = "\033[35m"
FG_BLUE = "\033[34m"

# ----- Utility sederhana -----

def format_rupiah(n):
    """Format angka menjadi string rupiah dengan pemisah ribuan."""
    try:
        n = float(n)
    except Exception:
        return str(n)
    # Jika bilangan bulat tampil tanpa desimal
    if n.is_integer():
        return f"Rp {int(n):,}".replace(",", ".")
    return f"Rp {n:,.2f}".replace(",", "~").replace(".", ",").replace("~", ".")


def clear_screen():
    """Membersihkan terminal (portabel sederhana)."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ----- Penyimpanan data -----

def load_data():
    """Membaca data dari `data.json`. Jika tidak ada, buat data awal."""
    if not os.path.exists(DATA_FILE):
        data_awal = {"saldo": 0, "riwayat": []}
        save_data(data_awal)
        return data_awal
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Jika file korup atau tidak bisa dibaca, backup dan buat data baru
        try:
            os.rename(DATA_FILE, DATA_FILE + ".bak")
        except Exception:
            pass
        data_awal = {"saldo": 0, "riwayat": []}
        save_data(data_awal)
        return data_awal


def save_data(data):
    """Menyimpan data ke `data.json` secara rapi."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ----- Fitur utama -----

def tambah_pemasukan(data):
    """Menambahkan pemasukan: minta jumlah dan keterangan, simpan ke riwayat."""
    print(FG_CYAN + BOLD + "\nTambah Pemasukan 💰" + RESET)
    try:
        jumlah_str = input("Masukkan jumlah pemasukan (angka): ").strip().replace('.', '').replace(',', '.')
        jumlah = float(jumlah_str)
    except ValueError:
        print(FG_RED + "Input tidak valid. Pastikan Anda memasukkan angka." + RESET)
        return
    if jumlah <= 0:
        print(FG_RED + "Jumlah harus lebih besar dari 0." + RESET)
        return
    keterangan = input("Keterangan (misal: gaji, bonus): ").strip() or "(Tanpa keterangan)"

    # Tambahkan ke saldo dan riwayat
    data["saldo"] = float(data.get("saldo", 0)) + jumlah
    transaksi = {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jenis": "Pemasukan",
        "jumlah": jumlah,
        "keterangan": keterangan,
    }
    data["riwayat"].append(transaksi)
    save_data(data)

    print(FG_GREEN + "✅ Pemasukan berhasil ditambahkan! " + RESET + "🎉")
    print("- Jumlah:", format_rupiah(jumlah), "| Keterangan:", keterangan)


def tambah_pengeluaran(data):
    """Menambahkan pengeluaran: minta jumlah dan keterangan, cek saldo, simpan jika cukup."""
    print(FG_CYAN + BOLD + "\nTambah Pengeluaran 🧾" + RESET)
    try:
        jumlah_str = input("Masukkan jumlah pengeluaran (angka): ").strip().replace('.', '').replace(',', '.')
        jumlah = float(jumlah_str)
    except ValueError:
        print(FG_RED + "Input tidak valid. Pastikan Anda memasukkan angka." + RESET)
        return
    if jumlah <= 0:
        print(FG_RED + "Jumlah harus lebih besar dari 0." + RESET)
        return
    keterangan = input("Keterangan (misal: makan, transport): ").strip() or "(Tanpa keterangan)"

    saldo_sekarang = float(data.get("saldo", 0))
    if jumlah > saldo_sekarang:
        print(FG_YELLOW + "⚠️  Saldo tidak mencukupi. Transaksi dibatalkan." + RESET)
        print("Saldo saat ini:", format_rupiah(saldo_sekarang))
        return

    # Kurangi saldo dan simpan transaksi
    data["saldo"] = saldo_sekarang - jumlah
    transaksi = {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jenis": "Pengeluaran",
        "jumlah": jumlah,
        "keterangan": keterangan,
    }
    data["riwayat"].append(transaksi)
    save_data(data)

    print(FG_GREEN + "✅ Pengeluaran berhasil dicatat!" + RESET)
    print("- Jumlah:", format_rupiah(jumlah), "| Keterangan:", keterangan)


def lihat_saldo(data):
    """Menampilkan saldo beserta tabel transaksi (pemasukan & pengeluaran)."""
    clear_screen()
    print(FG_MAGENTA + BOLD + "= Laporan Saldo =" + RESET)
    print("-" * 80)

    riwayat = data.get("riwayat", [])

    # Header tabel: Tanggal | Pemasukan | Pengeluaran | Keterangan
    headers = ["📅 Tanggal", "💸 Pemasukan", "💧 Pengeluaran", "📝 Keterangan"]
    widths = [19, 18, 18, 29]
    header_line = f"{BOLD}{FG_CYAN}{headers[0]:<{widths[0]}}{headers[1]:>{widths[1]}}{headers[2]:>{widths[2]}}  {headers[3]:<{widths[3]}}{RESET}"
    print(header_line)
    print("-" * 80)

    if not riwayat:
        print(FG_YELLOW + "(Belum ada transaksi)" + RESET)
    else:
        for it in riwayat:
            tanggal = it.get("tanggal", "-")
            jenis = it.get("jenis", "-")
            jumlah = it.get("jumlah", 0)
            ket = it.get("keterangan", "-")

            # Potong keterangan agar tidak pecah tabel
            if len(ket) > widths[3]:
                ket = ket[: widths[3] - 3] + "..."

            # Siapkan teks tanpa warna dengan padding agar alignment konsisten
            if jenis.lower().startswith("pemasukan"):
                pemasukan_plain = format_rupiah(jumlah)
                pengeluaran_plain = ""
            else:
                pemasukan_plain = ""
                pengeluaran_plain = "-" + format_rupiah(jumlah)

            pemasukan_cell = f"{pemasukan_plain:>{widths[1]}}"
            pengeluaran_cell = f"{pengeluaran_plain:>{widths[2]}}"

            # Balut dengan warna jika ada nilai
            if pemasukan_plain:
                pemasukan_cell = FG_GREEN + pemasukan_cell + RESET
            if pengeluaran_plain:
                pengeluaran_cell = FG_RED + pengeluaran_cell + RESET

            print(f"{tanggal:<{widths[0]}}{pemasukan_cell}{pengeluaran_cell}  {ket:<{widths[3]}}")

    print("-" * 80)

    # Tampilkan jumlah saldo di bawah tabel
    saldo_sekarang = data.get("saldo", 0)
    print("\n" + FG_MAGENTA + BOLD + "Jumlah Saldo:" + RESET + " "+ FG_GREEN + BOLD + f"{format_rupiah(saldo_sekarang)} 💵" + RESET)
    print("\n")


def lihat_riwayat(data):
    """Menampilkan riwayat transaksi dalam bentuk tabel dengan warna dan emoji."""
    riwayat = data.get("riwayat", [])
    print(FG_BLUE + BOLD + "\n📋 Riwayat Transaksi" + RESET)
    print("-" * 80)

    # Header tabel
    headers = ["📅 Tanggal", "🔁 Jenis", "💰 Jumlah", "📝 Keterangan"]
    widths = [19, 12, 18, 29]  # lebar kolom
    header_line = (
        f"{BOLD}{FG_CYAN}{headers[0]:<{widths[0]}}{headers[1]:<{widths[1]}}{headers[2]:>{widths[2]}}  {headers[3]:<{widths[3]}}{RESET}"
    )
    print(header_line)
    print("-" * 80)

    if not riwayat:
        print(FG_YELLOW + "(Belum ada transaksi)" + RESET)
        return

    # Tampilkan baris-baris riwayat
    for it in riwayat:
        tanggal = it.get("tanggal", "-")
        jenis = it.get("jenis", "-")
        jumlah = it.get("jumlah", 0)
        ket = it.get("keterangan", "-")
        jumlah_str = format_rupiah(jumlah)
        # Potong keterangan agar tidak pecah tabel
        if len(ket) > widths[3]:
            ket = ket[: widths[3] - 3] + "..."
        # Warna berdasarkan jenis
        warna = FG_GREEN if jenis.lower().startswith("pemasukan") else FG_RED
        print(f"{tanggal:<{widths[0]}}{jenis:<{widths[1]}}{warna}{jumlah_str:>{widths[2]}}{RESET}  {ket:<{widths[3]}}")

    print("-" * 80)


# ----- Menu utama -----

def tampilkan_menu():
    """Menampilkan menu utama dalam bentuk table sederhana."""
    clear_screen()
    print(BOLD + FG_MAGENTA + "\n✨ APLIKASI PENGELOLA UANG SEDERHANA ✨" + RESET)
    print("=" * 40)
    print(FG_CYAN + "Pilih opsi berikut (masukkan angka):" + RESET)
    print(FG_BLUE + "1.)" + RESET + " ➕ Tambah Pemasukan")
    print(FG_BLUE + "2.)" + RESET + " ➖ Tambah Pengeluaran")
    print(FG_BLUE + "3.)" + RESET + " 💳 Lihat Saldo")
    print(FG_BLUE + "4.)" + RESET + " 📋 Lihat Riwayat Transaksi")
    print(FG_BLUE + "5.)" + RESET + " ❌ Keluar" + "\n")


def main():
    """Loop utama program."""
    data = load_data()

    while True:
        tampilkan_menu()
        pilihan = input("Masukkan pilihan: ").strip()
        if pilihan == "1":
            tambah_pemasukan(data)
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "2":
            tambah_pengeluaran(data)
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "3":
            lihat_saldo(data)
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "4":
            lihat_riwayat(data)
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "5":
            print(FG_GREEN + "\nTerima kasih! Sampai jumpa 👋" + RESET)
            save_data(data)
            sys.exit(0)
        else:
            print(FG_YELLOW + "Pilihan tidak dikenali. Silakan pilih 1-5." + RESET)
            input("Tekan Enter untuk kembali ke menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + FG_GREEN + "Keluar. Data telah disimpan. Sampai jumpa! 👋" + RESET)
        # Pastikan data tersimpan
        # (data kemungkinan belum terdefinisi jika keluar sebelum load)
        try:
            save_data(load_data())
        except Exception:
            pass
        sys.exit(0)

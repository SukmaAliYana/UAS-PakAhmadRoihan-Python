import os

kontak_list = []

def tampilkan_menu():
    print("\n--- Pengelola Kontak Sederhana ---")
    print("1. Tambah Kontak")
    print("2. Tampilkan Kontak")
    print("3. Cari Kontak")
    print("4. Edit Kontak")
    print("5. Hapus Kontak")
    print("6. Keluar")

def tambah_kontak():
    nama = input("Masukkan nama: ")
    nomor = input("Masukkan nomor telepon: ")
    email = input("Masukkan email: ")
    
    kontak = {"nama": nama, "nomor": nomor, "email": email}
    kontak_list.append(kontak)
    simpan_data()

def tampilkan_kontak():
    if not kontak_list:
        print("Tidak ada kontak yang tersimpan.")
        return
    for kontak in kontak_list:
        print(f"Nama: {kontak['nama']}, Nomor: {kontak['nomor']}, Email: {kontak['email']}")


def cari_kontak(nama, index=0):
    if index >= len(kontak_list):
        print("Kontak tidak ditemukan.")
        return

    if kontak_list[index]["nama"].lower() == nama.lower():
        print(f"Ditemukan: Nama: {kontak_list[index]['nama']}, Nomor: {kontak_list[index]['nomor']}, Email: {kontak_list[index]['email']}")
    else:
        cari_kontak(nama, index + 1) 


def edit_kontak():
    nama = input("Masukkan nama kontak yang ingin diedit: ")
    for kontak in kontak_list:
        if kontak["nama"].lower() == nama.lower():
            print(f"Kontak ditemukan: {kontak}")
            kontak["nomor"] = input("Masukkan nomor telepon baru: ")
            kontak["email"] = input("Masukkan email baru: ")
            simpan_data()
            print("Kontak berhasil diperbarui.")
            return
    print("Kontak tidak ditemukan.")


def hapus_kontak():
    nama = input("Masukkan nama kontak yang ingin dihapus: ")
    for i, kontak in enumerate(kontak_list):
        if kontak["nama"].lower() == nama.lower():
            del kontak_list[i]
            simpan_data()
            print(f"Kontak {nama} berhasil dihapus.")
            return
    print("Kontak tidak ditemukan.")


def simpan_data():
    with open("kontak.txt", "w") as file:
        for kontak in kontak_list:
            file.write(f"{kontak['nama']},{kontak['nomor']},{kontak['email']}\n")

def baca_data():
    if os.path.exists("kontak.txt"):
        with open("kontak.txt", "r") as file:
            for line in file:
                nama, nomor, email = line.strip().split(",")
                kontak_list.append({"nama": nama, "nomor": nomor, "email": email})


def main():
    baca_data()
    while True:
        tampilkan_menu()
        pilihan = input("Pilih opsi: ")
        
        if pilihan == "1":
            tambah_kontak()
        elif pilihan == "2":
            tampilkan_kontak()
        elif pilihan == "3":
            nama = input("Masukkan nama yang dicari: ")
            cari_kontak(nama)
        elif pilihan == "4":
            edit_kontak()
        elif pilihan == "5":
            hapus_kontak()
        elif pilihan == "6":
            print("Keluar dari aplikasi...")
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
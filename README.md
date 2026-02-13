# Tugas Kecil 1 IF2211 Strategi Algoritma - Penyelesaian Queens LinkedIn

Program Penyelesaian Permainan Queens Linkedin menggunakan Algoritma Brute Force

## Deskripsi Program
Program ini bertujuan untuk menyelesaikan permainan logika Queens yang sedag populer di LinkedIn. Tujuan utama permainan ini adalah dengan menempatkan N buah Queen pada papan berwarna (dengan jumlah N warna) berukuran N x N dengan aturan sebagai berikut.
1. Hanya ada satu Queen per baris, kolom, dan daerah warna.
2. Queen tidak boleh saling bersentuhan, walau secara diagonal.

Program menggunakan algoritma Brute Force juga backtracking murni tanpa heuristik untuk mencari solusi dari papan yang menerima masukan input file ".txt". Program juga memiliki vitur GUI dan juga pengukuran waktu eksekusi dan total kasus yang dicoba.

## Struktur Folder
Struktur direktori repository ini adalah sebagai berikut.
```text
Tucil1_NIM/
├── doc/                # Laporan Tugas Kecil
├── src/                # Source code program
│   ├── main.py         # Program Utama
│   └── gui.py          # Program GUI
├── test/               # Solusi jawaban dari data uji
│   ├── test_A.txt
│   ├── test_B.txt
│   └── solution_test.txt
└── README.md           # Penjelasan program
```

## Requirement
Program ditulis menggunakan bahasa Python. Berikut adalah persyaratan sistem.
1. OS: Windows atau Linux.
2. Bahasa Pemrograman: Python 3
3. Library:
   a. os: Manajemen file dan pembersihan layar terminal untuk Update.
   b. time: Pengukuran waktu eksekusi dan delay visualisasi Update.
   c. tkinter: Antarmuka Pengguna Grafis (GUI)
   d. Pillow (PIL): Fitur menyimpan solusi dalam format gambar, berikut cara instalasi.
      ```bash
      pip install pillow
      ```

## Cara Mengkompilasi Program
Source Code tidak perlu dikompilasi karena menggunakan bahasa Python.

## Cara Menjalankan Program
Sebelumnya dipastikan berada di direktori root repository (Tucil1_13524096).

### 1. Menjalankan Mode CLI
1. Buka terminal
2. Jalankan perintah berikut.
   ```bash
   python src/main.py
   ```
3. Masukkan nama file .txt yang berada di folder test/ (Contoh: test_A.txt).
4. Program akan menampilkan proses pencarian secara Live dan hasil akhir beserta waktu eksekusi dan total kasus.

### 2. Menjalankan Mode GUI
1. Buka terminal
2. Jalankan perintah berikut.
   ```bash
   python src/gui.py
   ```
3. Tekan "Buka File" dan pilih file yang ingin dicari solusinya
4. Tekan "Temukan Solusi"
5. Program akan menampilkan proses pencarian secara Live dan hasil akhir beserta waktu eksekusi dan total kasus.

## Identitas Pembuat
Program ini dibuat untuk memenuhi Tugas Kecil 1 Strategi Algoritma oleh:

* Nama: Moreno Syawali Ganda Sugita
* NIM: 13524096
* Kelas: K02
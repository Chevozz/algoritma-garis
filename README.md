# Algorithm Drawing GUI

Aplikasi desktop Python untuk mendemonstrasikan penggambaran pixel memakai Tkinter Canvas. Tidak memakai matplotlib, library grafik eksternal, atau framework GUI eksternal.

## Tujuan

Aplikasi menghitung daftar koordinat pixel dengan empat algoritma, lalu menggambar setiap pixel sebagai kotak pada Canvas:

- Brute Force Line Drawing
- DDA Line Drawing
- Bresenham Line Drawing
- Midpoint Circle Algorithm

Sumbu X dan Y memakai koordinat Cartesian: X positif ke kanan, Y positif ke atas.

## Cara Menjalankan

Python 3.10+ disarankan. Tkinter biasanya sudah termasuk instalasi Python.

```bash
python main.py
```

Test tanpa pytest:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Struktur Folder

```text
project/
├── main.py
├── algorithms/
│   ├── __init__.py
│   ├── brute_force.py
│   ├── dda.py
│   ├── bresenham.py
│   └── circle.py
├── gui/
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_algorithms.py
└── README.md
```

## Penjelasan Algoritma

### Brute Force

Menggunakan persamaan `y = mx + c`. Program menghitung nilai y untuk setiap x, lalu membulatkannya ke pixel terdekat. Garis vertikal ditangani khusus agar tidak terjadi division by zero.

### DDA

Menghitung `dx`, `dy`, dan jumlah langkah. Setiap langkah menambahkan `x_increment` dan `y_increment`, kemudian hasilnya dibulatkan ke koordinat pixel.

### Bresenham

Menggunakan error integer untuk memilih pixel berikutnya. Algoritma tidak membutuhkan operasi pecahan dan menangani berbagai arah, slope, garis horizontal, serta garis vertikal.

### Midpoint Circle

Mulai dari titik `(0, radius)`, kemudian menghitung keputusan midpoint. Setiap titik dicerminkan ke delapan posisi simetris. Titik duplikat dihapus.

## Cara Kerja GUI

1. Pilih algoritma dari dropdown.
2. Isi koordinat garis atau center dan radius lingkaran.
3. Tekan `GAMBAR` untuk menampilkan semua pixel.
4. `RESET` mengembalikan input awal dan canvas.
5. Panel informasi menampilkan algoritma, input, jumlah pixel, waktu, dan koordinat hasil.

## Contoh Penggunaan

- DDA: `(0, 0) -> (15, 8)`
- Bresenham: `(5, 3) -> (0, 0)`
- Lingkaran: center `(0, 0)`, radius `8`

## Perbedaan Algoritma

- Brute Force mudah dipahami karena langsung memakai persamaan garis, tetapi memakai operasi pecahan.
- DDA memakai increment pecahan dan pembulatan pada tiap langkah.
- Bresenham lebih efisien karena memakai perhitungan integer.
- Midpoint Circle khusus untuk lingkaran dan memanfaatkan simetri delapan titik.

## Penjelasan Presentasi 5 Menit

1. Tujuan aplikasi: “Aplikasi ini mendemonstrasikan cara algoritma rasterisasi menghasilkan pixel untuk garis dan lingkaran.”
2. GUI: “Pengguna memilih algoritma dan mengisi input. Program menghasilkan list koordinat, lalu Canvas menggambar setiap koordinat sebagai kotak pixel.”
3. Brute Force: “Program menghitung persamaan garis untuk setiap x. Garis vertikal memakai kasus khusus.”
4. DDA: “DDA menentukan jumlah langkah terbesar dari dx dan dy, lalu menambah increment x dan y secara bertahap.”
5. Bresenham: “Bresenham memakai nilai error integer untuk memilih pixel yang paling dekat dengan garis.”
6. Circle Algorithm: “Midpoint Circle menghitung satu bagian lingkaran lalu menghasilkan delapan titik simetris.”
7. Perbedaan hasil: “Algoritma dapat memilih pixel berbeda karena metode pembulatan dan keputusan pixelnya berbeda. Bresenham paling hemat operasi karena integer.”
8. Penutup: “Animasi memperlihatkan urutan pixel yang dihasilkan, sehingga perhitungan algoritma dapat diamati langsung.”

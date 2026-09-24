import time
import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.brute_force import brute_force_line
from algorithms.dda import dda_line
from algorithms.bresenham import bresenham_line

CELL = 20          # ukuran 1 pixel kotak (dalam satuan layar)
COLS = 32          # jumlah kolom grid
ROWS = 26          # jumlah baris grid
ORIGIN_COL = 4     # kolom tempat x = 0
ORIGIN_ROW = 20    # baris (dihitung dari atas) tempat y = 0

MARGIN_L, MARGIN_T, MARGIN_R, MARGIN_B = 45, 15, 15, 45
CANVAS_W = MARGIN_L + COLS * CELL + MARGIN_R
CANVAS_H = MARGIN_T + ROWS * CELL + MARGIN_B

MIN_X, MAX_X = -ORIGIN_COL, COLS - 1 - ORIGIN_COL
MIN_Y, MAX_Y = ORIGIN_ROW - (ROWS - 1), ORIGIN_ROW

ALGORITHMS = {
    "Brute Force": brute_force_line,
    "DDA": dda_line,
    "Bresenham": bresenham_line,
}


def to_canvas(x, y):
    """Konversi koordinat Cartesian (y positif ke atas) ke koordinat canvas (y ke bawah)."""
    return MARGIN_L + (x + ORIGIN_COL) * CELL, MARGIN_T + (ORIGIN_ROW - y) * CELL


def draw_grid(canvas):
    """Gambar kotak-kotak grid abu-abu muda sebagai acuan pixel."""
    for col in range(COLS + 1):
        x = MARGIN_L + col * CELL
        canvas.create_line(x, MARGIN_T, x, MARGIN_T + ROWS * CELL, fill="#dddddd")
    for row in range(ROWS + 1):
        y = MARGIN_T + row * CELL
        canvas.create_line(MARGIN_L, y, MARGIN_L + COLS * CELL, y, fill="#dddddd")


def draw_axes(canvas):
    """Gambar sumbu X dan Y berwarna merah, plus angka koordinat."""
    x0, y0 = to_canvas(0, 0)

    canvas.create_line(MARGIN_L, y0, MARGIN_L + COLS * CELL, y0, fill="red", width=2)   # sumbu X
    canvas.create_line(x0, MARGIN_T, x0, MARGIN_T + ROWS * CELL, fill="red", width=2)   # sumbu Y

    for x in range(MIN_X, MAX_X + 1):
        if x % 5 == 0:
            cx, _ = to_canvas(x, 0)
            canvas.create_text(cx + CELL // 2, y0 + 10, text=str(x), fill="red", font=("Arial", 8))
    for y in range(MIN_Y, MAX_Y + 1):
        if y % 5 == 0:
            _, cy = to_canvas(0, y)
            canvas.create_text(x0 - 12, cy + CELL // 2, text=str(y), fill="red", font=("Arial", 8))


def draw_pixel(canvas, x, y, color):
    """Gambar satu pixel sebagai kotak kecil (create_rectangle, bukan create_line)."""
    cx, cy = to_canvas(x, y)
    canvas.create_rectangle(cx + 1, cy + 1, cx + CELL - 1, cy + CELL - 1, fill=color, outline=color)


class LineApp:
    def __init__(self, root):
        self.root = root
        root.title("Algoritma Menggambar Garis")

        self._build_input()
        self.canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="white")
        self.canvas.pack(padx=10, pady=(0, 5))
        self.reset()

    def _build_input(self):
        frame = tk.LabelFrame(self.root, text="Input Koordinat", padx=10, pady=8)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Titik Awal (X1, Y1)").grid(row=0, column=0, sticky="w")
        self.e_x1 = tk.Entry(frame, width=6)
        self.e_x1.grid(row=0, column=1, padx=4)
        self.e_y1 = tk.Entry(frame, width=6)
        self.e_y1.grid(row=0, column=2, padx=4)

        tk.Label(frame, text="Titik Akhir (X2, Y2)").grid(row=1, column=0, sticky="w", pady=4)
        self.e_x2 = tk.Entry(frame, width=6)
        self.e_x2.grid(row=1, column=1, padx=4)
        self.e_y2 = tk.Entry(frame, width=6)
        self.e_y2.grid(row=1, column=2, padx=4)

        tk.Label(frame, text="Algoritma").grid(row=0, column=3, padx=(20, 4), sticky="w")
        self.combo = ttk.Combobox(frame, values=list(ALGORITHMS), state="readonly", width=14)
        self.combo.current(1)   # default DDA
        self.combo.grid(row=0, column=4)

        tk.Button(frame, text="Gambar Garis", width=14, command=self.gambar).grid(
            row=1, column=3, padx=(20, 4), pady=4)
        tk.Button(frame, text="Reset", width=14, command=self.reset).grid(row=1, column=4)

        for entry, value in ((self.e_x1, 2), (self.e_y1, 6), (self.e_x2, 10), (self.e_y2, 14)):
            entry.insert(0, str(value))

        self.info = tk.Label(self.root, text="", justify="left", anchor="w",
                             font=("Consolas", 10))
        self.info.pack(fill="x", padx=10, pady=(0, 10))
        
    def reset(self):
        """Hapus garis dan kembalikan canvas ke kondisi awal."""
        self.canvas.delete("all")
        draw_grid(self.canvas)
        draw_axes(self.canvas)
        self.info.config(text="Algoritma : -\n"
                              "Titik Awal : -\n"
                              "Titik Akhir : -\n"
                              "Jumlah Pixel : -\n"
                              "Waktu Eksekusi : -")

    def _baca_input(self):
        """Ambil dan validasi isi Entry. Return (x1, y1, x2, y2)."""
        nilai = []
        for entry, nama in ((self.e_x1, "X1"), (self.e_y1, "Y1"),
                            (self.e_x2, "X2"), (self.e_y2, "Y2")):
            teks = entry.get().strip()
            try:
                nilai.append(int(teks))
            except ValueError:
                messagebox.showerror("Input Salah", f"{nama} harus berupa angka bulat.")
                return None

        x1, y1, x2, y2 = nilai
        for x, y in ((x1, y1), (x2, y2)):
            if not (MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y):
                messagebox.showerror(
                    "Di Luar Area",
                    f"Titik ({x}, {y}) di luar area gambar.\n"
                    f"X: {MIN_X}..{MAX_X}, Y: {MIN_Y}..{MAX_Y}")
                return None
        return x1, y1, x2, y2

    def gambar(self):
        data = self._baca_input()
        if data is None:
            return
        x1, y1, x2, y2 = data
        nama_algo = self.combo.get()

        self.canvas.delete("all")
        draw_grid(self.canvas)
        draw_axes(self.canvas)

        mulai = time.perf_counter()
        pixels = ALGORITHMS[nama_algo](x1, y1, x2, y2)
        selesai = time.perf_counter()

        for x, y in pixels:
            draw_pixel(self.canvas, x, y, "black")
        draw_pixel(self.canvas, x1, y1, "red")     # titik awal
        draw_pixel(self.canvas, x2, y2, "blue")    # titik akhir

        self.info.config(
            text=f"Algoritma : {nama_algo}\n"
                 f"Titik Awal : ({x1}, {y1})\n"
                 f"Titik Akhir : ({x2}, {y2})\n"
                 f"Jumlah Pixel : {len(pixels)}\n"
                 f"Waktu Eksekusi : {selesai - mulai:.6f} detik")


if __name__ == "__main__":
    root = tk.Tk()
    LineApp(root)
    root.mainloop()

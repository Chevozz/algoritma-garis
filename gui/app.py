import time
import tkinter as tk
from tkinter import messagebox, ttk

from algorithms import bresenham_line, brute_force_line, dda_line, midpoint_circle

CELL = 22
CANVAS_WIDTH, CANVAS_HEIGHT = 790, 590
ORIGIN_X, ORIGIN_Y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
ALGORITHMS = {
    "Brute Force": brute_force_line,
    "DDA": dda_line,
    "Bresenham": bresenham_line,
    "Lingkaran": midpoint_circle,
}
DESCRIPTIONS = {
    "Brute Force": "Menghitung y dari persamaan garis untuk setiap x.",
    "DDA": "Melangkah dengan increment pecahan lalu membulatkan pixel.",
    "Bresenham": "Memilih pixel terdekat memakai perhitungan integer.",
    "Lingkaran": "Midpoint Circle memakai simetri delapan arah.",
}


class GraphicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Drawing GUI")
        self.root.geometry("1160x720")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#eef2f6")
        self._setup_style()
        self._build_layout()
        self._set_defaults()
        self._draw_base()

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#16324f")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#607080")
        style.configure("Panel.TLabelframe", background="white")
        style.configure("Panel.TLabelframe.Label", background="white", foreground="#16324f", font=("Segoe UI", 10, "bold"))
        style.configure("Panel.TFrame", background="white")
        style.configure("TLabel", background="white", foreground="#263746")
        style.configure("Primary.TButton", background="#2563eb", foreground="white", padding=8)
        style.map("Primary.TButton", background=[("active", "#1d4ed8")])
        style.configure("TButton", padding=7)

    def _build_layout(self):
        body = ttk.Frame(self.root, padding=(24, 20, 24, 20))
        body.pack(fill="both", expand=True)
        self.control = ttk.Frame(body, style="Panel.TFrame", padding=18)
        self.control.pack(side="left", fill="y", padx=(0, 16))
        visual = ttk.Frame(body, style="Panel.TFrame", padding=12)
        visual.pack(side="left", fill="both", expand=True)

        ttk.Label(self.control, text="KONTROL INPUT", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 12))
        ttk.Label(self.control, text="Algoritma").pack(anchor="w")
        self.algorithm = ttk.Combobox(self.control, values=list(ALGORITHMS), state="readonly", width=23)
        self.algorithm.pack(anchor="w", pady=(4, 16))
        self.algorithm.bind("<<ComboboxSelected>>", lambda _event: self._update_form())

        self.form_holder = ttk.Frame(self.control, style="Panel.TFrame")
        self.form_holder.pack(fill="x")
        self.line_frame = ttk.LabelFrame(self.form_holder, text="Titik Garis", style="Panel.TLabelframe", padding=10)
        self.line_frame.pack(fill="x", pady=(0, 10))
        self.line_entries = self._make_entries(self.line_frame, (("X1", "x1"), ("Y1", "y1"), ("X2", "x2"), ("Y2", "y2")))

        self.circle_frame = ttk.LabelFrame(self.form_holder, text="Lingkaran", style="Panel.TLabelframe", padding=10)
        self.circle_entries = self._make_entries(self.circle_frame, (("Center X", "xc"), ("Center Y", "yc"), ("Radius", "radius")))

        buttons = ttk.Frame(self.control, style="Panel.TFrame")
        buttons.pack(fill="x", pady=(4, 12))
        ttk.Button(buttons, text="GAMBAR", style="Primary.TButton", command=self.draw).pack(fill="x", pady=3)
        ttk.Button(buttons, text="RESET", command=self.reset).pack(fill="x", pady=3)

        info_frame = ttk.LabelFrame(self.control, text="Informasi", style="Panel.TLabelframe", padding=10)
        info_frame.pack(fill="both", expand=True)
        self.info = tk.Text(info_frame, width=30, height=10, bg="#f8fafc", fg="#263746", relief="flat", font=("Consolas", 9), wrap="word")
        self.info.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(visual, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", highlightthickness=1, highlightbackground="#cbd5e1")
        self.canvas.pack(fill="both", expand=True)

    def _make_entries(self, parent, fields):
        entries = {}
        for row, (label, key) in enumerate(fields):
            ttk.Label(parent, text=label).grid(row=row // 2, column=(row % 2) * 2, sticky="w", padx=(0, 5), pady=5)
            entry = ttk.Entry(parent, width=7)
            entry.grid(row=row // 2, column=(row % 2) * 2 + 1, padx=(0, 8), pady=5)
            entries[key] = entry
        return entries

    def _set_defaults(self):
        self.algorithm.set("DDA")
        for key, value in (("x1", 0), ("y1", 0), ("x2", 15), ("y2", 8)):
            self.line_entries[key].insert(0, str(value))
        for key, value in (("xc", 0), ("yc", 0), ("radius", 8)):
            self.circle_entries[key].insert(0, str(value))
        self._update_form()

    def _update_form(self):
        is_circle = self.algorithm.get() == "Lingkaran"
        self.line_frame.pack_forget()
        self.circle_frame.pack_forget()
        (self.circle_frame if is_circle else self.line_frame).pack(fill="x", pady=(0, 10))

    def _draw_base(self):
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), CANVAS_WIDTH)
        height = max(self.canvas.winfo_height(), CANVAS_HEIGHT)
        self.canvas.create_line(0, ORIGIN_Y, width, ORIGIN_Y, fill="#94a3b8", width=2)
        self.canvas.create_line(ORIGIN_X, 0, ORIGIN_X, height, fill="#94a3b8", width=2)
        for x in range(ORIGIN_X % CELL, width, CELL):
            self.canvas.create_line(x, 0, x, height, fill="#e2e8f0")
        for y in range(ORIGIN_Y % CELL, height, CELL):
            self.canvas.create_line(0, y, width, y, fill="#e2e8f0")
        self.canvas.create_text(width - 16, ORIGIN_Y - 12, text="X", fill="#64748b")
        self.canvas.create_text(ORIGIN_X + 12, 12, text="Y", fill="#64748b")

    def _to_canvas(self, x, y):
        return ORIGIN_X + x * CELL, ORIGIN_Y - y * CELL

    def _draw_pixel(self, x, y, color="#2563eb"):
        cx, cy = self._to_canvas(x, y)
        self.canvas.create_rectangle(cx - CELL // 2 + 1, cy - CELL // 2 + 1, cx + CELL // 2 - 1, cy + CELL // 2 - 1, fill=color, outline=color, tags="pixel")

    def _read_ints(self, entries):
        values = {}
        for key, entry in entries.items():
            try:
                values[key] = int(entry.get().strip())
            except ValueError:
                messagebox.showerror("Input Salah", f"{key} harus berupa bilangan bulat.")
                return None
        if "radius" in values and values["radius"] < 0:
            messagebox.showerror("Input Salah", "Radius tidak boleh negatif.")
            return None
        return values

    def _compute(self):
        name = self.algorithm.get()
        values = self._read_ints(self.circle_entries if name == "Lingkaran" else self.line_entries)
        if values is None:
            return None
        if name == "Lingkaran":
            pixels = midpoint_circle(values["xc"], values["yc"], values["radius"])
            label = f"Center: ({values['xc']}, {values['yc']}), r={values['radius']}"
        else:
            pixels = ALGORITHMS[name](values["x1"], values["y1"], values["x2"], values["y2"])
            label = f"({values['x1']}, {values['y1']}) -> ({values['x2']}, {values['y2']})"
        return name, values, pixels, label

    def _show_info(self, name, values, pixels, label, elapsed=0):
        coordinates = ", ".join(map(str, pixels))
        text = f"Algoritma: {name}\nInput: {label}\nJumlah pixel: {len(pixels)}\nWaktu: {elapsed:.6f} detik\n\nKoordinat:\n{coordinates}"
        self.info.delete("1.0", "end")
        self.info.insert("1.0", text)

    def draw(self):
        data = self._compute()
        if data is None:
            return
        name, values, pixels, label = data
        started = time.perf_counter()
        self._draw_base()
        for x, y in pixels:
            self._draw_pixel(x, y)
        elapsed = time.perf_counter() - started
        self.pixels = pixels
        self._show_info(name, values, pixels, label, elapsed)

    def reset(self):
        for entry in (*self.line_entries.values(), *self.circle_entries.values()):
            entry.delete(0, "end")
        self._set_defaults()
        self._draw_base()
        self.info.delete("1.0", "end")
        self.info.insert("1.0", "Pilih algoritma lalu tekan GAMBAR.")


def run():
    root = tk.Tk()
    GraphicsApp(root)
    root.mainloop()

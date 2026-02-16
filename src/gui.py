import tkinter as tk
from tkinter import filedialog, messagebox
import main
import random
import time
import os
from PIL import Image, ImageDraw, ImageFont
from ctypes import windll

try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class GUI:
    def __init__(self, root):
        # Basic
        self.root = root
        self.root.title("Queens (Never Cry) Solver")
        self.root.geometry("900x950")
        self.root.config(bg="#F4F6F9")

        # State
        self.board = []
        self.n = 0
        self.solution = []
        self.color_map = {}
        self.filename_only = ""
        
        # Style (Aku memang anak pastel gitu kak)
        self.font_title = ("Segoe UI", 16, "bold")
        self.font_btn = ("Segoe UI", 11)
        self.font_text = ("Segoe UI", 10)
        self.font_mono = ("Consolas", 10)
        
        self.colors = [
            "#FFB7B2", "#FFDAC1", "#E2F0CB", "#B5EAD7", "#C7CEEA",
            "#F8BBD0", "#E1BEE7", "#D1C4E9", "#C5CAE9", "#BBDEFB",
            "#B3E5FC", "#B2EBF2", "#B2DFDB", "#C8E6C9", "#DCEDC8",
            "#F0F4C3", "#FFF9C4", "#FFECB3", "#FFE0B2", "#FFCCBC"
        ]

        # UI LAYOUT
        # Header
        header_frame = tk.Frame(root, bg="white", padx=20, pady=15)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        tk.Label(header_frame, text="Queens Solver", font=self.font_title, bg="white", fg="#2C3E50").pack(side=tk.LEFT)

        btn_frame = tk.Frame(header_frame, bg="white")
        btn_frame.pack(side=tk.RIGHT)

        self.btn_load = self.create_button(btn_frame, "Buka File", self.load_file, "#3498DB")
        self.btn_solve = self.create_button(btn_frame, "Temukan Solusi", self.run_solver, "#2ECC71", state=tk.DISABLED)
        
        # Status Bar
        status_frame = tk.Frame(root, bg="#F4F6F9", padx=20)
        status_frame.pack(fill=tk.X, pady=5)
        self.lbl_status = tk.Label(status_frame, text="Silakan muat file.", font=self.font_text, bg="#F4F6F9", fg="#7F8C8D")
        self.lbl_status.pack(side=tk.LEFT)
        
        # Slider Speed
        speed_frame = tk.Frame(status_frame, bg="#F4F6F9")
        speed_frame.pack(side=tk.RIGHT)
        tk.Label(speed_frame, text="Kecepatan:", font=self.font_text, bg="#F4F6F9", fg="#7F8C8D").pack(side=tk.LEFT, padx=5)
        self.scale_speed = tk.Scale(speed_frame, from_=0.00, to=0.3, resolution=0.01, orient=tk.HORIZONTAL, length=120, bg="#F4F6F9", highlightthickness=0)
        self.scale_speed.set(0.05)
        self.scale_speed.pack(side=tk.LEFT)

        # Canvas
        canvas_container = tk.Frame(root, bg="white", padx=5, pady=5)
        canvas_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        self.canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        self.lbl_stats = tk.Label(root, text="", font=self.font_mono, bg="#F4F6F9", fg="#2C3E50")
        self.lbl_stats.pack(pady=(0, 20))

    def create_button(self, parent, text, command, bg_color, state=tk.NORMAL):
        btn = tk.Button(parent, text=text, command=command, state=state, font=self.font_btn, bg=bg_color, fg="white", relief=tk.FLAT, padx=15, pady=6, cursor="hand2")
        btn.pack(side=tk.LEFT, padx=5)
        return btn

    def generate_colors(self):
        chars = sorted(list(set(c for row in self.board for c in row)))
        self.color_map = {}
        for i, char in enumerate(chars):
            if i < len(self.colors):
                self.color_map[char] = self.colors[i]
            else:
                self.color_map[char] = f'#{random.randint(200,255):02x}{random.randint(200,255):02x}{random.randint(200,255):02x}'

    def load_file(self):
        init_dir = os.path.join(os.getcwd(), "test")
        fullpath = filedialog.askopenfilename(initialdir=init_dir, filetypes=[("Text Files", "*.txt")])
        if not fullpath: return

        filename = os.path.basename(fullpath)
        self.filename_only = filename
        data, n, msg = main.ReadFiles(filename)

        if not data:
            messagebox.showerror("Error", msg)
            return

        self.board = data
        self.n = n
        self.solution = []
        self.generate_colors()
        self.draw_board()
        
        self.lbl_status.config(text=f"File Terbuka: {filename} ({n}x{n})", fg="#2C3E50")
        self.lbl_stats.config(text="")
        self.btn_solve.config(state=tk.NORMAL, bg="#2ECC71")

    def draw_board(self):
        self.canvas.delete("all")
        if not self.board: return

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        pad = 20
        size = min(w, h) - (2 * pad)
        cell = size / self.n
        sx, sy = (w - (cell * self.n)) / 2, (h - (cell * self.n)) / 2

        # Grid
        for r in range(self.n):
            for c in range(self.n):
                x1, y1 = sx + c*cell, sy + r*cell
                char = self.board[r][c]
                color = self.color_map.get(char, "#FFFFFF")
                self.canvas.create_rectangle(x1, y1, x1+cell, y1+cell, fill=color, outline="#E0E0E0", width=1)
                self.canvas.create_text(x1+10, y1+10, text=char, font=("Segoe UI", 8), fill="#888")

        for r, c in self.solution:
            cx, cy = sx + c*cell + cell/2, sy + r*cell + cell/2
            self.canvas.create_text(cx, cy, text="♛", fill="#2C3E50", font=("Segoe UI Symbol", int(cell*0.6)))

    def update_visuals(self, row, col, curr, board, n):
        if main.iter % 1000 == 0:
            self.solution = list(curr)
            self.draw_board()
            display_row = min(row + 1, n)
            display_col = max(0, col) + 1 if col < n else n
            self.lbl_stats.config(text=f"Mengecek Baris {display_row}, Kolom {display_col} | Iterasi: {main.iter}")
            self.root.update()
            speed = self.scale_speed.get()
            if speed > 0:
                time.sleep(speed)

    def run_solver(self):
        self.lbl_status.config(text="Sedang mencari solusi...", fg="#E67E22")
        self.btn_solve.config(state=tk.DISABLED, bg="#BDC3C7")
        self.btn_load.config(state=tk.DISABLED)
        
        main.iter = 0
        temp_sol = []
        
        start = time.perf_counter()
        found = main.solve(0, temp_sol, self.board, self.n, show=self.update_visuals)
        end = time.perf_counter()

        self.solution = temp_sol
        self.draw_board()
        final_row = self.n if found else self.n
        self.lbl_stats.config(text=f"Selesai | Total Iterasi: {main.iter}")
        self.root.update()
        
        self.btn_solve.config(state=tk.NORMAL, bg="#2ECC71")
        self.btn_load.config(state=tk.NORMAL)

        if found:
            self.lbl_status.config(text="Solusi Ditemukan!", fg="#27AE60")
            durasi = (end - start) * 1000
            self.lbl_stats.config(text=f"Waktu: {durasi:.2f} ms | Total Iterasi: {main.iter}")
            
            if messagebox.askyesno("Simpan Solusi", "Solusi ditemukan! Simpan ke file (TXT & PNG)?"):
                self.save_solution(temp_sol)
        else:
            self.lbl_status.config(text="Tidak ada solusi.", fg="#C0392B")
            durasi = (end - start) * 1000
            self.lbl_stats.config(text=f"Waktu: {durasi:.2f} ms | Total Iterasi: {main.iter}")

    # Fitur Simpan TXT & Gambar
    def save_solution(self, solution):
        try:
            base_name = os.path.splitext(self.filename_only)[0]
            folder_path = os.path.join("test")
            
            # Simpan TXT
            txt_path = os.path.join(folder_path, f"solusi_{base_name}.txt")
            grid = [list(r) for r in self.board]
            for r, c in solution: grid[r][c] = '#'
            with open(txt_path, "w") as f:
                for row in grid: f.write("".join(row) + "\n")
            
            msg = f"Teks disimpan: {txt_path}"

            # Simpan Gambar (PNG)
            img_path = os.path.join(folder_path, f"solusi_{base_name}.png")
            self.generate_image(solution, img_path)
            msg += f"\nGambar disimpan: {img_path}"
            
            messagebox.showinfo("Berhasil", msg)

        except Exception as e:
            messagebox.showerror("Gagal", f"Error saving files: {e}")

    def generate_image(self, solution, path):
        # Konfigurasi Ukuran Gambar
        IMG_SIZE = 1000
        CELL_SIZE = IMG_SIZE // self.n
        
        # Buat Canvas Putih
        img = Image.new("RGB", (IMG_SIZE, IMG_SIZE), "white")
        draw = ImageDraw.Draw(img)
        
        # Load Font
        try:
            font_queen = ImageFont.truetype("arial.ttf", int(CELL_SIZE * 0.7))
            font_label = ImageFont.truetype("arial.ttf", int(CELL_SIZE * 0.15))
        except:
            font_queen = ImageFont.load_default()
            font_label = ImageFont.load_default()

        # Gambar Grid & Label
        for r in range(self.n):
            for c in range(self.n):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                char = self.board[r][c]
                color = self.color_map.get(char, "#FFFFFF")
                draw.rectangle([x1, y1, x2, y2], fill=color, outline="#888888", width=2)
                draw.text((x1 + 10, y1 + 5), char, fill="#555555", font=font_label)

        # Gambar "Q" buat export
        for r, c in solution:
            # Koordinat titik tengah kotak
            mid_x = c * CELL_SIZE + (CELL_SIZE / 2)
            mid_y = r * CELL_SIZE + (CELL_SIZE / 2)
            draw.text((mid_x, mid_y), "Q", fill="black", font=font_queen, anchor="mm")

        img.save(path, "PNG")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

# Ratu ratu apa yang dipake buat belanja?
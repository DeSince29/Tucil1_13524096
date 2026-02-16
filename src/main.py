import time
import os

# Membaca file yang ada di folder test/
def ReadFiles(name):
    if os.path.exists(os.path.join("test", name)):
        path = os.path.join("test", name)
    else:
        return None, 0, f"File {name} tidak ditemukan di folder test/."
    
    try:
        with open(path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

            if not lines:
                return None, 0, "File kosong"
            
            board = [list(line) for line in lines]
            m = len(board)
            n = len(board[0])

            # Ngecek papannya valid atau tidak
            for i, row in enumerate(board):
                if len(row) != n:
                    return None, 0, f"Baris {i+1} memiliki panjang berbeda"
            if m != n:
                return None, 0, "Papan berbentuk persegi panjang. Tidak Valid"
            
            for r in range(n):
                for c in range(n):
                    if board[r][c] == '#':
                        return None, 0, "File mengandung karakter '#'"
            
            unik = set()
            for r in range(n):
                for c in range(n):
                    unik.add(board[r][c])
            
            colorCnt = len(unik)
            if colorCnt != n:
                return None, 0, f"Terdapat {colorCnt} warna, seharusnya {n} warna (sesuai ukuran papan)"

            return board, n, "Berhasil input file"
        
    except FileNotFoundError:
        return None, 0, "File tidak ditemukan"

# Cek papan solusi legal atau tidak
def IsItLegal(curr, board):
    for i in range(len(curr)):
        r1, c1 = curr[i]
        color1 = board[r1][c1]
        for j in range(i + 1, len(curr)):
            r2, c2 = curr[j]
            color2 = board[r2][c2]
            if c1 == c2 or color1 == color2 or (abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1): return False
    return True

# Output board
def PrintBoard(hasil):
    for row in hasil: print(" ".join(row))

# Parameter untuk menghitung kasus
iter = 0

# Fungsi untuk menyelesaikan puzzle secara rekursif
def solve(row, curr, board, n, show=None):
    global iter
    
    if row == n:
        iter += 1
        if show and iter % 1000 == 0: show(row, -1, curr, board, n)
        return IsItLegal(curr, board)

    for col in range(n):
        curr.append((row, col))
        if show and iter % 1000 == 0: show(row, col, curr, board, n)
        if solve(row + 1, curr, board, n, show): return True
        curr.pop()
        if show and iter % 1000 == 0: show(row, col, curr, board, n)
    
    return False

def cli_show(row, col, curr, board, n):
    print("\033[H", end="")
    display = [list(r) for r in board]

    for r, c in curr:
        display[r][c] = '#'

    for line in display:
        print(" ". join(line))

    print(f"Mengecek Baris {min(row + 1, len(board))}, Kolom {max(0, col) + 1}\nBanyak Iterasi: {iter}")

# MAIN PROGRAM
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    name = input("Masukkan nama file .txt dari folder test (cth: ""test.txt""): ")
    board, n, statusFile = ReadFiles(name)
    print(statusFile)
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

    if board:
        print("\033[?25l", end="")

        try:
            iter = 0
            solution = []
            start = time.perf_counter()
            found = solve(0, solution, board, n, show=cli_show)
            end = time.perf_counter()
            cli_show(n-1, n-1, solution, board, n)
            print("\033[?25h", end="")

            if found:
                print("\033[?25h", end="")
                end = time.perf_counter()
                print("\nSolusi ditemukan:")

                hasil = [list(row) for row in board]
                for r, c in solution:
                    hasil[r][c] = '#'
                PrintBoard(hasil)

                print(f"Waktu pencarian: {(end-start) * 1000:.2f} ms")
                print(f"Banyak kasus yang ditinjau: {iter} kasus")

                if input("Ingin menyimpan solusi? (y/n): ").lower() == 'y':
                    output = "solusi_" + name
                    path = os.path.join("test", output)
                    with open(path, "w") as file:
                        for row in hasil:
                            file.write("".join(row) + "\n")
                    print(f"Solusi telah disimpan di test/{output}")
            else:
                print("\nTidak ada solusi yang valid.")
                print(f"Waktu pencarian: {(end-start) * 1000:.2f} ms")
                print(f"Banyak kasus yang ditinjau: {iter} kasus")
        finally:
            print("\033[?25h", end="")

# Ratu-san juta HAHAHAHAHA (mmf stres dikit)
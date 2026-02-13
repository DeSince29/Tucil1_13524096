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
            lines = [line.strip() for line in file if line.strip]

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

# Mengecek apakah suatu kotak legal diletakkan Queen atau tidak
def IsItLegal(row, col, curr, board):
    color = board[row][col]
    for r, c in curr:
        if c == col or board[r][c] == color:
            return False
        if abs(r - row) <= 1 and abs(c - col) <= 1:
            return False
    return True

# Output board
def PrintBoard(hasil):
    for row in hasil:
        print(" ".join(row))
    print("")

# Parameter untuk menghitung kasus
iter = 0

# Fungsi untuk menyelesaikan puzzle secara rekursif
def solve(row, curr, board, n, show=None):
    global iter

    if row == n:
        return True

    for col in range(n):
        iter += 1

        if show:
            show(row, col, curr, board, n)

        if IsItLegal(row, col, curr, board):
            curr.append((row, col))
        
            if solve(row+1, curr, board, n, show):
                return True
        
            curr.pop()

            if show:
                show(row, col, curr, board, n, backtrack=True)
    
    return False

def cli_show(row, col, curr, board, n, backtrack=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    display = [list(r) for r in board]

    for r, c in curr:
        display[r][c] = '#'

    if not backtrack and row < n:
        display[row][col] = '?'

    for line in display:
        print(" ". join(line))

    print(f"Mengecek Baris {row}, Kolom {col}\nBanyak Iterasi: {iter}")
    time.sleep(0.05)

# MAIN PROGRAM
if __name__ == "__main__":
    name = input("Masukkan nama file .txt (di folder test): ")
    board, n, statusFile = ReadFiles(name)
    print(statusFile)

    if board:
        iter = 0
        start = time.perf_counter()
        solution = []

        if solve(0, solution, board, n, show=cli_show):
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
            print("Tidak ada solusi yang valid.")

# Ratu-san ribu HAHAHAHAHA (mmf stres dikit)
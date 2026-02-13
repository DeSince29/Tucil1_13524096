import time
import os

# 
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
            for i, row in enumerate(board):
                if len(row) != n:
                    return None, 0, f"Baris {i+1} memiliki panjang berbeda"
            if m != n:
                return None, 0, f"Papan berbentuk persegi panjang. Tidak Valid"
            
            return board, n, "Berhasil input file"
    except FileNotFoundError:
        return None, 0, "File tidak ditemukan"

def IsItLegal(row, col, curr, board):
    color = board[row][col]
    for r, c in curr:
        if c == col or board[r][c] == color:
            return False
        if abs(r - row) <= 1 and abs(c - col) <= 1:
            return False
    return True

def PrintBoard(hasil, n):
    for row in hasil:
        print(" ".join(row))
    print("")

def Update(row, col, board, n, curr):
    os.system('cls' if os.name == 'nt' else 'clear')
    temp = [list(r) for r in board]
    for r, c in curr:
        temp[r][c] = '#'
    temp[row][col] = '?'
    PrintBoard(temp, n)
    time.sleep(0.05)

iter = 0

def solve(row, curr, board, n):
    global iter

    if row == n:
        return True

    for col in range(n):
        iter += 1
        # Update(row, col, board, n, curr)
        if IsItLegal(row, col, curr, board):
            curr.append((row, col))
        
            if solve(row+1, curr, board, n):
                return True
        
            curr.pop()
    
    return False

# MAIN PROGRAM
if __name__ == "__main__":
    name = input("Masukkan nama file .txt (di folder test): ")
    board, n, statusFile = ReadFiles(name)
    print(statusFile)

    if board:
        start = time.perf_counter()
        solution = []

        if solve(0, solution, board, n):
            end = time.perf_counter()
            print("\nSolusi ditemukan:")

            hasil = [list(row) for row in board]
            for r, c in solution:
                hasil[r][c] = '#'
            PrintBoard(hasil, n)

            print(f"Waktu pencarian: {(end-start) * 1000:.2f} ms")
            print(f"Banyak kasus yang ditinjau: {iter} kasus")

            save = input("Ingin menyimpan solusi? (Ya/Tidak): ")
            if save.lower() == "ya":
                output = "solusi_" + name
                path = os.path.join("test", output)
                with open(path, "w") as file:
                    for row in hasil:
                        file.write("".join(row) + "\n")
                print(f"Solusi telah disimpan di test/{output}")
        else:
            print("Tidak ada solusi yang valid.")
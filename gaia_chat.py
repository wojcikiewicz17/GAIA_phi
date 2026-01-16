import socket, struct, sys, time
SOCKET_PATH = "gaia.sock"
def talk(text):
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(SOCKET_PATH)
        h = 5381
        for c in text: h = ((h << 5) + h) + ord(c)
        v = [(h & 0xFFFF)/65535.0, ((h >> 16) & 0xFFFF)/65535.0, ((h >> 32) & 0xFFFF)/65535.0]
        req = struct.pack("@B xxx 3f 64s", 2, v[0], v[1], v[2], b"")
        s.send(req)
        res = s.recv(1024)
        s.close()
        if res and res[0] == 1: print("MATCH ENCONTRADO!")
        else: print("SEM MEMORIA.")
    except Exception as e: print(f"ERR: {e}")
if __name__ == "__main__":
    while True:
        t = input("PY> ")
        if t == "q": break
        talk(t)

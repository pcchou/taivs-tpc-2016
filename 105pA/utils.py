from hashlib import sha256

SECRET = 'wowwowowow'

# 加 salt 的雜湊函數
def pwhash(x):
    m = sha256()
    m.update((x + SECRET).encode('utf-8'))
    return m.digest()

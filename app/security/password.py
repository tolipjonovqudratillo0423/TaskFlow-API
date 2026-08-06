from pwdlib import PasswordHash


def set_password(plain_password: str) -> str:
    
    password_hash = PasswordHash.recommended()
    
    hashed = password_hash.hash(plain_password)
    
    return hashed


def check_password(plain_password, hashed: str) -> bool:
    
    password_hash = PasswordHash.recommended()
    
    return password_hash.verify(plain_password, hashed)
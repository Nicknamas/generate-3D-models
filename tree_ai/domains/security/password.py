from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

argon2_hasher = Argon2Hasher(
    memory_cost=256 * 1024, time_cost=3, parallelism=4
)
bcrypt_hasher = BcryptHasher()
password_hash = PasswordHash(hashers=[argon2_hasher, bcrypt_hasher])

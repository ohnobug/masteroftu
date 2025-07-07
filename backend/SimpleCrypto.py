import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag

KEY = "1ocxv0tgU07NaKmneiQUbAR2RJrbrJnhAgNW1cYufjI="

class SimpleCrypto:
    # 定义加密算法，但不直接传入密钥。
    # algorithms.AES 构造函数需要一个 bytes 类型的密钥。
    # 我们需要传递密钥长度，但根据您提供的定义，直接实例化AES是需要密钥的。
    # 更常见的做法是，直接创建 Cipher 时传入算法实例和密钥。

    # 我们将 AES 的 key_size 定义为常量，方便验证
    AES_KEY_SIZE_BITS = 256
    AES_KEY_SIZE_BYTES = AES_KEY_SIZE_BITS // 8
    AES_BLOCK_SIZE_BITS = 128
    AES_BLOCK_SIZE_BYTES = AES_BLOCK_SIZE_BITS // 8

    CIPHER_MODE = modes.CBC

    @staticmethod
    def generate_key(key_size_bytes: int = AES_KEY_SIZE_BYTES) -> str:
        """
        生成一个安全的随机加密密钥。
        """
        key = os.urandom(key_size_bytes)
        return base64.urlsafe_b64encode(key).decode('utf-8')

    @staticmethod
    def _get_iv_length() -> int:
        """ 获取 AES 的 IV 长度 (16 字节)。 """
        return SimpleCrypto.AES_BLOCK_SIZE_BYTES

    @staticmethod
    def encrypt(data: str, key: str = None) -> str:
        """
        加密数据。
        """
        
        if not key:
            key = KEY
        
        try:
            # 1. 解码密钥
            key_bytes = base64.urlsafe_b64decode(key)
            if len(key_bytes) != SimpleCrypto.AES_KEY_SIZE_BYTES:
                 raise ValueError(f"Invalid key size. Expected {SimpleCrypto.AES_KEY_SIZE_BYTES} bytes, got {len(key_bytes)}.")

            # 2. 生成随机 IV (字节串)
            iv_bytes = os.urandom(SimpleCrypto._get_iv_length())

            # 3. 初始化 Cipher 对象
            # --- 正确方式：将密钥字节串传递给 algorithms.AES 构造函数 ---
            aes_algorithm_instance = algorithms.AES(key_bytes)
            cbc_mode_instance = SimpleCrypto.CIPHER_MODE(iv_bytes)
            cipher = Cipher(aes_algorithm_instance, cbc_mode_instance, backend=default_backend())
            # -------------------------------------------------------------
            encryptor = cipher.encryptor()

            # 4. 加密数据
            padded_data_bytes = encryptor.update(data.encode('utf-8')) + encryptor.finalize()

            # 5. 组合 IV 和密文，然后进行 base64 编码
            encrypted_combined_bytes = iv_bytes + padded_data_bytes
            return base64.urlsafe_b64encode(encrypted_combined_bytes).decode('utf-8')

        except (ValueError, TypeError, OSError) as e:
            raise ValueError(f"Encryption failed: {e}") from e

    @staticmethod
    def decrypt(encrypted_data_base64: str, key: str = None) -> str:
        """
        解密数据。
        """
        
        if not key:
            key = KEY
        
        try:
            # 1. 解码密钥
            key_bytes = base64.urlsafe_b64decode(key)
            if len(key_bytes) != SimpleCrypto.AES_KEY_SIZE_BYTES:
                 raise ValueError(f"Invalid key size. Expected {SimpleCrypto.AES_KEY_SIZE_BYTES} bytes, got {len(key_bytes)}.")

            # 2. 解码输入的加密数据 (包含 IV 和密文)
            encrypted_combined_bytes = base64.urlsafe_b64decode(encrypted_data_base64)
            iv_len = SimpleCrypto._get_iv_length()

            # 3. 提取 IV 和密文
            if len(encrypted_combined_bytes) < iv_len:
                raise ValueError("Encrypted data is too short to contain IV.")
            iv_bytes = encrypted_combined_bytes[:iv_len]
            encrypted_text_bytes = encrypted_combined_bytes[iv_len:]

            # 4. 初始化 Cipher 对象
            # --- 正确方式：将密钥字节串传递给 algorithms.AES 构造函数 ---
            aes_algorithm_instance = algorithms.AES(key_bytes)
            cbc_mode_instance = SimpleCrypto.CIPHER_MODE(iv_bytes)
            cipher = Cipher(aes_algorithm_instance, cbc_mode_instance, backend=default_backend())
            decryptor = cipher.decryptor()

            # 5. 执行解密
            decrypted_data_bytes = decryptor.update(encrypted_text_bytes) + decryptor.finalize()

            # 6. 将解密后的字节转换为字符串
            return decrypted_data_bytes.decode('utf-8')

        except (ValueError, TypeError, OSError, InvalidTag) as e:
            raise ValueError(f"Decryption failed: {e}") from e



# if __name__ == "__main__":
#     try:
#         secret_key = "1ocxv0tgU07NaKmneiQUbAR2RJrbrJnhAgNW1cYufjI="
#         encrypted_base64 = 'fICIWKmdy9o5NpjMg8xJQ2WmZPj8s9AHXfHjFAfDHU0='

#         decrypted_data = SimpleCrypto.decrypt(encrypted_base64, secret_key)
#         print(decrypted_data.strip())
#         # print(f"解密后的数据: {decrypted_data}")

#     except ValueError as e:
#         print(f"发生错误: {e}")
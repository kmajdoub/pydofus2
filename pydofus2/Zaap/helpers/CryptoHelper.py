import base64
import getpass
import hashlib
import json
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from pydofus2.Zaap.helpers.Device import Device


class CryptoHelper:
    
    @staticmethod
    def create_hash_from_string_md5(string):
        return hashlib.md5(string.encode()).digest()

    @staticmethod
    def create_hash_from_string_sha256(string):
        return hashlib.sha256(string.encode()).hexdigest()[:32]

    @staticmethod
    def encrypt(json_obj, uuid):
        key = CryptoHelper.create_hash_from_string_md5(uuid)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        json_bytes = json.dumps(json_obj).encode('utf-8')
        encrypted_data = encryptor.update(json_bytes) + encryptor.finalize()
        return iv.hex() + "|" + encrypted_data.hex()

    @staticmethod
    def generate_hash_from_cert(cert, hm1, hm2):
        # Extract the encoded certificate from the cert dict
        encoded_certificate = cert.get('encodedCertificate', '')
        
        # Convert hm2 to bytes and use as key for decryption
        key = hm2.encode()
        
        # Create a new AES-256-ECB cipher object for decryption
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the abse 64 encoded certificate
        base64_encoded_certificate = base64.b64decode(encoded_certificate)
        decoded_certificate_bytes = decryptor.update(base64_encoded_certificate)
        decrypted_certificate = decoded_certificate_bytes + decryptor.finalize()
        
        # Unpad the decrypted certificate
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_certificate = unpadder.update(decrypted_certificate) + unpadder.finalize()
        
        # Concatenate hm1 and decrypted certificate, then hash using SHA-256
        hash_input = hm1.encode() + decrypted_certificate
        return hashlib.sha256(hash_input).hexdigest()
    
    @staticmethod
    def encrypt_to_file(file_path, json_obj, uuid):
        encrypted_json_obj = CryptoHelper.encrypt(json_obj, uuid)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(encrypted_json_obj)

    @staticmethod
    def decrypt_from_file(file_path, uuid=None):
        if uuid is None:
            uuid = Device.get_uuid()
        # Logger().debug(f"Decrypting file {file_path} with uuid {uuid}")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return CryptoHelper.decrypt(data, uuid)

    @staticmethod
    def decrypt(data, uuid):
        iv, data_to_decrypt = data.split("|")
        iv = bytes.fromhex(iv)
        data_to_decrypt = bytes.fromhex(data_to_decrypt)
        key = CryptoHelper.create_hash_from_string_md5(uuid)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(data_to_decrypt) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()
        decrypted_data = decrypted_data.decode()
        return json.loads(decrypted_data)

    @staticmethod
    def get_file_hash(file_path):
        sha1_hasher = hashlib.sha1()
        try:
            with open(file_path, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    sha1_hasher.update(chunk)
            return sha1_hasher.hexdigest()
        except IOError:
            return 0

    @staticmethod
    def create_hm_encoder():
        plt, arch = Device.get_platform_and_architecture()
        id = Device.machine_id()
        username = getpass.getuser()
        os_version = Device.get_os_version()
        ram = Device.get_computer_ram()
        machine_infos = [arch, plt, id, username, str(int(os_version)), str(ram)]
        # Logger().debug(f"Machine infos : {machine_infos}, len : {len(machine_infos)}")
        machine_infos = "".join([arch, plt, id, username, str(int(os_version)), str(ram)])
        hm1 = CryptoHelper.create_hash_from_string_sha256(machine_infos)
        hm2 = hm1[::-1]
        return {"hm1": hm1, "hm2": hm2}
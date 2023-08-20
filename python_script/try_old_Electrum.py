import old_mnemonic

from typing import Union

import codecs
import hashlib
import ecdsa
import base58

def to_bytes(something, encoding='utf8') -> bytes:
    """
    cast string to bytes() like object, but for python2 support it's bytearray copy
    """
    if isinstance(something, bytes):
        return something
    if isinstance(something, str):
        return something.encode(encoding)
    elif isinstance(something, bytearray):
        return bytes(something)
    else:
        raise TypeError("Not a string or bytes like object")

def sha256(x: Union[bytes, str]) -> bytes:
    x = to_bytes(x, 'utf8')
    return bytes(hashlib.sha256(x).digest())

def sha256d(x: Union[bytes, str]) -> bytes:
    x = to_bytes(x, 'utf8')
    out = bytes(sha256(sha256(x)))
    return out

def string_to_number(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big', signed=False)
    
def stretch_key(seed):
    x = seed
    for i in range(100000):
        x = hashlib.sha256(x + seed).digest()        
    return string_to_number(x)
   
    
def get_sequence(mpk, for_change, n):
    return string_to_number(sha256d( ("%d:%d:"%(n, for_change)).encode('ascii') + bytes.fromhex(mpk) ))


    # n  - this will iterate used in that old electrum seed priv keys
CURVE_ORDER = 0xFFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFE_BAAEDCE6_AF48A03B_BFD25E8C_D0364141


def get_private_key(seedphrase, for_change = 0, n = 0):
    secexp_t = stretch_key( old_mnemonic.mn_decode(seedphrase.split(' ')).encode('utf8'))
    
    primPrivate = int.to_bytes(secexp_t, length=32, byteorder='big', signed=False).hex()

    private_key_bytes = codecs.decode(primPrivate, 'hex')
        # Get ECDSA public key (paired to given private key)
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    
    primPublic = key_bytes.hex()    
    
    secexp = (secexp_t + get_sequence(primPublic, for_change, n)) % CURVE_ORDER
    
    pk = int.to_bytes(secexp, length=32, byteorder='big', signed=False)
    return pk



def pk_to_hash_unc_p2pkh(priv_key): 
    private_key_bytes = codecs.decode(priv_key, 'hex')
        # Get ECDSA public key (paired to given private key)
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')
        # Add bitcoin byte '04' that denote UNCOMPRESSED public key
    bitcoin_byte = b'04'
    public_key = bitcoin_byte + key_hex
        # Compute the hash: public key bytes -> sha256 -> RIPEMD160
    public_key_bytes = codecs.decode(public_key, 'hex')
            # Run SHA256 for the public key
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()
            # Run ripemd160 for the SHA256
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        # Return RIPEMD160 hash
    return ripemd160_bpk_hex

    # Logic is same, but the public key is COMPRESSED: 
    # used only 32 bytes of the public key with "bitcoin code" set to
    # '03' or '02' based on the sign of the other unused 32 bytes
def pk_to_hash_c_p2pkh(priv_key):
    private_key_bytes = codecs.decode(priv_key, 'hex')

    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    
    if key_bytes[-1] & 1:
        bitcoin_byte = b'03'
    else:
        bitcoin_byte = b'02'
            
    key_bytes =  key_bytes[0:32]    
    key_hex = codecs.encode(key_bytes, 'hex')

    public_key = bitcoin_byte + key_hex

    public_key_bytes = codecs.decode(public_key, 'hex')
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')  
      
    return ripemd160_bpk_hex

def rp160hash_to_p2pkhAddress(rp160hash):
            # Add network byte
    network_byte = b'00'
    network_bitcoin_public_key = network_byte + rp160hash
    network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')
            # Double SHA256 to get checksum
    sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
    sha256_nbpk_digest = sha256_nbpk.digest()
    sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
    sha256_2_nbpk_digest = sha256_2_nbpk.digest()
    sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
    checksum = sha256_2_hex[:8]
            # Concatenate public key and checksum to get the address
    address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
    #address = BTC_operations.base58(address_hex)
    address = base58.b58encode(bytes(bytearray.fromhex(address_hex))).decode('utf-8')
    return address


    # Read the "text of interest"
    # (where seed words are planned to be inspected)
with open('text.txt') as f:
    text = f.readlines()    
text = ''.join(text).replace('\n',' ').replace("“",'').replace("”",'').replace(",",'').replace('.','')

    # Filter the text words - remain only the words from electrum word list
seedWords = [w for w in text.split(' ') if w in old_mnemonic.words]


for i in range(0,len(seedWords)-12+1):
    mnemonic_phrase = ' '.join(seedWords[i:(i+12)])
    
    addr_set = []
    for j in range(0, 20):
        pk = get_private_key(mnemonic_phrase, n = j).hex()
        addr_set.append(rp160hash_to_p2pkhAddress(pk_to_hash_c_p2pkh(pk)))
        addr_set.append(rp160hash_to_p2pkhAddress(pk_to_hash_unc_p2pkh(pk)))


    if '1K4ezpLybootYF23TM4a8Y4NyP7auysnRo' in addr_set:
    #if '1DxkewpFoKadwJzyxyoiq3qu9v5r6M1ZAd' in addr_set:    
        print(f'!!!!!!!!!!!! SOLUTION IS {mnemonic_phrase}')
        
    if (i % 10 == 0) and (i != 0):    
        print(f'{(i+1) / (len(seedWords)-12+1)}')



    



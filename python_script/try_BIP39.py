from bip32utils import BIP32Key
from bip32utils import BIP32_HARDEN
from bip32utils import Base58
import os, bip39

import codecs
import hashlib
import ecdsa
import base58

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


    # Read the BIP39 seed word list 
    # (english seed words here)
with open('english.txt') as f:
    bip39_list = f.readlines()    
bip39_list = [w.strip('\n') for w in bip39_list]

    # Read the "text of interest"
    # (where seed words are planned to be inspected)
with open('text.txt') as f:
    text = f.readlines()    
text = ''.join(text).replace('\n',' ').replace("“",'').replace("”",'').replace(",",'').replace('.','')

    # Filter the text words - remain only the words from BIP39 list
seedWords = [w for w in text.split(' ') if w in bip39_list]


    # go through all the BIP39 words meet in the text in their original
    # order with window of 12 words (assuming the seed is made from 12 words)
    # checking if they are forming some wallet - based on the checksum.
    # In case of a good combination - save the seed words AND the addresses
    # into mnemonics and addresses lists to be printed out at the end
passphrase = ''
addresses_c = []
addresses_unc = []
mnemonics = []

account_number = 0
i = 0        

for j in range(0,len(seedWords)-12+1):

    try:
        mnemonic = ' '.join(seedWords[j:(j+12)])
        
        seed = bip39.phrase_to_seed(mnemonic, passphrase=passphrase)
        key = BIP32Key.fromEntropy(seed)        
        pk = key.ChildKey(44 + BIP32_HARDEN).ChildKey(0 + BIP32_HARDEN).ChildKey(account_number + BIP32_HARDEN).ChildKey(0).ChildKey(i).PrivateKey().hex()
        
        addresses_c.append(rp160hash_to_p2pkhAddress(pk_to_hash_c_p2pkh(pk)))
        addresses_unc.append(rp160hash_to_p2pkhAddress(pk_to_hash_unc_p2pkh(pk)))
        
        mnemonics.append(mnemonic)
    except Exception as ex:
        with open('invalid_checksum_seeds.log','a') as f:
            f.write(f'{j}: error {ex}')
        
    # Print out the addresses and mnemonics(seed words) composed form 
    # the seed words ofr the original text
print( '\n'.join([pair[0]+', '+pair[1]+': '+pair[2] for pair in zip(addresses_c, addresses_unc, mnemonics )]) )


interesting_address = '1K4ezpLybootYF23TM4a8Y4NyP7auysnRo'
mnemonic = ''
if interesting_address in addresses_c:
    mnemonic = mnemonics[addresses_c.index(interesting_address)]
if interesting_address in addresses_unc:
    mnemonic = mnemonics[addresses_unc.index(interesting_address)]
    
if mnemonic != '':
    print(f'!!!!!!!!!!!! SOLUTION IS {mnemonic}')
else:
    print(f'\nMnemonic for {interesting_address} has not been found')

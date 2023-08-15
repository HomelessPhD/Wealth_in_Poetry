from bip32utils import BIP32Key
from bip32utils import BIP32_HARDEN
from bip32utils import Base58
import os, bip39

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
addresses = []
mnemonics = []
for i in range(0,len(seedWords)-12+1):

    try:
        mnemonic = ' '.join(seedWords[i:(i+12)])
        seed = bip39.phrase_to_seed(mnemonic, passphrase=passphrase)

        key = BIP32Key.fromEntropy(seed)
        account_number = 0
        i = 0
        print ("Address: " + key.ChildKey(44 + BIP32_HARDEN) \
         .ChildKey(0 + BIP32_HARDEN) \
         .ChildKey(account_number + BIP32_HARDEN) \
         .ChildKey(0) \
         .ChildKey(i) \
         .Address() )
        addresses.append(key.ChildKey(44 + BIP32_HARDEN).ChildKey(0 + BIP32_HARDEN).ChildKey(account_number + BIP32_HARDEN).ChildKey(0).ChildKey(i).Address())
        mnemonics.append(mnemonic)
    except Exception as ex:
        print(f'{i}: error {ex}')
        
    # Print out the addresses and mnemonics(seed words) composed form 
    # the seed words ofr the original text
print('\n'.join(addresses))
print('\n'.join(mnemonics))

if '1K4ezpLybootYF23TM4a8Y4NyP7auysnRo' in addresses:
    print(f'!!!!!!!!!!!! SOLUTION IS {mnemonics[addresses.index("1K4ezpLybootYF23TM4a8Y4NyP7auysnRo")]}')

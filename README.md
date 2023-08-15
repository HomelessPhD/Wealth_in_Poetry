# Securing Wealth in Poetry
What if you could embed your net worth in a story?

This puzzle composed by **Trithemius** and published on medium [[1]](https://medium.com/coinmonks/securing-bitcoin-seed-phrases-in-stories-d8eb43a02254).

To understand the ground of this puzzle - better read the article composed by the author (the copy available here on github in form of .mhtml document).

In short: the author stated that he saved [0.03 BTC](https://www.blockchain.com/explorer/addresses/btc/1K4ezpLybootYF23TM4a8Y4NyP7auysnRo) (~900$) on the wallet composed of some specific BIP39 seed words - and the word with the correct order is somehow encoded into the article.

```
Backup seed phrases are mnemonic devices used to backup and restore access
to wallets. BIP-39 seed phrases were implemented to create an english language
backup to be kept entirely offline. These are used by the majority of trusted
wallet providers to backup and restore access to accounts. Instead of needing
addresses together with private keys, only the seed phrases are required to
access an account.

....

A “trithemian seed” is a list of cryptocurrency backup seed phrases stored in an
 innocuous body of writing, such as a poem, story, or letter.

....

The beauty of trithemian seeds is that they hide in plain sight. If you’ve
 read this far, you’ve read every word required to access a wallet with .03 BTC.
 Good luck!
```

I have created a dummy python script (that can be found in "python_script" folder)
in order to check all BIP 39 seed words used in the article text. The script simply
goes over all BIP 39 words of the article trying the group of 12 words: stepping
them as: [1,2,3,....,11,12 words], [2,3,4,....,12,13 words], [3,4,5....,13,14 words],
.... In other words, it linearly takes 12 BIP 39 seed words from the text shifting
the beginning of the group over the text till it reach the end of the text.

The script works with the pythin module bip32utils, os and bip39 (they should be 
installed for the script to be used). It uses few files: english.txt - the list of all 
BIP 39 seed words and text.txt (the text of article) but you could replace with some
other text.
 

## P.S.

Thank you for spending time on my notes, i hope it was not totally useless and you've found something interesting. 

Any ideas\questions or propositions you may send to generalizatorSUB@gmail.com - also look at my twitter @MiningPredict.

-------------------------------------------------------------------------
### References:

[1] Trithemius puzzle description - https://medium.com/coinmonks/securing-bitcoin-seed-phrases-in-stories-d8eb43a02254


[@] The prize stated to be here - https://www.blockchain.com/explorer/addresses/btc/1K4ezpLybootYF23TM4a8Y4NyP7auysnRo

[*] MiningPredict (my twitter page) - https://twitter.com/miningpredict



-------------------------------------------------------------------------
### Support
I am poor Ukrainian student that will really appreciate any donations.
I have no home (flat\appartment), live in the dorm (refugee shelter).
 
P.S. Successfully evacuated from occupied regions of Ukraine.

**BTC**:  `1QKjnfVsTT1KXzHgAFUbTy3QbJ2Hgy96WU`

**LTC**:  `LNQopZ7ozXPQtWpCPrS4mGGYRaE8iaj3BE`

**DOGE**: `DQvfzvVyb4tnBpkd3DRUfbwJjgPSjadDTb`

 **BSV**: `1E56gGQ1rYG4kkRo5qPLMK7PHcpVYj15Pv`

**AR**: `0UM6uoLrrnxXuYpHMBDAv-6txNTMdaEkR2m_bP_1HyE`
(have never used Arweave wallet)

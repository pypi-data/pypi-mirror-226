# fair random

**fair random** is a random library with hash prove

```python
>>> from fair_random import get_client_seed, get_server_seed, get_final_seed
>>> client_seed = get_client_seed("123")
>>> client_seed.hash
'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
>>> server_seed = get_server_seed()
>>> server_seed.hash
'b83268d870a9045241918ee76041046e3ca1cb94230bfe6163401ea0ec8df907'
>>> server_seed.server_prove
'19d3b12106df35a87cb784986a8382b3f5eaa5da3bd67e38aa8abc07a5e2ae3d'
>>> final_seed = get_final_seed(server_seed, [client_seed])
>>> final_seed.hash
'a8a8a1a4c5dfbc4bf46dfb7469b21d9e7adb5c6c4bdc316c90bb0cdeb7111856'
>>> dice = Dice()
>>> dice.get_value(final_seed)
3
```

You can expose server_seed.server_prove before the game starts, allow clients to provide random input, and then expose server_seed.hash after the game ends to demonstrate the immutability of the game."
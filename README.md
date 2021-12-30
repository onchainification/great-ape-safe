# GreatApeSafe

This is an extension of the legendary [Ape Safe](https://github.com/banteg/ape-safe), inheriting all the good stuff from `ApeSafe`, while adding some extra functions and making it protocol aware.

Instead of (re)writing protocol specific logic for every script, `GreatApeSafe` contains wrappers for each protocol's specific on-chain API. On top of that, all necessary addresses are hard-coded and loaded.

This prevents having to dive into documentation every time, either for figuring out the exact way to call the on-chain functions or finding deployed addresses.

For example, calling the [AAVE lending pool's contract](https://etherscan.io/address/0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9#readProxyContract) doesn't require any searching or address copypasting:

```python
>>> safe.aave.pool.paused()
False
```

And making a deposit becomes as simple as:

```python
safe.aave.deposit(usdc, usdc.balanceOf(safe))
```

Under the hood, the protocol class `Aave` solves what exact aToken we are dealing with, makes the necessary approval, calls the right functions and makes an on-fork assertion of successful execution:

```python
class Aave():
    ...
    def deposit(self, underlying, mantissa, destination=None):
        # deposit `mantissa` amount of `underlying` into aave pool
        # https://docs.aave.com/developers/the-core-protocol/lendingpool#deposit
        destination = self.safe.address if not destination else destination
        atoken_addr = self.data.getReserveTokensAddresses(underlying)[0]
        atoken = self.safe.contract(atoken_addr)
        bal_before = atoken.balanceOf(destination)
        underlying.approve(self.pool, mantissa)
        self.pool.deposit(underlying, mantissa, destination, 0)
        assert atoken.balanceOf(destination) > bal_before
```

By no means complete, but included platforms currently are:
- Aave
- Compound
- Convex
- Curve

# Installation

```
git clone git@github.com:gosuto-ai/great-ape-safe.git
```
```
pip install -r requirements-core.txt
```
And copy `.env.example` to `.env` and add your API keys to it if needed.

# Running
```
brownie run example
```

# Testing
```
brownie test
```

![pngwing com](https://user-images.githubusercontent.com/2835259/147793601-c597898e-0e9a-4eac-9413-d3dc6a1534cb.png)

import pytest
from brownie import interface


@pytest.fixture(autouse=True)
def deposited(saddle, aleth):
    mantissa = 10_000 * 10**aleth.decimals()
    saddle.deposit(saddle.aleth_token, mantissa, aleth)


def test_withdraw(safe, saddle):
    n_coins = len(saddle.aleth_pool.calculateRemoveLiquidity(0))

    coins = []
    for n in range(n_coins):
        coins.append(saddle.aleth_pool.getToken(n))

    # get safe balance of each token
    before_coin_balances = [
        interface.IERC20Metadata(coin).balanceOf(safe) for coin in coins
    ]

    to_withdraw = saddle.aleth_token.balanceOf(safe)
    saddle.withdraw(saddle.aleth_token, to_withdraw)

    after_coin_balances = [
        interface.IERC20Metadata(coin).balanceOf(safe) for coin in coins
    ]

    # tokens are withdrawn in unknown proportions;
    # compare sum of token balances instead
    assert sum(after_coin_balances) > sum(before_coin_balances)


def test_withdraw_one_coin(safe, saddle, aleth):
    bal_before = aleth.balanceOf(safe)
    mantissa = saddle.aleth_token.balanceOf(safe)

    saddle.withdraw_to_one_coin(saddle.aleth_token, mantissa, aleth)

    assert aleth.balanceOf(safe) > bal_before

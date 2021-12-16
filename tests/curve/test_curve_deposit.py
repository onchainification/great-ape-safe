import pytest


def test_deposit_given_amounts(safe, curve, tripool_lptoken, USDC):
    before_bal_3crv = tripool_lptoken.balanceOf(safe)
    before_bal_usdc = USDC.balanceOf(safe)
    #          DAI   USDC    USDT
    amounts = [0, 1000000000, 0]
    curve.deposit(tripool_lptoken, amounts)

    assert tripool_lptoken.balanceOf(safe) > before_bal_3crv
    assert USDC.balanceOf(safe) < before_bal_usdc
    
def test_deposit_given_token(safe, curve, tripool_lptoken, USDC):
    before_bal_3crv = tripool_lptoken.balanceOf(safe)
    before_bal_usdc = USDC.balanceOf(safe)
    
    amount = 1000000000
    curve.deposit(tripool_lptoken, amount, USDC)

    assert tripool_lptoken.balanceOf(safe) > before_bal_3crv
    assert USDC.balanceOf(safe) < before_bal_usdc

@pytest.mark.xfail
def test_deposit_no_token_specified(curve, tripool_lptoken):
    amount = 1000000000
    curve.deposit(tripool_lptoken, amount)

import pytest


def test_deposit_given_amounts(safe, saddle, alusd):
    before_bal_d4 = saddle.d4_token.balanceOf(safe)
    before_bal_alusd = alusd.balanceOf(safe)

    amount_alusd = 10_000 * 10**alusd.decimals()
    amounts = [amount_alusd, 0, 0, 0]
    saddle.deposit(saddle.d4_token, amounts)

    assert saddle.d4_token.balanceOf(safe) > before_bal_d4
    assert alusd.balanceOf(safe) == before_bal_alusd - amount_alusd


def test_deposit_given_token(safe, saddle, alusd):
    before_bal_d4 = saddle.d4_token.balanceOf(safe)
    before_bal_alusd = alusd.balanceOf(safe)

    amount_alusd = 10_000 * 10**alusd.decimals()
    saddle.deposit(saddle.d4_token, amount_alusd, alusd)

    assert saddle.d4_token.balanceOf(safe) > before_bal_d4
    assert alusd.balanceOf(safe) == before_bal_alusd - amount_alusd


@pytest.mark.xfail
def test_deposit_no_token_specified(saddle):
    amount = 10_000 * 10**18
    saddle.deposit(saddle.d4_token, amount)

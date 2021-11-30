import numpy as np


class Curve():
    def __init__(self, safe):
        self.safe       = safe
        # tokens
        self.crv        = safe.contract('0xD533a949740bb3306d119CC777fa900bA034cd52')
        # contracts
        self.provider   = safe.contract('0x0000000022D53366457F9d5E68Ec105046FC4383')
        self.registry   = safe.contract(self.provider.get_registry())
        # parameters
        self.max_slippage_and_fees = .02


    def _get_coins(self, lp_token):
        # get coin addresses from registry for a specific `lp_token`
        pool = self.registry.get_pool_from_lp_token(lp_token)
        true_length = self.registry.get_n_coins(pool)[0]
        return list(self.registry.get_coins(pool))[:true_length]


    def deposit(self, lp_token, mantissas, asset=None):
        # wrap `mantissas` of underlying tokens into a curve `lp_token`
        # `mantissas` do not need to be balanced in any way
        # if `mantissas` is not a list but an int, `coin` needs to be specified
        # as well, in order to automatically determine correct slot number
        # https://curve.readthedocs.io/exchange-pools.html#StableSwap.add_liquidity
        #
        # TODO: find and route through zaps automatically
        # TODO: could pass dict to mantissas with {address: mantissa} and sort
        #       out proper ordering automatically?
        pool = self.registry.get_pool_from_lp_token(lp_token)
        if type(mantissas) == 'int' and asset is not None:
            mantissa = mantissas
            assert mantissa > 0
            pool = self.registry.get_pool_from_lp_token(lp_token)
            n_coins = self.registry.get_n_coins(pool)[0]
            mantissas = list(np.zeros(n_coins))
            for i, coin in enumerate(self.registry.get_coins(pool)):
                if coin == asset.address:
                    mantissas[i] = mantissa
            # could not find `asset` in `lp_token`
            raise
        assert self.registry.get_n_coins(pool)[0] == len(mantissas)
        expected = self.safe.contract(pool).calc_token_amount(mantissas, 1)
        assert self.safe.contract(pool).add_liquidity(
            mantissas,
            expected * (1 - self.max_slippage_and_fees)
        ).return_value > 0


    def withdraw(self, lp_token, mantissa):
        # unwrap `mantissa` amount of lp_token back to its underlyings
        # (in same ratio as pool is currently in)
        # https://curve.readthedocs.io/exchange-pools.html#StableSwap.remove_liquidity
        pool = self.registry.get_pool_from_lp_token(lp_token)
        n_coins = self.registry.get_n_coins(pool)[0] # note [1] tells us if there is a wrapped coin!
        # TODO: slippage and stuff

        minima = list(np.zeros(n_coins))
        receivables = self.safe.contract(pool).remove_liquidity(mantissa, minima).return_value
        # some pools (eg 3pool) do not return `receivables` as per the standard api
        if receivables is not None:
            assert (np.array(receivables) > 0).all()


    def withdraw_to_one_coin(self, lp_token, mantissa, asset):
        # unwrap `mantissa` amount of `lp_token` but single sided; into `asset`
        # https://curve.readthedocs.io/exchange-pools.html#StableSwap.remove_liquidity_one_coin
        pool = self.registry.get_pool_from_lp_token(lp_token)
        for i, coin in enumerate(self.registry.get_coins(pool)):
            if coin == asset.address:
                expected = self.safe.contract(pool).calc_withdraw_one_coin(mantissa, i)
                receiveable = self.safe.contract(pool).remove_liquidity_one_coin(
                    mantissa,
                    i,
                    expected * (1 - self.max_slippage_and_fees)
                ).return_value
                # some pools (eg 3pool) do not return `receivables` as per the standard api
                if receiveable is not None:
                    assert receiveable > 0
                return
        # could not find `asset` in `lp_token`
        raise

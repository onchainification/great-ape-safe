from great_ape_safe import GreatApeSafe


SAFE    = GreatApeSafe('dev.badgerdao.eth')
USDC    = SAFE.contract('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
WBTC    = SAFE.contract('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599')


def main():
    """example script which deposits all $usdc in safe to aave and all $wbtc to compound"""

    # also take snapshots of the $ausdc and $cwbtc2 tokens
    # snapshot method takes both Contract objects and address strings
    SAFE.take_snapshot([USDC, WBTC, '0xBcca60bB61934080951369a648Fb03DF4F96263C', '0xccF4429DB6322D5C611ee964527D42E5d685DD6a'])

    # initialise aave class; load all its platform specific contracts
    SAFE.init_aave()

    # safe is now aave aware, and can now directly call its tokens
    print('current total supply of $stkaave:', SAFE.aave.stkaave.totalSupply())
    # or its contracts
    print('is the aave lending pool paused?:', SAFE.aave.pool.paused())

    # underlying logic of depositing is taken care of by the aave class
    SAFE.aave.deposit(USDC, USDC.balanceOf(SAFE))

    # again but for compound
    SAFE.init_compound()
    SAFE.compound.deposit(WBTC, WBTC.balanceOf(SAFE))

    # this is a dry run; do not actually try to post to gnosis api
    SAFE.post_safe_tx(post=False)

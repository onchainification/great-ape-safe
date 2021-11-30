"""
Each known protocol has its own ApeSafe compatible class defined below.

Current standarised methods are:
- deposit(underlying, mantissa, <destination>)
- deposit_all(underlying, mantissa, <destination>)
- withdraw(underlying, mantissa, <destination>)
- withdraw_all(underlying, mantissa, <destination>)
- claim_all(<destination>)

Every method *must* make at least one assertion on fork to make sure
the action was successful.
"""

from great_ape_safe.api_safe.aave import Aave
from great_ape_safe.api_safe.compound import Compound
from great_ape_safe.api_safe.convex import Convex
from great_ape_safe.api_safe.curve import Curve

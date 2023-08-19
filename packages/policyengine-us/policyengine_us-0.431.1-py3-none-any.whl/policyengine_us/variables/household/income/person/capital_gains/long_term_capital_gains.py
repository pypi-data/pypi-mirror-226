from policyengine_us.model_api import *


class long_term_capital_gains(Variable):
    value_type = float
    entity = Person
    label = "Long-term capital gains (losses are expressed as negative gains)"
    unit = USD
    documentation = (
        "Net gains made from sales of assets held for more than one year."
    )
    definition_period = YEAR
    reference = dict(
        title="26 U.S. Code § 1222(3)",
        href="https://www.law.cornell.edu/uscode/text/26/1222#3",
    )

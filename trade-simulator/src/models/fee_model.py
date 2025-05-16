class FeeModel:
    def __init__(self, fee_tier):
        self.fee_tier = fee_tier

    def calculate_expected_fees(self, quantity):
        # Rule-based fee model implementation
        if self.fee_tier == 'tier1':
            fee_percentage = 0.001  # 0.1%
        elif self.fee_tier == 'tier2':
            fee_percentage = 0.002  # 0.2%
        elif self.fee_tier == 'tier3':
            fee_percentage = 0.003  # 0.3%
        else:
            raise ValueError("Invalid fee tier")

        expected_fees = quantity * fee_percentage
        return expected_fees
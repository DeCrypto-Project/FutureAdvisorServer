
class ResponseApi:
    def __str__(self, **options):
        return {
            'algorithm': self.algorithm,
            'volatilityPercentage': self.volatilityPercentage,
            'stocks': self.stocks,
            'totalInvestment': self.totalInvestment,
            'date': self.date
        }

    def __init__(self, algorithm, volatility=float('inf'), stocks=None, totalInvestment=float('inf'), date=None):
        if stocks is None:
            stocks = [{}]
        self.algorithm = algorithm
        self.volatilityPercentage = volatility
        self.stocks = stocks
        self.totalInvestment = totalInvestment
        self.date = date

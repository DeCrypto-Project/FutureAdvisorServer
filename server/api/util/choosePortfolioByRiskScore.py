

def choosePortfolioByRiskScore(optionalPortfolios, riskScore):
    if riskScore>0 and riskScore<31:
        return optionalPortfolios['Safest Portfolio']
    if riskScore>30 and riskScore<71:
        return optionalPortfolios['Sharpe Portfolio']
    if riskScore>70:
        return optionalPortfolios['Max Risk Porfolio']
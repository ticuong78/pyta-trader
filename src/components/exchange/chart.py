import MetaTrader5 as mt5


class Chart():
    def __init__(self, symbol, timeFrame):
        """
        Create a chart for the current Symbol and TimeFrame

        :param symbol: Symbol to take prices from in Meta Trader platform
        "param timeFrame: Time Frame to take prices from in Meta Trader platforms
        """
        self.symbol = symbol
        self.timeFrame = timeFrame

        pass

    def establish(self):
        pass
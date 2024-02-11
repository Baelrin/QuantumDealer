import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment

API_KEY = os.environ.get("ALPACA_API_KEY")
API_SECRET = os.environ.get("ALPACA_API_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}


class MLTrader(Strategy):
    """
    Machine Learning Trader Class, responsible for orchestrating the trading algorithm.
    This strategy focuses on sentiment analysis to make trading decisions.
    """

    def initialize(self, symbol: str = "SPY", cash_at_risk: float = .5):
        """
        Initializes the trading strategy with a symbol and how much cash to risk per trade.
        :param symbol: The stock symbol to trade.
        :param cash_at_risk: Fraction of cash to risk on each trade.
        """
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY,
                        secret_key=API_SECRET)

    def position_sizing(self):
        """
        Determines the quantity of stock to buy/sell based on the amount of cash at risk and the stock's last price.
        :return: Tuple containing cash available, the last price of the stock, and the quantity to trade.
        """
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,  0)
        return cash, last_price, quantity

    def get_dates(self):
        """
        Calculates today's date and the date three days prior.
        :return: A tuple of strings representing today's date and the date three days ago in YYYY-MM-DD format.
        """
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        """
        Retrieves news headlines for the symbol within a date range and estimates sentiment.
        :return: A tuple containing the probability and sentiment (positive or negative) of the news.
        """
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol,
                                 start=three_days_prior,
                                 end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment

    def on_trading_iteration(self):
        """
        Executes trading logic on each trading iteration, based on the sentiment analysis of recent news.
        """
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if cash > last_price:
            if sentiment == "positive" and probability > .999:
                if self.last_trade == "sell":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.20,
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order)
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999:
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price=last_price*.8,
                    stop_loss_price=last_price*1.05
                )
                self.submit_order(order)
                self.last_trade = "sell"


start_date = datetime(2020,   1,   1)
end_date = datetime(2023,   12,   31)
broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker,
                    parameters={"symbol": "SPY",
                                "cash_at_risk": .5})
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol": "SPY", "cash_at_risk": .5}
)
# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()

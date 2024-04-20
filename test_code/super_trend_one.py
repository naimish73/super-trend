# https://www.tradingview.com/script/TunYA7oc-Supertrend-1-0-with-Alerts/
# https://www.quantconnect.com/forum/discussion/3383/custom-indicator-in-python-algorithm/p1
from collections import deque
import datetime
from QuantConnect.Indicators import AverageTrueRange
class CalibratedUncoupledProcessor(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 5, 4)  # Set Start Date
        self.SetEndDate(2020, 5, 4)
        self.SetCash(5000)  # Set Strategy Cash
        self.AddEquity("SPY", Resolution.Minute)
        self.spy = RollingWindow[TradeBar](2) # spy trade bar window
        self.atrPeriod = 14
        self.superTrend = SuperTrend('custom', self.atrPeriod) # suepr trend
        self.lastSuperTrendTrend = 0 # the last self.superTrend.Trend

    def OnData(self, data):
        self.spy.Add(data["SPY"])
        if not self.spy.IsReady:  #  not self.superTrend.IsReady
            return 
        self.superTrend.Update(data["SPY"], self.spy[1])
        self.Debug("super trend : {}".format(self.superTrend.Trend))
        if self.lastSuperTrendTrend == -1 and self.superTrend.Trend == 1:
            if self.Portfolio.Invested: 
                self.Liquidate()
            self.SetHoldings("SPY", 1)
            self.Debug("Long")
        if self.lastSuperTrendTrend == 1 and self.superTrend.Trend == -1:
            if self.Portfolio.Invested: 
                self.Liquidate()
            self.SetHoldings("SPY", -1)
            self.Debug("Short")
        self.lastSuperTrendTrend = self.superTrend.Trend
        

class SuperTrend:
    def __init__(self, name, period):
        self.Name = name
        self.IsReady = False
        self.Trend = 0
        self.Up = 0
        self.Down = 0
        self.atr = AverageTrueRange(period, MovingAverageType.Wilders) 
        self.test= 0
        self.lastUp = 0
        self.lastDown = 0
        
    def Update(self, input, lastBar):
        self.atr.Update(input)
        if self.atr.IsReady: 
            self.test = 0
            self.lastUp =self.Up
            self.lastDown = self.Down
            hl2 = ((input.High - input.Low) / 2 ) + input.Low
            self.Up = hl2 + (self.atr.Current.Value * 1.5)
            self.Down = hl2 - (self.atr.Current.Value * 1.5)
            if lastBar.Close > self.lastDown:
                self.Down = max(self.Down, self.lastDown)
                self.test = 1
            if lastBar.Close < self.lastUp:
                self.Up = min(self.Up, self.lastUp)
                self.test = -1
            if self.lastUp != 0 and input.Close > self.lastUp:
                self.Trend = 1
            if self.lastDown != 0 and input.Close < self.lastDown:
                self.Trend = -1
            self.IsReady = self.Trend != 0
# The European Call Option Payoff Model
class CallPayoff:
  
  def __init__(self, strike_price):
    self.strike_price = strike_price
  
  def get_payoff(self, stock_price):
    if stock_price > self.strike_price:
      return stock_price - self.strike_price
    
    return 0
  
# The European Put Option Payoff Model
class PutPayoff:
  
  def __init__(self, strike_price):
    self.strike_price = strike_price
    
  def get_payoff(self, stock_price):
    if stock_price < self.strike_price:
      return self.strike_price - stock_price
    
    return 0
  
# Up and Out Barrier Option
class UpAndOutBarrierPayoff:
  
  def __init__(self, strike_price, barrier_price_level):
    self.strike_price = strike_price
    self.barrier_price_cap = barrier_price_level
    
  def checkBarrier(self, stock_price):
    if stock_price > self.barrier_price_level:
      self.barrier_exercised = True
  
  def get_payoff(self, stock_price):
    if self.barrier_exercised:
      return 0
    
    if stock_price > self.strike_price:
      return stock_price - self.strike_price
    
    return 0
  
# Down and out Barrier Option
class DownAndOutBarrierPayoff:
  
  def __init__(self, strike_price, barrier_price_level):
    self.strike_price = strike_price
    self.barrier_price_level = barrier_price_level
  
  def checkBarreier(self, stock_price):
    if stock_price < self.barrier_price_level:
      self.barrier_exercised = True
  
  def get_payoff(self, stock_price):
    if stock_price < self.strike_price:
      return self.strike_price - stock_price

    return 0
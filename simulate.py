from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from GBM import GBM
from Payoffs import CallPayoff, PutPayoff, UpAndOutBarrierPayoff, DownAndOutBarrierPayoff
import numpy as np
import matplotlib.pyplot as plt

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--initial_price", default=100, type=float, help="Initial price of an asset")
parser.add_argument("-d", "--drift", default=0.08, type=float, help="The drift or expected annual return")
parser.add_argument("-v", "--volatility", default=0.3, type=float, help="The volatility/spread of an asset")
parser.add_argument("-p", "--paths", default=1000, type=int, help="The desired number of generated paths")
args = vars(parser.parse_args())

# Set parameters
initial_price = args['initial_price']
drift = args['drift']
volatility = args['volatility']
n = args['paths']
risk_free_rate = 0.02
tte = 1 # time to expiry in years
interval = 1 / 365 # set interval to one day

# Initialize each process
def init_processes():
  stochastic_processes = []
  for _ in range(n):
    stochastic_processes.append( GBM(initial_price,drift,interval,volatility) )
  return stochastic_processes
  
# Simulate each stochastic process
def simulate_processes(stochastic_processes):
  for process in stochastic_processes:
    duration = tte
    while duration - process.dt > 0:
      process.time_step()
      duration -= process.dt
      
  return stochastic_processes
    
# plot generated paths
def plot_paths(stochastic_processes):
  for process in stochastic_processes:
    x = np.arange(len(process.asset_prices))
    y = process.asset_prices
    plt.plot(x,y)

  plt.title(f'{n} Price Paths : $\mu={drift},\ \sigma={volatility}$')
  plt.xlabel('Days')
  plt.ylabel('Price')
  plt.show()

def estimate_premium(stochastic_processes, payoff_model):
  call_payoffs = []
  for i in range(n):
    payoff_model.reset()
    highest_price = max(stochastic_processes[i].asset_prices)
    payoff_model.check_barrier(highest_price)
    
    end_price = stochastic_processes[i].asset_prices[-1]
    end_price = end_price / ((1 + risk_free_rate)**tte) # account for the present expected value of future cashflow 
    call_payoffs.append( payoff_model.get_payoff(end_price) )

  return np.average(call_payoffs)
  
stochastic_processes = init_processes()
stochastic_processes = simulate_processes(stochastic_processes)

payoff_model = UpAndOutBarrierPayoff(100,130)
print(estimate_premium(stochastic_processes,payoff_model))

plot_paths(stochastic_processes)
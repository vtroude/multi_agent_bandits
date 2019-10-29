import numpy as np
from abc import abstractmethod

class Agent:
	''' Define a set of agents in a double auction game '''

	def __init__(self, budget=0., N=1):
		if type(budget) is not 'array':
			self.profit = budget*np.ones(N).astype('float')
		else:
			self.profit = budget.astype('float')
		self.ask_price = np.zeros(N).astype('float')

	@abstractmethod
	def action(self, price, i=None): pass		# Buy/Sell if it is a buyer or a seller

	def set_ask_price(self, price, i=None):
		if i is None:
			self.ask_price = price
		else:
			self.ask_price[i] = price[i]
	
	def edit_agent(self, new_agent_profit, i):	# Change the agent i
		self.profit[i] = new_agent_profit
		self.ask_price[i] = 0.

class Seller(Agent):
	''' Define a set of sellers who sell a single unit of a product '''

	def action(self, price, i=None):		# Sell
		if i is None:
			self.profit = self.profit + price
		else:
			self.profit[i] = self.profit[i] + price

	def new_product(self, production_cost, i=None):	# Take possesion of an asset
		if i is None:
			self.profit = self.profit - production_cost
		else:
			self.profit[i] = self.profit[i] - production_cost

class Buyer(Agent):
	''' Define a set f buyers who buy a single unit of a product '''

	def action(self, price, i=None):		# Buy
		if i is None:
			self.profit = self.profit - price
		else:
			self.profit[i] = self.profit[i] - price

	def bid_on(self, ask_price, Index, i=None):		# Bid on the assets represented by the Index
		self.set_ask_price(ask_price, i)
		if i is None:
			self.buy_to = Index.astype('int')
		else:
			self.buy_to = int(Index)



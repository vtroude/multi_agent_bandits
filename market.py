from abc import abstractmethod
import numpy as np
import agent as ag

class Market:
	''' Market for a double auction game '''

	def __init__(self, budget, N_agent, assets):
		self.agents = ag.Agent(budget, N_agent)
		self.assets = assets
		self.agents.produce(self.assets)

	@abstractmethod
	def deal_price(self, selling_price, buying_price): pass	# Deal price when a matching happens
	@abstractmethod
	def update_price(self, deal_prices): pass		# New price of the asset

	def matching_mechanisme(self):
		for asset in range(self.assets.N_asset):	# For each assets
			buyers = np.where(self.agents.bid_on[:,asset]>0)[0]	# Set of buyers
			sellers = np.where(self.agents.bid_on[:,asset]<0)[0]	# Set of sellers
			dif = self.agents.ask_price[buyers,asset].reshape(-1,1)-self.agents.ask_price[sellers,asset].reshape(-1,1).T				# Table of price differences
			possible_match = np.where(dif>=0)	# Set ofpotential match
			new_price = []				# Deal price for each match
			while len(dif[possible_match])>0:
				match = np.argmin(dif[possible_match])		# match index
				buyer = buyers[possible_match[0][match]]	# buyer index
				seller = sellers[possible_match[1][match]]	# Seller index
				new_price.append(self.deal_price(self.agents.ask_price[seller,asset], self.agents.ask_price[seller,asset]))	# New price
				self.agents.deal(new_price[-1], buyer, seller, asset)	# make a deal
				self.assets.owner[asset] = np.where(self.assets.owner[asset]==seller, buyer, self.assets.owner[asset])	# edit the owner of the asset
				erase = list(set(np.concatenate((np.where(possible_match[0]==possible_match[0][match])[0], np.where(possible_match[1]==possible_match[1][match])[0]))))
				possible_match = (np.delete(possible_match[0], erase), np.delete(possible_match[1], erase))	# Erase the buyer and the seller of the list of potential match
			if len(new_price)>0:	# Edit the new price of the asset
				self.assets.price[asset] = self.update_price(new_price)

class Market_mdp(Market):
	''' Market using a mean deal price '''

	def deal_price(self, selling_price, buying_price):
		return (buying_price+selling_price)*0.5		# Mean deal price

	def update_price(self, deal_price):
		return float(sum(deal_price))/len(deal_price)	# Mean value of all the deal prices

#########################################################################
''' Test a market '''

def test(N_agent, N_asset, prices):
	assets = ag.Asset(prices, N_asset)
	market = Market_mdp(100., N_agent, assets)
	for agent in range(N_agent):
		for asset in range(market.assets.N_asset):
			if market.agents.own[agent, asset]>0:
				market.agents.bid_on[agent, asset] = -1
				market.agents.ask_price[agent, asset] = 100.*np.random.rand()
			else:
				market.agents.bid_on[agent, asset] = np.random.randint(0,2)
				if market.agents.bid_on[agent, asset] == 1:
					market.agents.ask_price[agent, asset] = 100.*np.random.rand()

	print 'Asset'
	print 'Prices : ', market.assets.price
	print 'Owner : ', market.assets.owner
	print
	print 'Agent'
	print 'Budget : ', market.agents.budget
	print 'Own : '
	print market.agents.own
	print 'bid_on : '
	print market.agents.bid_on
	print 'Ask prices : '
	print market.agents.ask_price
	print

	market.matching_mechanisme()

	print 'Asset'
	print 'Prices : ', market.assets.price
	print 'Owner : ', market.assets.owner
	print
	print 'Agent'
	print 'Budget : ', market.agents.budget
	print 'Own : '
	print market.agents.own
	print 'bid_on : '
	print market.agents.bid_on
	print 'Ask prices : '
	print market.agents.ask_price
	print

#test(10, [2,3], np.array([10., 35.]))











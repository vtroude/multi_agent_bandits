from abc import abstractmethod
import numpy as np
import agent

class Asset:
	''' Define a set of assets in an auction game '''

	def __init__(self, price=0., N=1):
		if type(price) is not 'array':			# Set production cost
			self.price = price*np.ones(N).astype('float')
		else:
			self.price = price.astype('float')
		self.owner = np.zeros(N).astype('int')		# Name of the owner of each assets

	def set_owner(self, name, i=None):
		if i is None:
			self.owner = name
		else:
			self.owner[i] = name
	
	def edit_price(self, price, i=None):
		if i is None:		# Price of the asset after a deal between two agent
			self.price = price
		else:
			self.price[i] = price

class Market:
	''' Market for a double auction game '''

	def __init__(self, N_buyers=1, N_sellers=1, budget=0., price=0.):
		self.buyers = agent.Buyer(budget, N_buyers)	# Set of buyers
		self.sellers = agent.Seller(budget, N_sellers)	# Set of sellers
		self.assets = Asset(price, N_sellers)		# Set of assets
		self.name = np.linspace(1, N_buyers+N_sellers, N_buyers+N_sellers).astype('int')	# name of each agent (Buyers: 1 to N_buyers, Sellers: N_buyers to N_buyers+N_sellers)

		self.sellers.new_product(self.assets.price)	# The sellers produced their assets
		self.assets.set_owner(self.name[N_buyers:])	# Set the owner of eacha assets

	@abstractmethod
	def deal_price(self, selling_price, buying_price): pass	# Deal price when a matching happens

	def exchange(self, b,s):		# After deal the buyer become seller and respectively
		buyer_profit = self.buyers.profit[b]
		self.buyers.edit_agent(self.sellers.profit[s], b)
		self.sellers.edit_agent(buyer_profit, s)
		buyer_name = self.name[b]
		S = s+len(self.buyers.profit)
		self.name[b] = self.name[S]		# The buyer become seller
		self.name[S] = buyer_name	# The seller become buyer
		self.assets.set_owner(self.name[S], s)	# Set the new owner of the asset

	def matching_mechanisme(self):
		for s in range(len(self.sellers.profit)):
			B_s = np.where(self.buyers.buy_to==s)[0]	# Index of buyers interested by the asset s
			if len(B_s)>0:
				b_s = np.where(self.buyers.ask_price[B_s]>=self.sellers.ask_price[s])[0]	# Index of buyers that cover what the seller ask
				if len(b_s)>0:
					b = np.argmin(self.buyers.ask_price[B_s[b_s]])
					b = B_s[b_s[b]]		# Index of the buyer that match with the seller of asset s
					deal = self.deal_price(self.sellers.ask_price[s], self.buyers.ask_price[b])	# Deal price
					self.sellers.action(deal, s)	# Edit the seller profit after the sale 
					self.buyers.action(deal, b)	# Edit the buyer profit after the purchase
					self.assets.edit_price(deal, s)	# Edit the price of the asset
					self.exchange(b,s)		# Transform the seller into a buyer and the buyer into a seller

class Market_mdp(Market):
	''' Market using a mean deal price '''

	def deal_price(self, selling_price, buying_price):
		return (buying_price+selling_price)*0.5		# Mean deal price

#########################################################################
''' Test a market '''

def test(N_b, N_s):
	market = Market_mdp(N_b, N_s, 100., 100.*np.random.rand(N_s))
	market.buyers.bid_on(100.*np.random.rand(N_b), np.random.randint(0, N_s, size=N_b))
	market.sellers.set_ask_price(100.*np.random.rand(N_s))
	print 'Buyers : '
	print np.stack((market.name[:N_b], market.buyers.profit, market.buyers.buy_to+N_b+1, market.buyers.ask_price))
	print
	print'Sellers : '
	print np.stack((market.name[N_b:], market.sellers.profit, market.sellers.ask_price))
	print
	print 'Assets : '
	print np.stack((market.assets.owner, market.assets.price))
	print
	print

	market.matching_mechanisme()
	print 'Buyers : '
	print np.stack((market.name[:N_b], market.buyers.profit))
	print
	print'Sellers : '
	print np.stack((market.name[N_s:], market.sellers.profit))
	print
	print 'Assets : '
	print np.stack((market.assets.owner, market.assets.price))
	print

test(3,3)











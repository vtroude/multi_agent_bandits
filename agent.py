import numpy as np

class Asset:
	''' Define a set of assets in an auction game '''

	def __init__(self, price=0., N=[1]):
		self.N_asset = len(N)			# Number of assets
		self.owner = []				# List of owner of the assets
		for n in range(self.N_asset):
			self.owner.append(np.zeros(N[n]).astype('int'))
		self.price = price*np.ones(self.N_asset)	# Production cost of the assets

class Agent:
	''' Define a set of agents in a double auction game '''

	def __init__(self, budget=0., N=1):
		if type(budget) is not 'array':
			self.budget = budget*np.ones(N).astype('float')
		else:
			self.budget = budget.astype('float')
		self.N_agent = N
		
	def produce(self, asset):
		self.own = np.zeros((self.N_agent, asset.N_asset)).astype('int')
		self.ask_price = np.zeros((self.N_agent, asset.N_asset)).astype('float')
		self.bid_on = np.zeros((self.N_agent, asset.N_asset)).astype('float')
		n = 0
		for i in range(asset.N_asset):
			for j in range(len(asset.owner[i])):
				self.budget[n+j] = self.budget[n+j]-asset.price[i]
				self.own[n+j,i] = 1
				asset.owner[i][j] = n+j
			n = n + len(asset.owner[i])

	def deal(self, deal_price, buyer, seller, asset_i):
		self.budget[buyer] = self.budget[buyer]-deal_price
		self.budget[seller] = self.budget[seller]+deal_price
		self.own[buyer, asset_i] = 1
		self.own[seller, asset_i] = 0
		self.bid_on[[buyer,seller],asset_i] = 0
		self.ask_price[[buyer,seller],asset_i] = 0.

####################################################################"
''' Test asset & agent '''

def test():
	asset = Asset(np.array([10., 13.]), [2, 3])
	print 'Assets'
	print 'N -> ', asset.N_asset
	print 'Price -> ', asset.price
	print
	agent = Agent(100., 10)
	print 'Agent'
	print 'Budget -> ', agent.budget
	print
	agent.produce(asset)
	print 'Book'
	print agent.own
	print 'Budget -> ', agent.budget
	print 'Owned -> ', asset.owner
	print
	agent.deal(12., 9, 0, 0)
	asset.price[0] = 12.
	asset.owner[0] = np.where(asset.owner[0]==0, 9, asset.owner[0])
	print 'Deal'
	print 'Budget -> ', agent.budget
	print agent.own
	print 'Owned -> ', asset.owner
	print 'Price -> ', asset.price


#test()






























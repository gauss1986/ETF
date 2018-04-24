Portfolio optimization toolbox by Lin Gao.

It is designed to have handle mean-variance and various linear optimization using pyomo. Piece-wise linear transaction cost is considered. Notations used follow those in A.H. Chen et al., Chap6 Handbook of portfolio construction, which is included here.

Historical price for the basket of candidate ETF can be downloaded using IQFeed. Subscription to IQFeed is necessary to get access to the data. 

Pyomo and pandas are required python packages. Abstract models are coded in p-etf.py. Model instances are initialized with p-etf.dat. NEOs cloud server is called to run optimization routines. Results returned are in results.yml.

Run "pyomo solve --solver-manager=neos --solver=cbc p-etf.py p-etf.dat" in command line with proper virtual environment to execute the code.

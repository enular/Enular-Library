# Enular Library
 
pip install enular

NOTE: Pre-alpha version (v0.2.3) and development in progress. Expect beta release in late 2022.

The Enular Library contains tools for backtesting, evaluating and visualising algorithmic trading strategies. It allows the user to easily combine indicators with complex operations into strategies, similar to neural networks. It also provides indicators, data sources, and paper trading capabilities. Documentation coming soon. Enular.com

Details:
- Uses Backtrader's Cerebro engine with fixes from Backtrader2
- Data streaming from Yahoo Finance
- Indicator and strategy collection
- Improve accessiblity with simplified architecture
- Highly scalable strategies: extend classes and redefine trade logic
- Live trading capabilities

Architecture:

- 1 category of base indicators (INPUT: market data, OUTPUT: single indicator signal)
    - Indicator library with existing technical analysis indicators

- 3 categories of indicator operations (INPUT: two indicator signals, OUTPUT: single indicator signal):
    - Scalar inputs to scalar output
    - Scalar inputs to boolean output
    - Boolean inputs to boolean output (7 basic logic gates)

- 2 categories of strategy operations (INPUT two indicator signals, OUTPUT: order instructions):
    - Scalar inputs to order instructions
    - Boolean inputs to order instructions (7 basic logic gates)

Development in progress:
- Live trading via IB
- Indicator library
- Strategy library
- Data feed improvements
- Machine learning capabities
- Instructional articles on Medium
- Templates
- Documentation
- User forum
- Resaerch
- Data hosting and supply
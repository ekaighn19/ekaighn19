import yfinance
import plotly.graph_objects as go
import plotly.io as pio
import pandas
from plotly.subplots import make_subplots

ma1 = 0
ma2 = 0
years = 0

#Prompts
tick = input("Which stock would you like to analyze? ")

while ma1 < 1 or ma1 > 365:        #https://www.adamsmith.haus/python/answers/how-to-use-while-not-in-python
    ma1 = int(input("What is the first moving average you would like to analyze? "))
    if ma1 < 1 or ma1 > 365:
        print("Not a valid moving average ")

while ma2 < 1 or ma2 > 365:
    ma2 = int(input("What is the second moving average you would like to analyze? "))
    if ma2 < 2 or ma2 > 365:
        print("Not a valid moving average ")

while years < 1 or years > 30:
    years = int(input("How many years would you like to analyze the data for? "))
    if ma1 < 2 or ma2 > 365:
        print("Not a valid amount of years ")

#Calculating Returns
stock = yfinance.Ticker(str(tick))
spy = yfinance.Ticker('spy')
ndaq = yfinance.Ticker('ndaq')

hist = stock.history(period= str(years)+'y')
spyHist = spy.history(period= str(years)+'y')
ndaqHist = ndaq.history(period= str(years)+'y')

hist.drop(['Dividends','Stock Splits'],inplace=True,axis=1)
hist[str(ma1) + 'MA']=hist[['Close']].rolling(ma1).mean()
hist[str(ma2) + 'MA']=hist[['Close']].rolling(ma2).mean()
hist['Stock Change'] = hist['Close'].pct_change()

stockOpen = hist.iloc[0,0]
stockClose = hist.iloc[-1,-5]
stockReturn = ((stockClose - stockOpen) / stockOpen) * 100
stockReturn = str(round(stockReturn, 2))

spyOpen = spyHist.iloc[0,0]
spyClose = spyHist.iloc[-1,-4]
spyReturn = ((spyClose - spyOpen) / spyOpen) * 100
spyReturn = str(round(spyReturn, 2))

ndaqOpen = ndaqHist.iloc[0,0]
ndaqClose = ndaqHist.iloc[-1,-4]
ndaqReturn = ((ndaqClose - ndaqOpen) / ndaqOpen) * 100
ndaqReturn = str(round(ndaqReturn, 2))

#Calculating Moving Average Return
return1 = 0
return2 = 0

for index, row in hist.iterrows():
    if row[str(ma1) + 'MA'] > row[str(ma2) + 'MA']:
        return1 = return1 + row['Stock Change']
    if row[str(ma2) + 'MA'] > row[str(ma1) + 'MA']:
        return2 = return2 + row['Stock Change']
return1 = str(round(return1 * 100, 2))
return2 = str(round(return2 * 100, 2))

#Graph
pio.templates.default = "plotly_dark"
fig3 = make_subplots(specs=[[{"secondary_y": True}]])           #https://pythoninoffice.com/draw-stock-chart-with-python/
fig3.add_trace(go.Candlestick(x=hist.index,
                              open=hist['Open'],
                              high=hist['High'],
                              low=hist['Low'],
                              close=hist['Close'],
                             ))
fig3.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=int(ma1)).mean(),marker_color='blue',name= str(ma1) + ' Day MA'))
fig3.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=int(ma2)).mean(),marker_color='yellow',name= str(ma2) + ' Day MA'))
fig3.add_trace(go.Bar(x=hist.index, y=hist['Volume'], marker_color='orange',name='Volume'),secondary_y=True)
fig3.update_layout(title={'text':str(tick), 'x':0.5})
fig3.update_yaxes(range=[0,1000000000],secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_layout(xaxis_rangeslider_visible=False)
hist['diff'] = hist['Close'] - hist['Open']
hist.loc[hist['diff']>=0, 'color'] = 'green'
hist.loc[hist['diff']<0, 'color'] = 'red'

fig3.add_annotation(dict(font=dict(color='white',size=15),         #https://stackoverflow.com/questions/62716521/plotly-how-to-add-text-to-existing-figure
                                        x=0.92,
                                        y=0.6,
                                        showarrow=False,
                                        text= tick + ' Return: ' + stockReturn +  '%<br>SPY Return: ' + spyReturn + 
                                        '%<br>Nasdaq Return: ' + ndaqReturn +'%<br><br>' + str(ma1) +'MA > ' + str(ma2) +
                                         'MA Return: ' + str(return1) + '%<br>' + str(ma1) +'MA < ' + str(ma2) +
                                         'MA Return: ' + str(return2) + '%',
                                        textangle=0,
                                        xanchor='left',
                                        xref="paper",
                                        yref="paper"))

fig3.show()



from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

from sklearn.model_selection import train_test_split
from keras.models import load_model



def prepare_lstm_data(data, n_steps):
    x, y = [], []
    for i in range(len(data)):
        end_ix = i + n_steps
        if end_ix > len(data) - 1:
            break
        seq_x, seq_y = data[i:end_ix], data[end_ix]
        x.append(seq_x)
        y.append(seq_y)
    return np.array(x), np.array(y)

def make_prediction(request):

    if request.method=="POST":
        date=request.POST.get('date')
        open=request.POST.get('open')
        model=load_model('LSTM_ONLY_BEST.h5')
        
        new_row={'Date':f'{date}','Open':0,'High':0,'Low':0,'Close':0,'Volume':0,'Change':0}
        # new_row=[f'{date}',None,None,None,None,None,None]
        # if open !="":
        #     print('THERE IS OPEN',open)
        #     row_df=[date,open,None,None,None,None,None]
        print('PREDICT VALUE',new_row)
        data = pd.read_csv('dataset2.csv',header=None,names=["Date","Open","High","Low","Close","Volume","Change"])
        date_column = 'Date'
        price_column = 'Close'
        # data= shuffle(data)
        # data.loc[len(data)]= row_df#['11/30/2023',None,None,None,None,None,None]
        data[date_column] = pd.to_datetime(data[date_column])
        search= pd.to_datetime(date)
        data['date_dif']=abs(data['Date']-search)
        closest=data.iloc[data['date_dif'].idxmin()]
        print('CLOSEST',closest)
        index=data[data['Date']==closest.Date].index[0]
        print('INDEX',index)
        location=index+1
        print('LOCATION',location)
        data=pd.concat([data.loc[:location-1],pd.DataFrame([new_row]),data.loc[location:]]).reset_index(drop=True)
        data.set_index(date_column, inplace=True)
        prices = data[price_column].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        prices_scaled = scaler.fit_transform(prices)
        n_steps = 5
        X, y = prepare_lstm_data(prices_scaled, n_steps)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        # Make predictions using LSTM on the test set
        lstm_predictions = model.predict(X, verbose=0)
        lstm_predicted_price = scaler.inverse_transform(lstm_predictions)[location][0]
        print('PREDICTED',lstm_predicted_price)
        context={

        }
        p='%.3f' % lstm_predicted_price
        context['message']=f'Predicted Closing Price is:N{p}.'
        context['class']='success'
        return render(request,'partials/alert.html',context)

import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Provider, connect } from 'react-redux'
import { createStore } from 'redux'
import SButton from './components/StockButton'
import RStocks from './components/RenderStocks'

const initialState = {
  stocks: []
}

const reducer = (state = initialState, action) => {
  switch(action.type){
    case 'GET_STOCKS':
      return {stocks: fetch('https://ec2-107-23-71-107.compute-1.amazonaws.com/bullstocks')
        .then((resp) => resp.json())
        .then((respJson) => {
          return { stocks: respJson }
        })
        .catch((err) => {
          console.log("GET_STOCKS ERROR", err.message)
          return initialState;
        })}
  }
  return state
}

const store = createStore(reducer)

function App() {
  return (
    <Provider store={store}>
      <SButton/>
    </Provider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default App

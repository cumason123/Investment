import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import SButton from './components/StockButton'
import RStocks from './components/RenderStocks'

function App() {
  return (
    <SButton/>
  );
}

const styles = StyleSheet.create({
  // hellobro
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default App

import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import {connect} from "react-redux";
import { bindActionCreators } from 'redux';

export default class SButton extends React.Component {

  state = {
    stocks: ['APPLE','BANNANA']
  }
  constructor(props) {
    super(props)
  };
  genStocks = () => {
    console.log('genStocks called')
    let data = fetch('http://ec2-107-23-71-107.compute-1.amazonaws.com/bullstocks')
      .then(response => response.json())
      .then(json => {
        this.setState({stocks: json.toString()})
      })
      .catch(err => err.message)
  }

  render(){
 
    return(
      <View style={styles.container}>
        <Button onPress={this.genStocks} title='Click Me'/>
        <Text>{this.state.stocks}</Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});


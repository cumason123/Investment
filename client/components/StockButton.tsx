import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import {connect} from "react-redux";
import { bindActionCreators } from 'redux';
import RStocks from './RenderStocks';

export default class SButton extends React.Component {

  state = {
    stocks: ['APPLE','BANNANA'],
    render: <Text>N/A</Text>
  }
  constructor(props) {
    super(props)
  };
  genStocks = () => {
    console.log('genStocks called')
    let data = fetch('http://ec2-107-23-71-107.compute-1.amazonaws.com/bullstocks')
      .then(response => response.json())
      .then(json => {
        json = json.map((item) => ({'stock': item}))
        json = {stocks: json}
        this.setState({ stocks: json, render: <RStocks {...json}/>})
      })
      .catch(err => err.message)
  }

  render(){
 
    return(
      <View style={styles.container}>
        <Button onPress={this.genStocks} title='Click Me'/>
        {this.state.render}
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


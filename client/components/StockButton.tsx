import React from 'react';
import { StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native';
import { connect } from 'react-redux'

class SButton extends React.Component {

  render(){

    return (
        <View style={styles.container}>
          <View style={{ flexDirection: 'row', width: 120, justifyContent: 'space-around'}}>
            <Button title='Get' onPress={()=>this.props.getstocks()}>
              <Text>Get</Text>
            </Button>
            <Text>{JSON.stringify(this.props.stocks)}</Text>
          </View>
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

function mapStateToProps(state) {
    console.log('StockButton.mapStateToProps: ', state)
    if (state == undefined) {
      return { stocks:[] }
    }
    return {
        stocks: state.stocks
    }
}

function mapDispatchToProps(dispatch) {
    return {
        getstocks: () => dispatch({ type: 'GET_STOCKS' }),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SButton)

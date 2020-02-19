import React from 'react';
import { StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native';
import { connect } from 'react-redux'
import axios from 'axios'
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
    if (state == undefined) {
      console.log("Undefined mapStateToProps")
      return { stocks:[] }
    }
    console.log("Mapping: ", state)
    return {
        stocks: state.stocks
    }
}

function mapDispatchToProps(dispatch) {
  console.log('mapDispatchToProps')
    return {
        getstocks: () => dispatch({ 
          type: 'GET_STOCKS', 
          stocks: axios.get('http://ec2-107-23-71-107.compute-1.amazonaws.com/bullstocks')
            .then((response) => response.data)
            .catch((err) => console.log(err.message)) 
        }),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SButton)

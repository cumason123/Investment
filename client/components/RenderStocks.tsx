import React from 'react';
import { FlatList, StyleSheet, Text, View } from 'react-native';

export default class RStocks extends React.Component {
	constructor(props) {
		super(props);
	}

	render(){
		const renderStocks = (item, index) => {
			return <Text>{item}</Text>
		}
		return(
			// <Text>{this.props.stocks.toString()}</Text>
			<FlatList data={this.props.stocks}   
				renderItem={({item}) => <Text>{item.stock}</Text>}>
			
			</FlatList>
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
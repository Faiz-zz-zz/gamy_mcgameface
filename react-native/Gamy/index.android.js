/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  TextInput
} from 'react-native';
import Moment from 'moment';
import 'moment-range';

class Gamy extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      something: 'Initial',
      currentEvent: '',
    };
  }

  componentDidMount() {
    fetch("http://localhost:8000/get_current_events")
    .then(response => response.json())
    .then(json => {
      console.log(json)
    })
  }

  sendEmail(email) {
    fetch("localhost:8000/")
  }

  render() {
    return (
      <View>
        <Text>
          {`Active Event: ${this.state.currentEvent}`}
        </Text>
        <TextInput
          style={{height: 40, borderColor: 'gray', borderWidth: 1}}
          onChangeText={(text) => this.setState({text})}
          placeholder={"Enter your email"}
          value={this.state.text}
          autoFocus={true}
          returnKeyType={"send"}
          onSubmitEditing={(event) => this.setState({ something: event.nativeEvent.text })}
          keyboardType={"email-address"}
        />
        <Text>
          {this.state.something}
        </Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});

AppRegistry.registerComponent('Gamy', () => Gamy);

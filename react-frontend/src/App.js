import React, { Component } from 'react';
import axios from 'axios';
import './App.css';

class PinField extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: ''
    };
  }

  updateInputValue(evt) {
    this.setState({
      inputValue: evt.target.value
    });
  }

  onPinSubmit() {
    axios.get('http://127.0.0.1:5000/verify/' + this.state.inputValue)
      .then(res => {
        // display the result in some thing below this
        console.log(res);
      })
  }

  render() {
    return (
      <div className="PinField">
        <input value={this.state.inputValue} type="text" name="pin" onChange={evt => this.updateInputValue(evt)}/>
        <button onClick={() => this.onPinSubmit()}>
          Submit
        </button>
      </div>
    );
  }
}

class TwitterLoginButton extends Component {
  authenticate() {
    axios.get('http://127.0.0.1:5000/')
      .then(res => {
        // hide the login button and show the text field with a submit button to input the pin
      })
  }

  render() {
    return (
      <button onClick={() => this.authenticate()}>
        Log in with Twitter
      </button>
    );
  }
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <TwitterLoginButton />
        <PinField />
      </div>
    );
  }
}

export default App;

import React, { Component } from 'react';
import axios from 'axios';
import './App.css';

class TwitterLoginButton extends Component {
  authenticate() {
    axios.get('http://127.0.0.1:5000/', {withCredentials: true})
      .then(res => {
        // prepare for the callback from the authentication?
        console.log(res);
        window.location.replace(res.data);
      });
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
      </div>
    );
  }
}

export default App;

import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import axios from 'axios';
import './App.css';

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = {account: 'loading'};
  }

  componentDidMount() {
    var queryString = this.props.location.search;
    var regex = /[?&]([^=#]+)=([^&#]*)/g,
      url = queryString,
      params = {},
      match;
    while(match = regex.exec(url)) {
      params[match[1]] = match[2];
    }
    var verifier = params['oauth_verifier'];
    var obj = {
      params: {oauth_verifier: verifier},
      withCredentials: true,
    };

    axios.get('https://twisimilar.herokuapp.com/verify', obj)
      .then(res => {
        this.setState({account: res.data.account[0]});
      });
  }

  render() {
    return (
      <div>
        {this.state.account === 'loading' ? <div className='ui active massive inline inverted loader' /> : <p>Your most similar top 10 Twitter account is: {this.state.account}</p>}
      </div>
    );
  }
}

class TwitterLoginButton extends Component {
  authenticate() {
    axios.get('https://twisimilar.herokuapp.com/', {withCredentials: true})
      .then(res => {
        window.location.replace(res.data);
      });
  }

  render() {
    return (
      <button className='ui button' onClick={() => this.authenticate()}>
        Log in with Twitter
      </button>
    );
  }
}

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Route exact path="/TwiSimilar" component={TwitterLoginButton} />
          <Route path="/TwiSimilar/result" component={Result} />
        </div>
      </Router>
    );
  }
}

export default App;

import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import axios from 'axios';
import './App.css';
const qs = require('query-string');

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = {account: 'loading'};
  }

  componentDidMount() {
    var verifier = qs.parse(this.props.location.search).oauth_verifier;
    var obj = {
      params: {oauth_verifier: verifier},
      withCredentials: true,
      validateStatus: (status) => status === 6
    };

    axios.get('https://twisimilar.herokuapp.com/verify', obj)
      .then(res => {
        this.setState({account: res.data});
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
      <button class='ui button' onClick={() => this.authenticate()}>
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
          <Route exact path="/" component={TwitterLoginButton} />
          <Route path="/result" component={Result} />
        </div>
      </Router>
    );
  }
}

export default App;

import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import axios from 'axios';
import './App.css';
const qs = require('query-string');

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = {account: ''};
  }

  componentDidMount() {
    var verifier = qs.parse(this.props.location.search).oauth_verifier;
    var obj = {
      params: {oauth_verifier: verifier},
      withCredentials: true,
      validateStatus: (status) => status === 6
    };

    axios.get('http://127.0.0.1:5000/verify', obj)
      .then(res => {
        this.setState({account: res.data});
      });
  }

  render() {
    return (
      // display the account name that is returned here from the state
      <p>{this.state.account}</p>
    );
  }
}

class TwitterLoginButton extends Component {
  authenticate() {
    axios.get('http://127.0.0.1:5000/', {withCredentials: true})
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
        <div className="Outer">
          <div className="App">
            <Route exact path="/" component={TwitterLoginButton} />
            <Route path="/result" component={Result} />
          </div>
        </div>
      </Router>
    );
  }
}

export default App;

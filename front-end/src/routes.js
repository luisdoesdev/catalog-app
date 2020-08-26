import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";


import Home from './views/Home.js'

function Routes() {
  return (
    <Router>
  
      <Switch>
        <Route path="/" exact component={Home}/>
        <Route path="/will-match" component={WillMatch}/>
        <Route component={NoMatch} />
      </Switch>
    
    </Router>
  );
}

function NoMatch(){
  return <h1>#Not Found <Link to="/"> return Home</Link></h1>
}


function WillMatch(){
  return <h1>#willMatch</h1>
}

export default Routes;

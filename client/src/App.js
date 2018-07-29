import React, { Component } from 'react';
import './App.css';
import SearchPage from './components/searchpage';
import {BrowserRouter, Route} from 'react-router-dom';
import ItemPage from './components/itempage';

class App extends Component {   
    render(){
        return(
            <BrowserRouter>
                <div>
                    {/*This is how we add a new route to the website*/}
                    <Route exact={true} path='/' render={() => (
                        <div className="App">
                            <SearchPage/>
                        </div>
                    )}/>
                    <Route exact={true} path='/item' render={() => (
                        <div className="App">
                            <ItemPage/>
                        </div>
                    )}/>

                </div>
            </BrowserRouter>
        );
    }// end render
}//end App

export default App;

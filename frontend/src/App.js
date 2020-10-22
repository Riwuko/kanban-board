import React from 'react';
import Registration from './components/Registration';
import {BrowserRouter, Route} from 'react-router-dom';

const App = () => {
    return (
    <BrowserRouter>
    <Route path="/register" component={Registration} />
    </BrowserRouter>
    )
};

export default App;

import React from 'react';
import './App.css';
import Stocks from './Stocks';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';

function HomePage() {
    return <div>Welcome to the homepage!</div>;
}

function App() {
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    <nav>
                        <ul>
                            <li>
                                <Link to="/">Home</Link>
                            </li>
                            <li>
                                <Link to="/stocks">Stocks</Link>
                            </li>
                        </ul>
                    </nav>

                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/stocks" element={<Stocks />} />
                    </Routes>
                </header>
            </div>
        </Router>
    );
}

export default App;

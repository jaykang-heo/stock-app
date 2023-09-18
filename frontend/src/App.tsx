import React from 'react';
import './App.css';
import Stocks from './Stocks';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import Blogs from './Blogs';
import PersonalFinance from './PersonalFinance';


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
                            <li>
                                <Link to="/blogs">Blogs</Link> {/* New Link for Blogs */}
                            </li>
                            <li>
                                <Link to="/personal-finance">Personal Finance</Link> {/* New Link for Blogs */}
                            </li>
                        </ul>
                    </nav>

                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/stocks" element={<Stocks />} />
                        <Route path="/blogs" element={<Blogs />} /> {/* New Route for Blogs */}
                        <Route path="/personal-finance" element={<PersonalFinance />} /> {/* New Route for Blogs */}
                    </Routes>
                </header>
            </div>
        </Router>
    );
}


export default App;

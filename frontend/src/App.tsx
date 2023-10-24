import React from 'react';
import './App.css';
import Stocks from './Stocks';
import { BrowserRouter as Router, Route, NavLink, Routes } from 'react-router-dom';
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
                                <NavLink to="/" className={({ isActive }) => isActive ? "active" : ""} end>Home</NavLink>
                            </li>
                            <li>
                                <NavLink to="/stocks" className={({ isActive }) => isActive ? "active" : ""}>Stocks</NavLink>
                            </li>
                            <li>
                                <NavLink to="/blogs" className={({ isActive }) => isActive ? "active" : ""}>Blogs</NavLink>
                            </li>
                            <li>
                                <NavLink to="/personal-finance" className={({ isActive }) => isActive ? "active" : ""}>Personal Finance</NavLink>
                            </li>
                        </ul>
                    </nav>

                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/stocks" element={<Stocks />} />
                        <Route path="/blogs" element={<Blogs />} />
                        <Route path="/personal-finance" element={<PersonalFinance />} />
                    </Routes>
                </header>
            </div>
        </Router>
    );
}


export default App;

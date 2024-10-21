// src/App.js
import React from 'react';
import SearchForm from './SearchForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Maillog Search</h1>
        <SearchForm />
      </header>
    </div>
  );
}

export default App;

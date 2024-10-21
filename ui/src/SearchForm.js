// src/SearchForm.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Импортируем стили

const SearchForm = () => {
  const [email, setEmail] = useState('');
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/v1/search`, { email });
      const { items, total } = response.data;
      if (total === 0) {
        setMessage('По вашему запросу ничего не найдено');
      } else if (total > 100) {
        setMessage('Количество найденных строк превышает 100');
      } else {
        setMessage('');
      }
      setResults(items);
    } catch (error) {
      console.error('Error fetching search results', error);
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <label>
          Адрес получателя:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <button type="submit">Поиск</button>
      </form>
      {message && <p>{message}</p>}
      <div className="results-container">
        <table className="results-table">
          <thead>
            <tr>
              <th width={'15%'}>Дата</th>
              <th>Лог</th>
            </tr>
          </thead>
          <tbody>
            {results.map((item, index) => (
              <tr key={index}>
                <td nowrap={true}>{item.date}</td>
                <td>{item.log}</td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
    </div>
  );
};

export default SearchForm;

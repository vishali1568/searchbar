import React, { useState, useEffect } from 'react';
import { Country } from '../types/Country'; // Assume we have a Country type defined
import styles from './SearchBar.module.css';

const SearchBar: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState<Country[]>([]);
  const [countries, setCountries] = useState<Country[]>([]);

  useEffect(() => {
    // Fetch countries data from API or load from a file
    // For now, we'll use a placeholder
    const fetchCountries = async () => {
      // TODO: Replace with actual API call or data loading
      const data = [
        { name: 'United States', capital: 'Washington, D.C.' },
        { name: 'United Kingdom', capital: 'London' },
        // ... more countries
      ];
      setCountries(data);
    };
    fetchCountries();
  }, []);

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setSearchTerm(value);

    if (value.length > 0) {
      const filteredSuggestions = countries.filter(
        (country) =>
          country.name.toLowerCase().includes(value.toLowerCase()) ||
          country.capital.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filteredSuggestions);
    } else {
      setSuggestions([]);

    }
  };

  return (
    <div className={styles.searchContainer}>
      <input
        type="text"
        placeholder="Search for countries or capitals..."
        value={searchTerm}
        onChange={handleSearch}
        className={styles.searchInput}
      />
      {suggestions.length > 0 && (
        <ul className={styles.suggestions}>
          {suggestions.map((country, index) => (
            <li key={index} className={styles.suggestionItem}>
              {country.name} - {country.capital}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBar;
export default SearchBar;
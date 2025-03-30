import { useState } from 'react';

export function useShortener() {
  const [shortenedUrl, setShortenedUrl] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const shorten = async ( original_url, prefix ) => {
    setLoading(true);
    setError(null);
    setShortenedUrl('');

    console.log("Me llego: ", original_url, ". Y tambien: ", prefix);

    const payload = prefix
      ? { original_url, prefix }
      : { original_url };

    try {
      const response = await fetch('http://localhost:8000/url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Error al acortar la URL');
      const data = await response.json();
      console.log(data)
      setShortenedUrl(data.short_url);
      setExpirationDate(data.expiration_date);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'Ocurrió un error');
    } finally {
      setLoading(false);
    }
  };

  return {
    shortenedUrl,
    expirationDate,
    loading,
    error,
    shorten,
  };
}

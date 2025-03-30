import React, { useState, useEffect } from "react";
import { useShortener } from "../hooks/useShortener";
import CopyIcon from "../assets/icons/copyIcon";

function Home() {
  const [longUrl, setLongUrl] = useState("");
  const [prefix, setPrefix] = useState("");
  const [shortUrl, setshortUrl] = useState(null);
  const [localDate, setLocalDate] = useState(null);
  const [prefixError, setPrefixError] = useState(null);

  const { shortenedUrl, expirationDate, loading, error, shorten } = useShortener();

  const handlePrefixChange = (e) => {
    const value = e.target.value;
    const regex = /^[a-zA-Z0-9-]*$/; // Only letters, numbers and hyphens are allowed.
    if (value && !regex.test(value)) {
      setPrefixError("Prefix can only contain letters, numbers, and hyphens.");
    } else {
      setPrefixError(null);
    }
    setPrefix(value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    shorten(longUrl, prefix);
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shortenedUrl);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };

  useEffect(() => { // Change UTC to Local Date
    if (expirationDate) {
      console.log(expirationDate);
      const utcDate = new Date(expirationDate);
      const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        timeZoneName: 'short',
      };
      const date = utcDate.toLocaleString('en-US', options);
      setLocalDate(date);
      console.log(localDate)
    }
  }, [expirationDate]);

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-gray-100 py-10 px-10">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold">URL Shortener</h1>
        <p className="text-lg text-gray-600 mt-2">
          This page allows you to shorten any long URL and share it easily.
        </p>
      </div>

      <div className="border p-6 rounded-lg shadow-lg bg-white w-96">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="longUrl" className="block text-sm font-medium text-gray-800">
              Paste your long link here(e.g. https://www.example.com)
            </label>
            <input
              type="url"
              id="longUrl"
              placeholder="https://www.example.com"
              className="mt-1 p-2 border rounded-lg w-full"
              value={longUrl}
              onChange={(e) => setLongUrl(e.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="prefix" className="block text-sm font-medium text-gray-800">
              Add a prefix (Optional)
            </label>
            <input
              type="text"
              id="prefix"
              className="mt-1 p-2 border rounded-lg w-full"
              value={prefix}
              onChange={handlePrefixChange}
            />
            {prefixError && <p className="text-red-500 text-sm mt-2">{prefixError}</p>}
          </div>

          <button
            type="submit"
            style={{
              backgroundColor: !!prefixError || loading || shortenedUrl ? '#d1d5db' : '#3b82f6',
              color: 'white',
              padding: '0.5rem',
              width: '100%',
              borderRadius: '0.375rem',
              transition: 'background-color 0.3s ease',
              cursor: !!prefixError || loading || shortenedUrl ? 'not-allowed' : 'pointer',
            }}
            onMouseEnter={(e) => {
              if (!(!!prefixError || loading || shortenedUrl)) {
                e.target.style.backgroundColor = '#2b72e6';
              }
            }}
            onMouseLeave={(e) => {
              if (!(!!prefixError || loading || shortenedUrl)) {
                e.target.style.backgroundColor = '#3b82f6';
              }
            }}
            disabled={!!prefixError || loading || shortenedUrl}
          >
            {loading ? 'Generating your URL' : shortenedUrl ? 'Done' : 'Shorten URL'}
          </button>
        </form>

        {/* Shortened link display */}
        {shortenedUrl && (
          <div className="mt-4 p-4 border rounded-lg">
            <label className="block text-sm font-medium text-gray-800">
              Here is your shortened link:
            </label>

            {/* Clickable shortened link */}
            <div className="mt-2 flex items-center">
              <a
                href={shortenedUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="h-10 text-blue-500 hover:underline border border-blue-500 px-2 py-1 truncate w-64 rounded-l-lg" // Borde azul, padding y truncar si es largo
              >
                {shortenedUrl}
              </a>

              {/* Copy to clipboard button */}
              <button
                onClick={copyToClipboard}
                style={{
                  height: '2.5rem',
                  paddingLeft: '1rem',
                  paddingRight: '1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  borderRadius: '0.375rem',
                  border: 'none',
                  transition: 'background-color 0.3s ease',
                }}
                onMouseEnter={(e) => {
                  e.target.style.backgroundColor = '#2563eb';
                }}
                onMouseLeave={(e) => {
                  e.target.style.backgroundColor = '#3b82f6';
                }}
                onKeyPress={(e) => e.key === 'Enter' && copyToClipboard()}
              >
                Copy
              </button>
            </div>

            {/* Expiration date */}
            {localDate && (
              <div className="mt-2 text-sm text-gray-600">
                <p>
                  The link will expire on: <strong>{localDate}</strong>
                </p>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}

export default Home;

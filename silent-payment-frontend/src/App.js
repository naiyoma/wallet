import React, { useState } from 'react';
import axios from 'axios';
import QRCode from 'qrcode.react';
import './index.css'; // Make sure this import is here

function App() {
  const [address, setAddress] = useState('');

  const handleGenerateAddress = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/generate-silent-payment-address/');
      setAddress(response.data.address);
    } catch (error) {
      console.error('There was an error generating the silent payment address!', error);
    }
  };

  return (
    <div className="container mx-auto px-4  flex flex-col items-center justify-center min-h-screen">
      <header className="App-header text-center">
        <h1 className="text-4xl font-bold mb-8">Silent Payment Test Generator</h1>
        {/* <button 
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4" 
          onClick={handleGenerateAddress}>
          Receive
        </button> */}
        
<button type="button" 
        class="py-2.5 px-12 me-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-full border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
        onClick={handleGenerateAddress}>
        Receive
        </button>
<button type="button" 
        class="py-2.5 px-16 me-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-full border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
        onClick={handleGenerateAddress}>
        Send
        </button>

        {address && (
          <div className="mt-4 p-2 bg-gray-700 rounded">
            <p className="text-white mb-4">Silent Payment Address: {address}</p>
            <QRCode value={address} />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;

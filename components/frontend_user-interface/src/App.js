import React, { useState } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('image', selectedFile);
  
    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        alert('Image uploaded successfully!');
      } else {
        throw new Error('Failed to upload image.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error uploading image.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Image Uploader</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Upload</button>
        </form>
      </header>
    </div>
  );
}

export default App;
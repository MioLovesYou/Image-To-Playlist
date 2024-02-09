const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const fetch = require('node-fetch');
const FormData = require('form-data'); // Import the form-data module

const upload = multer({ dest: 'uploadsCache/' });
const app = express();
const port = 4000; // Use port 4000 for Node.js server to avoid conflict with Python server

app.use(cors()); // Enable CORS

app.post('/upload', upload.single('image'), async (req, res) => {
  console.log(req.file); // You can see the uploaded file details in your console

  // Prepare the formData and append the file
  const formData = new FormData();
  formData.append('image', fs.createReadStream(req.file.path));

  try {
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
      headers: formData.getHeaders(), // Now this should work as expected
    });

    // After the image is sent to the Python server, delete it from the Node server
    fs.unlink(req.file.path, (err) => {
      if (err) {
        console.error("Error deleting the file", err);
        return res.status(500).send('Failed to delete the temporary file.');
      }
      console.log("File deleted successfully");
    });

    if (response.ok) {
      res.send('Image uploaded and processed successfully.');
    } else {
      res.status(response.status).send('Failed to process image.');
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Error uploading image.');
  }
});

app.listen(port, () => console.log(`Node.js server running on port ${port}`));

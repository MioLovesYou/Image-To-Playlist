const express = require('express');
const multer = require('multer');
const cors = require('cors');

const upload = multer({ dest: 'uploads/' });
const app = express();
const port = 5000;

app.use(cors()); // Enable CORS

app.post('/upload', upload.single('image'), (req, res) => {
  console.log(req.file); // You can see the uploaded file details in your console
  res.send('File uploaded successfully.');
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
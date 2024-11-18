require('dotenv').config();
const port = process.env.PORT || 3000;

const express = require('express');
const app = express();

const birdsRoute = require('./routes/Birds')

app.use('/birds', birdsRoute)

app.get('/test', (req, res) => {
    res.json({ok: true});
});

app.listen(port, () => console.log(`Server is now listening on port ${port}}`));
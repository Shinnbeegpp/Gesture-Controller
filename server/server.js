const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(cors());

app.use(express.json());

const configPath = path.join(__dirname, '..', 'config.json');

app.get('/api/config', (req, res) => {
    fs.readFile(configPath, 'utf8', (err, data) => {
        if (err) {
            console.error("Error reading config:", err);
            return res.status(500).json({ error: "Failed to read configuration file." });
        }
        res.json(JSON.parse(data));
        });
});

app.post('/api/config', (req, res) => {
    const newConfig = req.body;
    const jsonString = JSON.stringify(newConfig, null, 2);

    fs.writeFile(configPath, jsonString, 'utf8', (err) => {
        if (err) {
            console.error("Error writing config:", err);
            return res.status(500).json({ error: "Failed to save configuration." });
        }
        res.json({ message: "Configuration successfully updated!" });
    });
});

app.listen(PORT, () => {
    console.log(`Backend API Server running at http://localhost:${PORT}`);
});
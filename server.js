const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const app = express();

app.use(bodyParser.json());
app.use(express.static('public')); // Serves index.html and app.js

app.post('/search', (req, res) => {
    const player = req.body.player;

    const py = spawn('C:\\Python312\\python.exe', ['player_script.py', player]);

    let output = '';
    py.stdout.on('data', data => output += data.toString());

    py.stderr.on('data', data => console.error('Python error:', data.toString()));

    py.on('close', () => {
        res.json({ output });
    });
});

app.post('/search-team', (req, res) => {
    const team = req.body.team;
    const type = req.body.type;

    console.log("REQ BODY:", req.body);
    console.log(`Running script with args: ${team}, ${type}`);

    const py = spawn('C:\\Python312\\python.exe', ['team_script.py', team, type]);
  
    let output = '';
    py.stdout.on('data', data => { output += data.toString(); });

    py.stderr.on('data', data => console.error(data.toString()));
  
    py.on('close', () => {
      res.json({ output });
    });
  });
  

app.listen(3000, () => console.log('Server running at http://localhost:3000'));

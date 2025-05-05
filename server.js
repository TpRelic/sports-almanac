const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const app = express();

app.use(bodyParser.json());
app.use(express.static('public'));

const streamlitProcess = spawn('C:\\Python312\\python.exe', ['-m', 'streamlit', 'run', 'test_frontend.py', '--server.headless', 'true'], {
    detached: true,
    stdio: 'ignore' 
});
  
streamlitProcess.unref();
console.log('Streamlit app started in background.');

app.post('/search', (req, res) => {
    const player = req.body.player;
    const type = req.body.type

    //console.log("REQ BODY:", req.body);
    //console.log(`Running script with args: ${player}, ${type}`);

    const py = spawn('C:\\Python312\\python.exe', ['player_script.py', player, type]);

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

    //console.log("REQ BODY:", req.body);
    //console.log(`Running script with args: ${team}, ${type}`);

    const py = spawn('C:\\Python312\\python.exe', ['team_script.py', team, type]);
  
    let output = '';
    py.stdout.on('data', data => { output += data.toString(); });

    py.stderr.on('data', data => console.error('Python error:', data.toString()));
  
    py.on('close', () => {
      res.json({ output });
    });
  });
  
app.post('/analyze', (req, res) => {
    const htmlTables = req.body.table;

    const py = spawn('C:\\Python312\\python.exe', ['analyze.py']);

    py.stdin.write(htmlTables);
    py.stdin.end();

    //console.log("REQ BODY:", req.body);

    let result = '';
    py.stdout.on('data', data => result += data.toString());

    py.stderr.on('data', data => console.error('Python error:', data.toString()));

    py.on('close', () => {
        res.json({ output: result });
    });
});

app.get('/shutdown', (req, res) => {
    console.log('Shutting down...');
    streamlitProcess.kill();
    process.exit(0);
  });

app.listen(3000, () => console.log('Server running at http://localhost:3000'));

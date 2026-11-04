const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/start-bot', (req, res) => {
    const { login, password, server, symbol, lot } = req.body;

    console.log(`[Titan Bot] Trigger received for Weltrade Account: ${login} on server ${server}`);

    const command = `python3 bot_executor.py --login ${login} --password "${password}" --server "${server}" --symbol "${symbol}" --lot ${lot || 0.01}`;
    
    exec(command, (err, stdout, stderr) => {
        if (err) {
            console.error(`Execution error: ${err.message}`);
            return;
        }
        console.log(`Bot Output:\n${stdout}`);
    });

    res.json({ success: true, message: `Titan Bot successfully launched for Weltrade Account ${login}! Running 24/7.` });
});

app.listen(3000, '0.0.0.0', () => {
    console.log('Titan Dashboard running live on http://YOUR_VPS_IP:3000');
});

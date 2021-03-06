let express = require('express');
let app = express();
let http = require('http').createServer(app);
let io = require('socket.io')(http);
let PythonShell = require('python-shell');

app.use(express.static(__dirname + '/node_modules'));

app.get('/', (req, res) => res.sendFile(__dirname + '/index.html'));

io.on('connection', socket => {
    socket.on('request', args => {
        PythonShell.run('transpiler.py', {args}, (err, res) => {
            if (err) socket.emit('syntax error', err);
            else socket.emit('response', res || []);
        });
    });
});

http.listen(process.env.PORT || 3000, process.env.IP);

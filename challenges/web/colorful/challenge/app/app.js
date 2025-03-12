const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const session = require('express-session');
const crypto = require('crypto');
const path = require('path');

const app = express();
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use('/public', express.static(path.join(__dirname, 'public')));


app.use(express.urlencoded({ extended: true }));

// Session setup
app.use(session({
    secret: crypto.randomBytes(24).toString('hex'),
    resave: false,
    saveUninitialized: true,
}));

// SQLite database connection
const db = new sqlite3.Database('./users.db');


// Initialize database
function initDb() {
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        favorite_color TEXT,
        is_admin INTEGER DEFAULT 0
    )`);

    db.run(`CREATE TABLE IF NOT EXISTS notes (
        id TEXT PRIMARY KEY,
        content TEXT NOT NULL,
        user_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )`);
    const adminUsername = process.env.["ADMIN_USERNAME"];
    const adminPassword = process.env["ADMIN_PASSWORD"];
    const hashedPassword = crypto.createHash('sha256').update(adminPassword).digest('hex');
    const adminId = generateUUID();
    
    db.get('SELECT * FROM users WHERE username = ?', [adminUsername], (err, user) => {
        if (!user) {
            db.run('INSERT INTO users (id, username, password, is_admin) VALUES (?, ?, ?, ?)', 
                [adminId, adminUsername, hashedPassword, 1]);
        }
    });
}



initDb();

function generateUUID() {
    return crypto.randomBytes(16).toString('hex');
}

// Routes

// Register route
app.get('/register', (req, res) => {
    res.render('register');
});

// Register route
app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', (req, res) => {
    const { username, password, favorite_color } = req.body;

    if (typeof username !== 'string' || typeof password !== 'string') {
        return res.send('Error');
    }

    const hashedPassword = crypto.createHash('sha256').update(password).digest('hex');
    const userId = generateUUID();

    db.run('INSERT INTO users (id, username, password, favorite_color) VALUES (?, ?, ?, ?)', 
        [userId, username, hashedPassword, favorite_color || 'Unknown'], 
        function(err) {
            if (err) {
                return res.send('Username already taken!');
            }
            res.redirect('/login');
        }
    );
});

// Login route
app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;

    if (typeof username !== 'string' || typeof password !== 'string') {
        return res.send('Error');
    }

    const hashedPassword = crypto.createHash('sha256').update(password).digest('hex');

    db.get('SELECT * FROM users WHERE username = ? AND password = ?', [username, hashedPassword], (err, user) => {
        if (err || !user) {
            return res.send('Invalid credentials');
        }

        req.session.user_id = user.id;
        req.session.username = user.username;
        req.session.is_admin = user.is_admin;
        res.redirect('/notes');
    });
});

// Notes route
app.get('/notes', (req, res) => {
    if (!req.session.user_id) {
        return res.redirect('/login');
    }

    db.get('SELECT favorite_color FROM users WHERE id = ?', [req.session.user_id], (err, user) => {
        const favorite_color = user ? user.favorite_color : 'Unknown';
        let note = req.query.note || '';
        note = note.toString().replace(/"/g, '');
        const nonce = crypto.randomBytes(16).toString('base64');

        res.render('notes', { note, username: req.session.username, nonce, favorite_color });
    });
});


// Admin route
app.get('/flag', (req, res) => {
    if (!req.session.user_id || !req.session.is_admin) {
        return res.redirect('/login');
    }
    const flag = process.env.FLAG || 'Securinets{TEST}';
    res.send(flag);

});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

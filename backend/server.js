const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const cors = require('cors');

const app = express();

// Middleware
app.use(express.json());
app.use(cors({
    origin: 'http://localhost:3000',
    credentials: true
}));

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/socialMediaDB')
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log('MongoDB connection error:', err));

// User Schema
const userSchema = new mongoose.Schema({
    fullname: String,
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});

const User = mongoose.model('User', userSchema);

// Register Route (Overwrite Existing User)
app.post('/api/register', async (req, res) => {
    try {
        const { fullname, email, password } = req.body;

        const hashedPassword = await bcrypt.hash(password, 10);

        const user = await User.findOneAndUpdate(
            { email },
            { fullname, password: hashedPassword },
            { upsert: true, new: true }
        );

        res.status(201).json({ 
            message: 'User registered/updated successfully', 
            user: { id: user._id, fullname: user.fullname, email: user.email }
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

// Login Route
app.post('/api/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ message: 'Invalid credentials' });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ message: 'Invalid credentials' });
        }

        res.json({ 
            message: 'Login successful',
            user: { 
                id: user._id,
                fullname: user.fullname,
                email: user.email 
            }
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

app.get('/', (req, res) => {
    res.send('Social Media App Backend Running');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
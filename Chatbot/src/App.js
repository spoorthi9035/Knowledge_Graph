import React, { useState } from 'react';
import './App.css';
import {
  Container,
  Paper,
  TextField,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Typography,
  CssBaseline,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (input.trim() === '') return;
  
    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
  
    try {
      const response = await fetch('http://127.0.0.1:5000/natural_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
  
      // Assuming the backend response is an array of names
      const botReply = data.reply.map(item => item.name).join(', ');
  
      setMessages([...newMessages, { sender: 'bot', text: botReply }]);
      setInput('');
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([...newMessages, { sender: 'bot', text: 'Error: Could not get response from server' }]);
    }
  };
  

  return (
    <Container className="container" component="main" maxWidth="xs">
      <CssBaseline />
      <Paper className="chatPaper">
        <Typography variant="h4" className="typography">
          ChatBot
        </Typography>
        <div className="messagesContainer">
          <List>
            {messages.map((msg, index) => (
              <ListItem key={index}>
                <ListItemAvatar>
                  <Avatar className={msg.sender === 'user' ? 'userAvatar' : 'botAvatar'}>
                    {msg.sender === 'user' ? 'U' : 'B'}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText primary={msg.text} />
              </ListItem>
            ))}
          </List>
        </div>
        <div className="inputContainer">
          <TextField
            className="textField"
            variant="outlined"
            placeholder="Type a message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <IconButton color="primary" onClick={handleSend}>
            <SendIcon />
          </IconButton>
        </div>
      </Paper>
    </Container>
  );
}

export default App;

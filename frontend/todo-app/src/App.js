import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container,
  List,
  ListItem,
  ListItemText,
  Checkbox,
  Typography,
  Paper,
  IconButton,
  Divider,
  InputAdornment,
  OutlinedInput
} from '@mui/material';
import { Add, Delete } from '@mui/icons-material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [error, setError] = useState(null);

  const theme = createTheme({
    palette: {
      primary: { main: '#6200ea' },
      secondary: { main: '#03dac6' },
    },
  });

  const sortedTodos = [...todos].sort((a, b) => {
    if (a.is_done === b.is_done) return 0;
    return a.is_done ? 1 : -1;
  });

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await axios.get('http://localhost:8000/todos/');
      setTodos(response.data);
    } catch (err) {
      setError('Failed to fetch todos');
      console.error(err);
    }
  };

  const handleAddTodo = async () => {
    if (!newTodo.trim()) return;
    try {
      const response = await axios.post('http://localhost:8000/todos/', {
        task: newTodo,
        is_done: false
      });
      setTodos([...todos, response.data]);
      setNewTodo('');
    } catch (err) {
      setError('Failed to add todo');
      console.error(err);
    }
  };

  const handleToggleComplete = async (id, is_done) => {
    try {
      const currentTodo = todos.find(todo => todo.id === id);
      const response = await axios.put(`http://localhost:8000/todos/${id}`, {
        task: currentTodo.task,
        is_done: !is_done
      });
      setTodos(todos.map(todo => 
        todo.id === id ? response.data : todo
      ));
    } catch (err) {
      setError('Failed to update todo');
      console.error(err);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/todos/${id}/`);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err) {
      setError('Failed to delete todo');
      console.error(err);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="sm" sx={{ pt: 5 }}>
        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}
        <Typography variant="h4" align="center" sx={{ mb: 4 }}>
          TODO Application
        </Typography>
        <Paper elevation={3} sx={{ p: 2.5, mb: 4, bgcolor: 'grey.100' }}>
        <OutlinedInput
          placeholder="New TODO"
          fullWidth
          value={newTodo}
          onChange={e => setNewTodo(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleAddTodo()}
          sx={{ 
            '& .MuiOutlinedInput-root': { pr: 1 },
            bgcolor: 'background.paper'
          }}
          endAdornment={
            <InputAdornment position="end">
              <IconButton onClick={handleAddTodo}>
                <Add />
              </IconButton>
            </InputAdornment>
          }
        />
        </Paper>
        <Paper elevation={3} sx={{ p: 2.5, bgcolor: 'background.paper' }}>
          <List>
            {sortedTodos.length === 0 && (
              <Typography align="center" color="text.secondary">
                No TODOs available.
              </Typography>
            )}
            {sortedTodos.map(todo => (
              <React.Fragment key={todo.id}>
                <ListItem sx={{ py: 1.25 }}>
                  <Checkbox
                    edge="start"
                    checked={todo.is_done}
                    onChange={() => handleToggleComplete(todo.id, todo.is_done)}
                    color="secondary"
                  />
                  <ListItemText
                    primary={todo.task}
                    sx={{
                      ml: 2,
                      textDecoration: todo.is_done ? 'line-through' : 'none',
                      color: todo.is_done ? 'text.disabled' : 'text.primary'
                    }}
                  />
                  <IconButton 
                    edge="end" 
                    onClick={() => handleDeleteTodo(todo.id)} 
                    color="secondary"
                  >
                    <Delete />
                  </IconButton>
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </Paper>
      </Container>
    </ThemeProvider>
  );
}

export default App;
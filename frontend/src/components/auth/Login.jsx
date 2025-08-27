import React, { useState } from 'react';
import { Button, Input, notification } from 'antd';
import { login } from '../../services/auth_api';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      notification.warning({
        message: 'Input Required',
        description: 'Please enter both username and password.',
      });
      return;
    }

    setLoading(true);
    try {
      const response = await login(username, password);
      notification.success({
        message: 'Login Successful',
        description: `Welcome back, ${username}!`,
      });
      if (onLoginSuccess) {
        onLoginSuccess(response.user_id);
      }
    } catch (error) {
      notification.error({
        message: 'Login Failed',
        description: error.message || 'An unknown error occurred.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ width: 300, margin: 'auto', padding: 20, border: '1px solid #d9d9d9', borderRadius: 8 }}>
      <h2 style={{ textAlign: 'center', marginBottom: 20 }}>Login</h2>
      <Input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{ marginBottom: 10 }}
      />
      <Input.Password
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        onPressEnter={handleLogin}
        style={{ marginBottom: 20 }}
      />
      <Button type="primary" onClick={handleLogin} loading={loading} block>
        Login
      </Button>
    </div>
  );
};

export default Login;

/**
 * LoginButton - Firebase authentication login button
 */

import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

export const LoginButton: React.FC = () => {
  const { user, signIn, signOut, loading } = useAuth();

  if (loading) {
    return <button className="login-button" disabled>Loading...</button>;
  }

  if (user) {
    return (
      <button className="login-button" onClick={signOut}>
        Sign Out
      </button>
    );
  }

  return (
    <button className="login-button" onClick={signIn}>
      Sign In with Google
    </button>
  );
};

export default LoginButton;

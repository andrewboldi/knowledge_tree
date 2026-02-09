/**
 * UserProfile - Display authenticated user information
 */

import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

export const UserProfile: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="user-profile">
      {user.photoURL && (
        <img
          src={user.photoURL}
          alt={user.displayName || 'User'}
          className="user-avatar"
        />
      )}
      <span className="user-name">{user.displayName || user.email}</span>
    </div>
  );
};

export default UserProfile;

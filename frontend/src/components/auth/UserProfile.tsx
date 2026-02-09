import { useAuth } from '../../contexts/AuthContext';

export function UserProfile() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading user...</div>;
  }

  if (!user) {
    return <div>Not signed in</div>;
  }

  return (
    <div className="user-profile">
      {user.photoURL && (
        <img
          src={user.photoURL}
          alt={user.displayName || 'User avatar'}
          className="user-avatar"
        />
      )}
      <div className="user-info">
        <span className="user-name">{user.displayName}</span>
        <span className="user-email">{user.email}</span>
      </div>
    </div>
  );
}

import { useAuth } from '../../hooks/useAuth';

export function LoginButton() {
  const { user, loading, signInWithGoogle, logout } = useAuth();

  if (loading) {
    return <button disabled>Loading...</button>;
  }

  if (user) {
    return (
      <button onClick={logout}>
        Sign Out
      </button>
    );
  }

  return (
    <button onClick={signInWithGoogle}>
      Sign in with Google
    </button>
  );
}

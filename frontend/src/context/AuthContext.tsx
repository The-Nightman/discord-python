import {
  ReactNode,
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { jwtDecode } from "jwt-decode";

interface User {
  userID: string | null;
}

interface AuthProviderProps {
  children: ReactNode;
}

interface AuthContextInterface {
  user: User;
  login: (jwt: string) => void;
  logout: () => void;
  loading: boolean;
}

/**
 * Context to provide authentication-related data and operations.
 *
 * This context is used to manage and access the authentication state
 * and related functionalities throughout the application.
 *
 * @type {AuthContextInterface | undefined}
 */
const AuthContext = createContext<AuthContextInterface | undefined>(undefined);

/**
 * AuthProvider component that provides authentication context to its children.
 *
 * @param {AuthProviderProps} props - The props for the AuthProvider component.
 * @param {React.ReactNode} props.children - The child components that will have access to the authentication context.
 *
 * @returns {JSX.Element} The AuthProvider component with authentication context.
 *
 * @remarks
 * This code is repurposed from my `IBDirect` project at:
 * https://github.com/The-Nightman/IBDirect/blob/main/src/context/AuthContext.tsx
 *
 * This component uses the `useState` and `useEffect` hooks to manage the authentication state.
 * It checks for a JWT token in local storage and decodes it to set the user state.
 * It also provides `login` and `logout` functions to manage the authentication state.
 *
 * @example
 * ```tsx
 * import { AuthProvider } from './context/AuthContext';
 *
 * function App() {
 *   return (
 *     <AuthProvider>
 *       <YourComponent />
 *     </AuthProvider>
 *   );
 * }
 * ```
 */
export const AuthProvider = ({ children }: AuthProviderProps): JSX.Element => {
  const [user, setUser] = useState<User>({ userID: null });
  const [loading, setLoading] = useState(true);

  // Check for JWT token in local storage and set user state on mount
  useEffect(() => {
    const jwt = localStorage.getItem("jwt");
    // Use a timeout to prevent flashing back to the login screen when refreshing due to failing protected routes checks
    setTimeout(() => {
      if (jwt) {
        const decodedToken: { exp: number; sub: string } = jwtDecode(jwt);
        // Check if the token is expired
        if (decodedToken.exp * 1000 > Date.now()) {
          setUser({ userID: decodedToken.sub });
        } else {
          localStorage.removeItem("jwt");
        }
      }
      setLoading(false);
    }, 1000);
  }, []);

  /**
   * Logs in the user by storing the JWT in local storage and decoding it to set the user state.
   *
   * @param {string} jwt - The JSON Web Token received upon successful authentication.
   * @returns {void}
   */
  const login = (jwt: string): void => {
    localStorage.setItem("jwt", jwt);
    const decodedToken: { exp: number; sub: string } = jwtDecode(jwt);
    setUser({ userID: decodedToken.sub });
  };

  /**
   * Logs out the current user by removing the JWT from local storage
   * and resetting the user state.
   * 
   * @returns {void}
   */
  const logout = (): void => {
    localStorage.removeItem("jwt");
    setUser({ userID: null });
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to access the authentication context.
 *
 * @returns {AuthContextInterface} The current authentication context value.
 */
export const useAuth = () => {
  return useContext(AuthContext) as AuthContextInterface;
};

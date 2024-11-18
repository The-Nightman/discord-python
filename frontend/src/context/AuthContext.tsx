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
  validateAuth: () => Promise<boolean>;
  logout: () => void;
}

/**
 * Context to provide authentication-related data and operations.
 *
 * This context is used to manage and access the authentication state
 * and related functionalities throughout the application.
 *
 * @type {Context<AuthContextInterface | undefined>}
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
 * This code is repurposed and refactored from my `IBDirect` project at:
 * https://github.com/The-Nightman/IBDirect/blob/main/src/context/AuthContext.tsx
 *
 * This component uses the `useState` and `useEffect` hooks to manage the authentication state.
 * It checks for a JWT token in local storage and decodes it to set the user state.
 * It also provides `login`, `validateAuth` and `logout` functions to manage the authentication state.
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

  // Re-use the validateAuth function to check if a JWT is stored in local storage
  // on component mount and store the userID in the user state if the JWT is valid.
  useEffect(() => {
    const checkAuth = async () => {
      await validateAuth();
    };

    checkAuth();
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
   * Validates the authentication status of the user by checking the JWT token stored in local storage.
   *
   * - If a valid JWT token is found and it is not expired, the user is considered authenticated.
   * - If the JWT token is expired or not found, the user is considered unauthenticated and the token is removed from local storage.
   *
   * @remarks This alone does not protect against invalid modified JWT tokens but this should be taken care of with propper backend auth.
   *
   * @returns {Promise<boolean>} A promise that resolves to a boolean indicating whether the user is authenticated.
   */
  const validateAuth = async (): Promise<boolean> => {
    const jwt = localStorage.getItem("jwt");
    if (jwt) {
      const decodedToken: { exp: number; sub: string } = jwtDecode(jwt);
      if (decodedToken.exp * 1000 > Date.now()) {
        setUser({ userID: decodedToken.sub });
        return true; // User is authenticated
      }
      // Remove the JWT if it is expired
      localStorage.removeItem("jwt");
      setUser({ userID: null });
      return false;
    }
    return false;
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
    <AuthContext.Provider value={{ user, login, validateAuth, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to access the authentication context.
 *
 * @returns {AuthContextInterface} The current authentication context value.
 */
export const useAuth = (): AuthContextInterface => {
  return useContext(AuthContext) as AuthContextInterface;
};

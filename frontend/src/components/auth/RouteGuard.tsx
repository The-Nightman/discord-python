import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { Spinner } from "../UX/Spinner";
import { useEffect, useState } from "react";

/**
 * RouteGuard component is responsible for protecting routes based on user authentication status.
 * It uses the `validateAuth` function from the `useAuth` hook to validate the user's authentication state.
 *
 * @component
 *
 * @remarks
 * - The component maintains an internal state `authState` to track loading and authentication status.
 * - The `useEffect` hook is used to trigger the authentication check when the component mounts.
 * - If the user is authenticated, it renders the `Outlet` component to display nested routes.
 * - If the user is not authenticated, it redirects to the home page using the `Navigate` component.
 *
 * @returns {JSX.Element} Returns a loading spinner while checking authentication,
 * and either renders the child components if authenticated or redirects to the home page if not.
 *
 * @example
 * ```tsx
 * <Routes>
 *   <Route path="/" element={<UnauthenticatedLayout />} >
 *   <RouteGuard>
 *     <Route path="/app" element={<AuthenticatedLayout />} />
 *   </RouteGuard>
 * </Routes>
 * ```
 */
const RouteGuard = (): JSX.Element => {
  const [authState, setAuthState] = useState({
    loading: true,
    authenticated: false,
  });
  const { validateAuth } = useAuth();

  // Check if the user is authenticated
  useEffect(() => {
    const checkAuth = async () => {
      if (await validateAuth()) {
        setAuthState({ loading: false, authenticated: true });
      } else {
        setAuthState({ loading: false, authenticated: false });
      }
    };

    checkAuth();
  }, []);

  if (authState.loading) {
    return (
      <div className="h-screen w-screen flex justify-center items-center">
        <p className="animate-pulse absolute top-[45%] z-[100] text-2xl text-white">
          Checking User Authentication
        </p>
        <Spinner />
      </div>
    );
  }
  return <>{authState.authenticated ? <Outlet /> : <Navigate to={"/"} />}</>;
};
export default RouteGuard;

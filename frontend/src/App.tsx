import { Route, Routes } from "react-router-dom";
import { UnauthenticatedLayout } from "./layouts/UnauthenticatedLayout";
import { Login } from "./routes/unauthenticated/Login";
import { Register } from "./routes/unauthenticated/Register";
import RouteGuard from "./components/auth/RouteGuard";
import { AuthenticatedLayout } from "./layouts/AuthenticatedLayout";
import { ServerLayout } from "./layouts/ServerLayout";

function App() {
  return (
    <Routes>
      <Route path="/" Component={UnauthenticatedLayout}>
        <Route path="/" Component={Login} />
        <Route path="/register" Component={Register} />
      </Route>
      <Route path="/" Component={RouteGuard}>
        <Route path="/app" Component={AuthenticatedLayout}>
          <Route path="/app" Component={ServerLayout} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;

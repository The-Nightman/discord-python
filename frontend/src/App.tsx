import { Route, Routes } from "react-router-dom";
import { UnauthenticatedLayout } from "./layouts/UnauthenticatedLayout";
import { Login } from "./routes/unauthenticated/Login";
import { Register } from "./routes/unauthenticated/Register";

function App() {
  return (
    <Routes>
      <Route path="/" Component={UnauthenticatedLayout}>
        <Route path="/" Component={Login} />
        <Route path="/register" Component={Register} />
      </Route>
    </Routes>
  );
}

export default App;

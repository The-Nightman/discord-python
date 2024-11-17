import { Route, Routes } from "react-router-dom";
import { UnauthenticatedLayout } from "./layouts/UnauthenticatedLayout";
import { Login } from "./routes/unauthenticated/Login";

function App() {
  return (
    <Routes>
      <Route path="/" Component={UnauthenticatedLayout}>
        <Route path="/" Component={Login} />
      </Route>
    </Routes>
  );
}

export default App;

import { Route, Routes } from "react-router-dom";
import { UnauthenticatedLayout } from "./layouts/UnauthenticatedLayout";

function App() {
  return (
    <Routes>
      <Route path="/" Component={UnauthenticatedLayout}>
      </Route>
    </Routes>
  );
}

export default App;

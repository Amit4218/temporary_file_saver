import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Home } from "./pages/Home";
import { Error } from "./pages/Error";
import { NavBarComponent } from "./components/Navbar";
import { Footer } from "./components/Footer";

export function App() {
  return (
    <>
      <BrowserRouter>
        <NavBarComponent />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="*" element={<Error />} />
        </Routes>

        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;

import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "sonner";
import HomePage from "./pages/HomePage";
import ProposalPage from "./pages/ProposalPage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/proposal/:proposalId" element={<ProposalPage />} />
        </Routes>
      </BrowserRouter>
      <Toaster 
        position="top-center"
        toastOptions={{
          style: {
            background: '#FFF0F5',
            border: '1px solid #FF8FA3',
            color: '#4A4A4A',
          },
        }}
      />
    </div>
  );
}

export default App;

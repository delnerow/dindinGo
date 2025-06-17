import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Transacoes from './pages/Transacoes';
import Contas from './pages/Contas';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/transacoes" element={<Transacoes />} />
        <Route path="/contas" element={<Contas />} />
      </Routes>
    </BrowserRouter>
  );
}
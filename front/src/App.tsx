import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Transacoes from './pages/Transacoes';
import Carteiras from './pages/Carteiras';
import Cofrinhos from './pages/Cofrinhos';
import Pontos from './pages/Pontos';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/transacoes" element={<Transacoes />} />
        <Route path="/carteiras" element={<Carteiras />} />
        <Route path="/cofrinhos" element={<Cofrinhos />} />
        <Route path="/pontos" element={<Pontos />} />
      </Routes>
    </BrowserRouter>
  );
}
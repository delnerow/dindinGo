import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Transacoes from './pages/Transacoes';
import Carteiras from './pages/Carteiras';
import Cofrinhos from './pages/Cofrinhos';
import Pontos from './pages/Pontos';
import React, { createContext, useContext, useEffect, useState } from 'react';
import { Settings } from 'lucide-react';
import { SettingsModal } from './pages/Transacoes';

// Theme context and provider
const themes = ['light', 'dark', 'green', 'blue', 'neon'] as const;
type Theme = typeof themes[number];

const ThemeContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
}>({ theme: 'light', setTheme: () => {} });

export function useTheme() {
  return useContext(ThemeContext);
}

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(() => {
    const stored = localStorage.getItem('theme');
    return (stored && themes.includes(stored as Theme)) ? (stored as Theme) : 'light';
  });

  useEffect(() => {
    document.body.classList.remove(...themes.map(t => `theme-${t}`));
    document.body.classList.add(`theme-${theme}`);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const setTheme = (t: Theme) => setThemeState(t);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export default function App() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard settingsOnClick={() => setIsSettingsOpen(true)} />} />
          <Route path="/transacoes" element={<Transacoes settingsOnClick={() => setIsSettingsOpen(true)} />} />
          <Route path="/carteiras" element={<Carteiras settingsOnClick={() => setIsSettingsOpen(true)} />} />
          <Route path="/cofrinhos" element={<Cofrinhos settingsOnClick={() => setIsSettingsOpen(true)} />} />
          <Route path="/pontos" element={<Pontos settingsOnClick={() => setIsSettingsOpen(true)} />} />
        </Routes>
        {isSettingsOpen && (
          <SettingsModal onClose={() => setIsSettingsOpen(false)} />
        )}
      </BrowserRouter>
    </ThemeProvider>
  );
}
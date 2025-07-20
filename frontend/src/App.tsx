import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import GuestOnlyRoute from "@components/GuestOnlyRoute";
import ProtectedRoute from "@components/ProtectedRoute";
import { AuthProvider } from "@context/AuthContext";

// === Error Pages ===
import PageNotFound from "@pages/PageNotFound";

// === Auth Pages ===
import AuthPage from "@pages/AuthPage";

// === Main Pages ===
import HomePage from "@pages/HomePage";

import AccountProfilePage from "@pages/account/AccountProfilePage";
import AccountSecurityPage from "@pages/account/AccountSecurityPage";

import WorldsPage from "@pages/library/WorldsPage";

import WorldDetailPage from "@pages/library/detail/WorldDetailPage";

export default function App() {
  return (
    <div className="w-100 h-100">
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/auth" element={<GuestOnlyRoute><AuthPage /></GuestOnlyRoute>} />

            <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />

            <Route path="/account/profile" element={<ProtectedRoute><AccountProfilePage /></ProtectedRoute>} />
            <Route path="/account/settings" element={<ProtectedRoute><AccountSecurityPage /></ProtectedRoute>} />
            <Route path="/account/*" element={<Navigate to="/account/profile" />} />

            <Route path="/library/worlds" element={<ProtectedRoute><WorldsPage /></ProtectedRoute>} />
            <Route path="/library/campaigns*" element={<Navigate to="/library/worlds" />} />
            <Route path="/library/actors*" element={<Navigate to="/library/worlds" />} />
            <Route path="/library/items*" element={<Navigate to="/library/worlds" />} />
            <Route path="/library/*" element={<Navigate to="/library/worlds" />} />

            <Route path="/details/world/:id" element={<WorldDetailPage />} />
            <Route path="/details/*" element={<Navigate to="/library" />} />

            <Route path="*" element={<PageNotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import GuestOnlyRoute from "@components/GuestOnlyRoute";
import ProtectedRoute from "@components/ProtectedRoute";
import { AuthProvider } from "@context/AuthContext";

import PageNotFound from "@pages/PageNotFound";

import AuthPage from "@pages/AuthPage";
import HomePage from "@pages/HomePage";
import AccountProfilePage from "@/pages/account/AccountProfilePage";
import AccountSecurityPage from "@/pages/account/AccountSecurityPage";

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

            <Route path="*" element={<PageNotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

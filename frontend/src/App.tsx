import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import GuestOnlyRoute from "@components/GuestOnlyRoute";
import ProtectedRoute from "@components/ProtectedRoute";
import { AuthProvider } from "@context/AuthContext";

// === Error Pages ===
import PageNotFound from "@/pages/error/PageNotFound";
import RequestDenied from "@/pages/error/RequestDenied";

// === Auth Pages ===
import AuthPage from "@pages/AuthPage";

// === Main Pages ===
import HomePage from "@pages/HomePage";

import AccountProfilePage from "@pages/account/AccountProfilePage";
import AccountSecurityPage from "@pages/account/AccountSecurityPage";

import LibraryPage from "@pages/library/LibraryPage";

import WorldWizardPage from "@pages/library/wizard/WorldWizardPage";

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

            <Route path="/library" element={<ProtectedRoute><LibraryPage /></ProtectedRoute>} />
            <Route path="/library/worlds" element={<Navigate to="/library?tab=0" replace />} />
            <Route path="/library/campaigns" element={<Navigate to="/library?tab=1" replace />} />
            <Route path="/library/blueprints" element={<Navigate to="/library?tab=2" replace />} />
            <Route path="/library/*" element={<Navigate to="/library/worlds" />} />

            <Route path="/details/world/:id" element={<ProtectedRoute><WorldWizardPage /></ProtectedRoute>} />
            <Route path="/details/campaign/:id" element={<Navigate to="/library/worlds" />} />
            <Route path="/details/*" element={<Navigate to="/library" />} />

            <Route path="/session/:id/:role" element={<ProtectedRoute><WorldWizardPage /></ProtectedRoute>} />

            <Route path="/403" element={<RequestDenied />} />
            <Route path="/404" element={<PageNotFound />} />
            <Route path="*" element={<Navigate to="/404" />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

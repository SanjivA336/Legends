import { createContext, useContext, useEffect, useState } from "react";
import { authenticate } from "@apis/auth_api";
import type { UserResponse } from "@apis/_schemas";

type AuthContextType = {
    user: UserResponse | null;
    loading: boolean;
};

const AuthContext = createContext<AuthContextType>({
    user: null,
    loading: true,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<UserResponse | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function checkAuth() {
            try {
                const data = await authenticate();
                setUser(data);
            } catch (err) {
                console.error("Authentication failed:", err);
                setUser(null);
            } finally {
                setLoading(false);
            }
        }

        checkAuth();
    }, []);

    return (
        <AuthContext.Provider value={{ user, loading }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}

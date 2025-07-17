import React, { useState } from "react";
import AuthLayout from "@layouts/AuthLayout";
import LoginForm from "@features/auth/LoginForm";
import RegisterForm from "@features/auth/RegisterForm";

export default function AuthPage() {
    const [isLogin, setIsLogin] = useState(true);

    // Optional shared error message between forms
    const [error, setError] = useState("");

    const toggleFormMode = () => {
        setError(""); // reset errors when switching
        setIsLogin((prev) => !prev);
    };

    return (
        <AuthLayout>
            {isLogin ? (
                <LoginForm
                toggleMode={toggleFormMode}
                error={error}
                setError={setError}
                />
            ) : (
                <RegisterForm
                toggleMode={toggleFormMode}
                error={error}
                setError={setError}
                />
            )}
        </AuthLayout>
    );
}

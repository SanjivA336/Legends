import { useState } from "react";
import AuthLayout from "@layouts/AuthLayout";
import LoginForm from "@features/auth/LoginForm";
import RegisterForm from "@features/auth/RegisterForm";

export default function AuthPage() {
    const [isLogin, setIsLogin] = useState(true);

    // Optional shared error message between forms

    const toggleFormMode = () => {
        setIsLogin((prev) => !prev);
    };

    return (
        <AuthLayout>
            {isLogin ? (
                <LoginForm toggleMode={toggleFormMode}/>
            ) : (
                <RegisterForm toggleMode={toggleFormMode}/>
            )}
        </AuthLayout>
    );
}

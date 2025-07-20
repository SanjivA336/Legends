import React, { useState } from "react";
import { login } from "@apis/auth_api";
import TextField from "@/components/modular/TextField";
import ToggleField from "@/components/modular/ToggleField";
import ErrorBox from "@/components/modular/ErrorBox";


type LoginFormProps = {
    toggleMode: () => void;
};

export default function LoginForm({ toggleMode }: LoginFormProps) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        if (loading) return;

        e.preventDefault();
        setLoading(true);
        setError("");

        if (!email || !password) {
            setError("Please enter email and password.");
            return;
        }

        try {
            await login(email, password);
            window.location.reload();
            setError("");
        } catch (err: any) {
            setError(err.message || "Login failed.");
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <form className="w-100 text-center d-flex flex-column gap-2 align-items-center" onSubmit={handleSubmit}>
            <h2>Login</h2>
            <TextField
                value={email}
                setValue={setEmail}
                placeholder="Email"
                autoComplete="email"
                type="email"
                label="Email"
                required={true} />
            <TextField
                value={password}
                setValue={setPassword}
                placeholder="Password"
                autoComplete="current-password"
                type={showPassword ? "text" : "password"}
                label="Password"
                required={true} />
            <ToggleField
                value={showPassword}
                setValue={setShowPassword}
                label="Show Password"
                type="checkbox"
                required={false}
                disabled={loading} />

            <ErrorBox error={error} />

            <button className="w-50 bg-primary rounded-pill px-3 py-2 border-0 text-light" type="submit" disabled={loading}>
                Login
                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
            </button>

            <p>
                Don't have an account?{" "}
                <button className="bg-transparent p-0  m-0 text-primary border-0" type="button" onClick={toggleMode}>
                    Register here
                </button>
            </p>
        </form>
    );
}
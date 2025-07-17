import React, { useState } from "react";
import { login } from "@apis/auth_api";


type LoginFormProps = {
    toggleMode: () => void;
    error: string;
    setError: (msg: string) => void;
};

export default function LoginForm({ toggleMode, error, setError }: LoginFormProps) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

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
            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2" >Email</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type="email"
                    placeholder="Email"
                    value={email}
                    autoComplete="email"
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2" >Password</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    value={password}
                    autoComplete="current-password"
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>
            <div className="form-check w-100 text-start">
                <input
                    className="form-check-input"
                    type="checkbox"
                    id="showPassword"
                    checked={showPassword}
                    onChange={() => setShowPassword((prev) => !prev)}
                />
                <label className="form-check-label" htmlFor="showPassword">
                    Show Password
                </label>
            </div>
            {error && <div className="w-100 text-danger border border-2 border-danger p-2 bg-darker rounded-3">{error}</div>}
            <button className="w-50 bg-primary rounded-pill px-3 py-2 border-0 text-light" type="submit" disabled={loading}>
                Login
                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
            </button>
            <p>
                Don't have an account?{" "}
                <button className="bg-transparent p-0 text-primary border-0" type="button" onClick={toggleMode}>
                    Register here
                </button>
            </p>
        </form>
    );
}
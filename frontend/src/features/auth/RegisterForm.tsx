import React, { useState } from "react";
import { register } from "@apis/auth_api";

type RegisterFormProps = {
    toggleMode: () => void;
    error: string;
    setError: (msg: string) => void;
};

export default function RegisterForm({ toggleMode, error, setError }: RegisterFormProps) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (loading) return;

        setError("");
        setLoading(true);

        if (!username || !email || !password || !confirm) {
            setError("Please fill in all fields.");
            setLoading(false);
            return;
        }

        if (password !== confirm) {
            setError("Passwords do not match.");
            setLoading(false);
            return;
        }

        try {
            await register(username, email, password);
            window.location.reload();
            setError("");
        } catch (err: any) {
            setError(err.message || "Registration failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form className="w-100 text-center d-flex flex-column gap-2 align-items-center" onSubmit={handleSubmit}>
            <h2>Register</h2>

            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2">Username</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type="text"
                    placeholder="Username"
                    value={username}
                    autoComplete="username"
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
            </div>

            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2">Email</label>
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
                <label className="w-100 text-start ps-2 pb-2">Password</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    value={password}
                    autoComplete="new-password"
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>

            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2">Confirm Password</label>
                <input
                    className={`w-100 bg-darker text-light rounded-pill px-3 py-2 ${
                        confirm && confirm !== password ? "border border-2 border-danger" : "border-0"
                    }`}
                    type={showPassword ? "text" : "password"}
                    placeholder="Confirm Password"
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
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

            {error && (
                <div className="w-100 text-danger border border-2 border-danger p-2 bg-darker rounded-3">
                    {error}
                </div>
            )}

            <button
                className="w-50 bg-primary rounded-pill px-3 py-2 border-0 text-light"
                type="submit"
                disabled={loading}
            >
                Register
                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}

            </button>

            <p>
                Already have an account?{" "}
                <button
                    className="bg-transparent p-0 text-primary border-0"
                    type="button"
                    onClick={toggleMode}
                >
                    Login here
                </button>
            </p>
        </form>
    );
}

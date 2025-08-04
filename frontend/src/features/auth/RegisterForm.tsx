import React, { useState } from "react";
import { register } from "@apis/auth_api";
import ShortTextField from "@/components/fields/ShortTextField";
import ToggleField from "@/components/fields/ToggleField";
import MessageBox from "@/components/MessageBox";

type RegisterFormProps = {
    toggleMode: () => void;
};

export default function RegisterForm({ toggleMode }: RegisterFormProps) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

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
            <ShortTextField
                value={username}
                setValue={setUsername}
                placeholder="Username"
                autoComplete="username"
                type="text"
                label="Username"
                required={true} />
            <ShortTextField
                value={email}
                setValue={setEmail}
                placeholder="Email"
                autoComplete="email"
                type="email"
                label="Email"
                required={true} />
            <ShortTextField
                value={password}
                setValue={setPassword}
                placeholder="Password"
                autoComplete="current-password"
                type={showPassword ? "text" : "password"}
                label="Password"
                required={true} />
            <ShortTextField
                value={confirm}
                setValue={setConfirm}
                placeholder="Confirm Password"
                autoComplete="new-password"
                type={showPassword ? "text" : "password"}
                label="Confirm Password"
                required={true} />
            <ToggleField
                value={showPassword}
                setValue={setShowPassword}
                label="Show Password"
                type="checkbox"
                required={false}
                disabled={loading} />

            <MessageBox error={error} />

            <button className="w-50 bg-primary rounded-pill px-3 py-2 border-0 text-light" type="submit" disabled={loading}>
                Register
                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
            </button>
            <p>
                Already have an account?{" "}
                <button className="bg-transparent p-0  m-0 text-primary border-0" type="button" onClick={toggleMode}>
                    Login here
                </button>
            </p>

        </form>
    );
}

import React, { useEffect, useState } from "react";
import { account_get, security_update } from "@apis/account_api"
import TextField from "@/components/modular/TextField";
import ToggleField from "@/components/modular/ToggleField";
import ErrorBox from "@/components/modular/ErrorBox";

export default function SecurityForm() {
    const [email, setEmail] = useState("");
    const [newEmail, setNewEmail] = useState("");
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchProfile = async () => {
        setLoading(true);
        setError("");
        try {
            const data = await account_get();
            setEmail(data.email || "");
            setNewEmail(data.email || "");
        } catch (err: any) {
            setError(err.message || "Failed to load profile.");
        }
        setLoading(false);
    };

    useEffect(() => {
        if (loading) return;

        fetchProfile();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (loading) return;

        setError("");
        setLoading(true);

        try {
            await security_update(newEmail, currentPassword, newPassword);
            setEmail(newEmail);
            setCurrentPassword("");
            setNewPassword("");
            setError("");
        } catch (err: any) {
            setError(err.message || "Registration failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form className="w-100 text-center d-flex flex-column gap-2 align-items-start" onSubmit={handleSubmit}>
            <h4>Communication</h4>
            <TextField
                label="Email"
                value={newEmail}
                setValue={setNewEmail}
                placeholder={email}
                autoComplete="email"
                type="email" />

            <h4 className="mt-3">Change Password</h4>
            <TextField
                label="Current Password"
                value={currentPassword}
                setValue={setCurrentPassword}
                placeholder="Enter your current password"
                autoComplete="current-password"
                type={showPassword ? "text" : "password"}
                required={false} />
            <TextField
                label="New Password"
                value={newPassword}
                setValue={setNewPassword}
                placeholder="Enter your new password"
                autoComplete="new-password"
                type={showPassword ? "text" : "password"}
                required={false} />
            <ToggleField
                value={showPassword}
                setValue={setShowPassword}
                label="Show Password"
                type="checkbox"
                required={false}
                disabled={loading} />

            <ErrorBox error={error} />

            <div className="w-100 d-flex flex-row gap-2">
                <button className="w-50 btn btn-outline-primary rounded-3 px-3 py-2" type="submit" disabled={loading}>
                    Save Changes
                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                </button>
                <button className="w-50 btn btn-outline-danger rounded-3 px-3 py-2" disabled={loading} onClick={() => {setNewEmail(email); setCurrentPassword(""); setNewPassword(""); setError("");}}>
                    Cancel Changes
                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                </button>
            </div>
        </form>
    );
}
    
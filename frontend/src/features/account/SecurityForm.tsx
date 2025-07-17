import React, { useEffect, useState } from "react";
import { account_get, security_update } from "@apis/account_api"

export default function SecurityForm() {
    const [email, setEmail] = useState("");
    const [newEmail, setNewEmail] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    useEffect(() => {
        if (loading) return;

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

        fetchProfile();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (loading) return;

        setError("");
        setLoading(true);

        if (!newEmail || !oldPassword) {
            setError("Please fill in all fields.");
            setLoading(false);
            return;
        }

        try {
            await security_update(newEmail, oldPassword, newPassword);
            setEmail(newEmail);
            setOldPassword("");
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
            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2">Email</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type="text"
                    placeholder={email}
                    value={newEmail}
                    autoComplete="email"
                    onChange={(e) => setNewEmail(e.target.value)}
                    required
                />
            </div>
            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2">Old Password</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type={showPassword ? "text" : "password"}
                    placeholder="Old Password"
                    value={oldPassword}
                    autoComplete="current-password"
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                />
            </div>
            <div className="w-100 text-light mb-2">
                <label className="w-100 text-start ps-2 pb-2">New Password</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type={showPassword ? "text" : "password"}
                    placeholder="New Password"
                    value={newPassword}
                    autoComplete="new-password"
                    onChange={(e) => setNewPassword(e.target.value)}
                />
            </div>
            <div className="form-check w-100 text-start">
                <input
                    className="form-check-input"
                    type="checkbox"
                    checked={showPassword}
                    onChange={() => setShowPassword(!showPassword)}
                />
                <label className="form-check-label">Show Password</label>
            </div>

            {error && (
                <div className="w-100 text-danger border border-2 border-danger p-2 bg-darker rounded-3">
                    {error}
                </div>
            )}

            <div className="w-100 d-flex flex-row gap-2">
                <button className="w-50 btn btn-outline-primary rounded-3 px-3 py-2" type="submit" disabled={loading}>
                    Save Changes
                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                </button>
                <button className="w-50 btn btn-outline-danger rounded-3 px-3 py-2" disabled={loading} onClick={() => {setNewEmail(email); setOldPassword(""); setNewPassword(""); setError("");}}>
                    Cancel Changes
                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                </button>
            </div>
        </form>
    );
}
    
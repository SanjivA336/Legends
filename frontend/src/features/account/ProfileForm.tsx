import React, { useEffect, useState } from "react";
import { account_get, profile_update } from "@apis/account_api"

export default function ProfileForm() {
    const [username, setUsername] = useState("");
    const [newUsername, setNewUsername] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    useEffect(() => {
        if (loading) return;

        const fetchProfile = async () => {
            setLoading(true);
            setError("");
            try {
                const data = await account_get();
                setUsername(data.username || "");
                setNewUsername(data.username || "");
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

        if (!newUsername) {
            setError("Please fill in all fields.");
            setLoading(false);
            return;
        }

        try {
            await profile_update(newUsername);
            setUsername(newUsername);
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
                <label className="w-100 text-start ps-2 pb-2">Username</label>
                <input
                    className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                    type="text"
                    placeholder={username}
                    value={newUsername}
                    autoComplete="username"
                    onChange={(e) => setNewUsername(e.target.value)}
                />
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
                <button className="w-50 btn btn-outline-danger rounded-3 px-3 py-2" disabled={loading} onClick={() => {setNewUsername(username); setError("");}}>
                    Cancel Changes
                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                </button>
            </div>
        </form>
    );
}
    
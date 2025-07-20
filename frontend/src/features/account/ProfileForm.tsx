import React, { useEffect, useState } from "react";
import { account_get, profile_update } from "@apis/account_api"
import TextField from "@/components/modular/TextField";
import ErrorBox from "@/components/modular/ErrorBox";

export default function ProfileForm() {
    const [username, setUsername] = useState("");
    const [newUsername, setNewUsername] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

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

    useEffect(() => {
        fetchProfile();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        if (loading) return;

        e.preventDefault();
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
            <h4>Display</h4>
            <TextField
                label="Username"
                value={newUsername}
                setValue={setNewUsername}
                placeholder={username}
                autoComplete="username"
                type="text" />

            <ErrorBox error={error} />

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
    
import { useNavigate } from "react-router-dom";
import { logout } from "@apis/auth_api";
import React from "react";

import Logo from "@/assets/brand/LogoAccent.png";

export const NAVBAR_HEIGHT = "70px";

const Navbar = () => {
    const navigate = useNavigate();

    const [loading, setLoading] = React.useState(false);

    const handleLogout = async () => {
        if (loading) return;

        setLoading(true);

        try {
            await logout();
            window.location.reload();
        } catch (err: any) {
            console.error(err);
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-100 px-4 bg-dark d-flex flex-row justify-content-between fixed-top" style={{ height: NAVBAR_HEIGHT }}>
            {/* Navbar Start */}
            <div className="d-flex align-items-start h-100">
                <img src={Logo} className="h-50 my-auto me-2" onClick={() => navigate("/")}/>
                <h1 className="text-light my-auto" onClick={() => navigate("/")}>Legends</h1>
            </div>

            {/* Navbar End */}
            <div className="d-flex gap-2 align-items-end">
                <button className="btn btn-dark px-3 my-auto" onClick={() => navigate("/")} disabled={loading}>
                    Home
                </button>
                <button className="btn btn-dark px-3 my-auto" onClick={() => navigate("/account")} disabled={loading}>
                    Account
                </button>
                <button className="btn btn-outline-danger px-3 my-auto" onClick={() => handleLogout()} disabled={loading}>
                    Logout
                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                </button>
            </div>
        </div>
    );
};

export default Navbar;

import { useNavigate } from "react-router-dom";

const AccountSidebar = () => {
    const navigate = useNavigate();

    return (
        <div className="w-100 h-100 d-flex flex-column justify-content-between">
            {/* Sidebar Top */}
            <div className="w-100 d-flex flex-column gap-1 align-items-center my-2">
                <button className="w-75 btn btn-dark p-2 mb-2" onClick={() => navigate("/account/profile")}>
                    Profile
                </button>
                <button className="w-75 btn btn-dark p-2 mb-2" onClick={() => navigate("/account/settings")}>
                    Settings
                </button>
            </div>

            {/* Sidebar Bottom */}
            <div className="d-flex align-items-end">
                <div className="w-100 d-flex flex-column align-items-end my-2">
                    
                </div>
            </div>
        </div>
    );
};

export default AccountSidebar;

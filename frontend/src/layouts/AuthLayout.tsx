import React from "react";

type AuthLayoutProps = {
    children: React.ReactNode;
};

export default function AuthLayout({ children }: AuthLayoutProps) {
    return (
        <div className="vw-100 vh-100 d-flex flex-column align-items-center justify-content-center bg-darkest text-light">
            <div className="d-flex mb-3">
                <h1 className="text-light">Welcome to&nbsp;</h1>
                <h1 className="text-primary">Legends.</h1>
            </div>
            <div className="d-flex flex-column align-items-center justify-content-center rounded-5 bg-dark px-5 py-4 shadow">
                {children}
            </div>
        </div>
    );
}

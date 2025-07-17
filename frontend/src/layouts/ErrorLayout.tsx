import React from "react";

type ErrorLayoutProps = {
    children: React.ReactNode;
};

export default function ErrorLayout({ children }: ErrorLayoutProps) {
    return (
        <div className="w-100 h-100 d-flex flex-column align-items-center justify-content-center bg-darkest text-light">
            {children}
        </div>
    );
}

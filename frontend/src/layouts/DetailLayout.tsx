import { useNavigate } from "react-router-dom";

type DetailLayoutProps = {
    children: React.ReactNode;
};

export default function DetailLayout({ children }: DetailLayoutProps) {
    const navigate = useNavigate();

    return (
        <div className="w-100 h-100 p-5 d-flex flex-column align-items-center justify-content-center bg-darkest text-light">
            <div className="w-100 h-100 bg-dark rounded-5 p-4 shadow">
                {children}

            </div>
        </div>
    );
}

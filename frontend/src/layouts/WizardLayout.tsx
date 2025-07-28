import { useNavigate } from "react-router-dom";

type DetailLayoutProps = {
    children: React.ReactNode;
    title: string;
    style: "tabs" | "stages" | "hidden";
    tabs: string[];
    currentTab: number;
    setCurrentTab: (tab: number) => void;
};

export default function DetailLayout({ children, title, style, tabs, currentTab, setCurrentTab }: DetailLayoutProps) {
    const navigate = useNavigate();

    return (
        <div className="w-100 h-100 p-4 d-flex flex-column align-items-center justify-content-center bg-darkest text-light">
            <h1 className="text-light mb-4">{title}</h1>
            {style === "tabs" && (
                <div className="w-100 px-5 gap-4 d-flex justify-content-between">
                    {tabs.map((tab, index) => (
                        <button
                            key={index}
                            className={`w-100 p-2 btn ${currentTab === index ? "btn-primary" : "btn-dark"}`}
                            onClick={() => setCurrentTab && setCurrentTab(index)}
                        >
                            {tab}
                        </button>
                    ))}
                </div>
            )}
            {style === "stages" && (
                <div className="w-100 px-5 gap-4 d-flex justify-content-between mb-3">
                    {tabs.map((tab, index) => (
                        <>
                            <button
                                key={index}
                                className={`w-100 p-2 btn ${currentTab === index ? "btn-primary" : currentTab > index ? "btn-outline-primary" : "btn-dark"}`}
                                onClick={() => setCurrentTab && setCurrentTab(index)}
                            >
                                {tab}
                            </button>
                            <h2 className={`m-0 p-0 ${currentTab > index ? "text-primary" : "text-light"}`}>{index < tabs.length - 1 ? ">" : ""}</h2>
                        </>
                    ))}
                </div>
            )}
            <div className="w-100 h-100 d-flex flex-column align-items-center justify-content-center p-3">
                {children}
            </div>
        </div>
    );
}

import { useNavigate } from "react-router-dom";

import TabGroup from "@components/TabGroup";

type DetailLayoutProps = {
    currentTab: number;
    setCurrentTab: (tab: number) => void;

    tabs: string[];
    title: string;

    children: React.ReactNode;
};

export default function DetailLayout({ currentTab, setCurrentTab, tabs, title, children }: DetailLayoutProps) {
    const navigate = useNavigate();

    return (
        <div className="w-100 p-4 d-flex flex-column align-items-center justify-content-center bg-darkest text-light">
            <h1 className="text-light mb-4">{title}</h1>
            <TabGroup
                tabNumber={currentTab}
                setTabNumber={setCurrentTab}
                tabNames={tabs}
                orientation="horizontal"
                rounding="3"
                disabled={false}
            />
            <div className="w-100 d-flex flex-column align-items-center justify-content-center p-3">
                {children}
            </div>
        </div>
    );
}

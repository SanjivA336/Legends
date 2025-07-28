import BaseLayout from "@/layouts/BaseLayout";
import {NAVBAR_HEIGHT} from "@components/Navbar";
import { useNavigate } from "react-router-dom";

type LibraryLayoutProps = {
    tab: number;
    children: React.ReactNode;
};

export default function LibraryLayout({ tab, children }: LibraryLayoutProps) {
    const navigate = useNavigate();

    return (
        <BaseLayout>
            <div className="w-100 m-3" style={{ height: NAVBAR_HEIGHT }}/>

            <div className="d-flex flex-column gap-3 w-100 h-100">
                {/* Tabs */}
                <div className="d-flex flex-row gap-3 px-3">
                    <button className={tab === 0 ? "btn btn-primary p-3 w-100" : "btn btn-dark p-3 w-100"} onClick={() => navigate("/library/worlds")}>
                        Worlds
                    </button>
                    <button className={tab === 1 ? "btn btn-primary p-3 w-100" : "btn btn-dark p-3 w-100"} onClick={() => navigate("/library/campaigns")}>
                        Campaigns
                    </button>
                    <button className={tab === 2 ? "btn btn-primary p-3 w-100" : "btn btn-dark p-3 w-100"} onClick={() => navigate("/library/actors")}>
                        Actors
                    </button>
                    <button className={tab === 3 ? "btn btn-primary p-3 w-100" : "btn btn-dark p-3 w-100"} onClick={() => navigate("/library/items")}>
                        Items
                    </button>
                </div>

                <hr className="text-light px-3 py-0 my-1" />

                {/* Main Content */}
                <div className="w-100 h-auto d-flex flex-column mt-3">
                    {children}
                </div>
            </div>
        </BaseLayout>
    );
}

import LibraryLayout from "@layouts/LibraryLayout";
import WorldsList from "@/features/library/WorldsList";
import { useNavigate } from "react-router-dom";

export default function WorldsPage() {
    const navigate = useNavigate();

    return (
        <LibraryLayout tab={0}>
            <div className="w-100 h-100 d-flex flex-column align-items-center">
                <div className="w-100 d-flex flex-row gap-3 justify-content-center">
                    <button className="col-1 btn btn-primary rounded-pill m-3" onClick={() => navigate("/details/world/new")}>Create</button>
                    <h1 className="col-3 text-light text-center">Your Worlds</h1>
                    <button className="col-1 btn btn-primary rounded-pill m-3" onClick={() => window.location.reload()}>Refresh</button>
                </div>
                <p className="text-primary">Manage your worlds here.</p>
                <WorldsList />
            </div>
        </LibraryLayout>
    );
}

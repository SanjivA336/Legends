import DetailLayout from "@/layouts/WizardLayout";
import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { world_get, world_post} from "@apis/library_api";
import type { WorldPayload } from "@apis/_schemas";

import WorldGeneral from "@/features/wizard/world/WorldGeneral";
import WorldAdvanced from "@/features/wizard/world/WorldAdvanced";
import WorldContext from "@/features/wizard/world/WorldContext";
import WorldFinish from "@/features/wizard/world/WorldFinish";

import ErrorBox from "@/components/modular/ErrorBox";

export default function WorldWizardPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [world, setWorld] = useState<WorldPayload>({
        name: "",
        description: "",
        is_public: false,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>("");
    const [currentTab, setCurrentTab] = useState<number>(0);

    async function fetchData() {
        try {
            setLoading(true);
            const data = await world_get(id ?? "new");
            setWorld({
                name: data.name,
                description: data.description,
                is_public: data.is_public,
            });
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchData();
    }, [id]);

    const handleSave = async () => {
        try {
            setLoading(true);
            alert("Saving world...");
            navigate("/library/worlds");
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <DetailLayout title={id === "new" ? "Create World" : "Edit World"} style={id === "new" ? "stages" : "tabs"} tabs={id === "new" ? ["General", "Settings", "Context", "Finish"] : ["General", "Settings", "Context"]} currentTab={currentTab} setCurrentTab={setCurrentTab}>
            <div className="w-100 h-100 d-flex flex-column gap-2 align-items-center">
                <div className="w-100 h-100 d-flex flex-column gap-3 px-4">
                    {currentTab === 0 && (
                        <WorldGeneral world={world} setWorld={setWorld} />
                    )}
                    {currentTab === 1 && (
                        <WorldAdvanced world={world} setWorld={setWorld} />
                    )}
                    {currentTab === 2 && (
                        <WorldContext world={world} setWorld={setWorld} />
                    )}
                    {currentTab === 3 && (
                        <WorldFinish world={world} handleSave={handleSave} />
                    )}

                    {error && <ErrorBox error={error} />}
                </div>  

                {id === "new" ? (
                    <div className="w-100 d-flex flex-row justify-content-between">
                        {currentTab === 0 ? (
                            <button className="btn btn-danger" onClick={() => navigate("/library/worlds")} disabled={loading}>
                                Cancel
                                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                            </button>
                        ) : (
                            <button className="btn btn-dark" onClick={() => setCurrentTab(currentTab - 1)} disabled={loading}>
                                Previous
                                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                            </button>
                        )}

                        {currentTab === 3 ? (
                            null
                        ) : (
                            <button className="btn btn-dark" onClick={() => setCurrentTab(currentTab + 1)} disabled={loading}>
                                Next
                                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                            </button>
                        )}
                    </div>
                ) : (
                    <div className="w-100 d-flex flex-row justify-content-between">
                        <button className="btn btn-danger" onClick={() => navigate("/library/worlds")} disabled={loading}>
                            Cancel
                            {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                        </button>

                        <button className="btn btn-primary" onClick={() => handleSave()} disabled={loading}>
                            Save
                            {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                        </button>
                    </div>
                )}
            </div>
        </DetailLayout>
    );
}

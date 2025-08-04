import DetailLayout from "@/layouts/WizardLayout";
import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { context_post, world_get, world_post, object_post} from "@apis/library_api";
import type { WorldResponse } from "@apis/_schemas";

import WorldDisplay from "@/features/wizard/world/WorldDisplay";
import WorldSettings from "@/features/wizard/world/WorldSettings";
import WorldCodex from "@/features/wizard/world/WorldCodex";
import WorldFinish from "@/features/wizard/world/WorldFinish";

import MessageBox from "@/components/MessageBox";

export default function WorldWizardPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [world, setWorld] = useState<WorldResponse | null>(null);
    const [oldWorld, setOldWorld] = useState<WorldResponse | null>(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>("");
    const [currentTab, setCurrentTab] = useState<number>(0);

    async function fetchData() {
        try {
            setLoading(true);
            const data: WorldResponse = await world_get(id ?? "new");
            setWorld(data);
            setOldWorld(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchData();
    }, [id]);

    const handleSave = async (route?: string) => {
        try {
            setLoading(true);
            if (!world) {
                throw new Error("World data is not available.");
            }

            const blueprint_ids = world.blueprints.map(element => element.id);

            const contextResponses = await Promise.all(
                world.contexts.map(ctx =>
                    context_post("new", ctx.name, ctx.content)
                )
            );
            const context_ids = contextResponses.map(c => c.id);

            const objectResponses = await Promise.all(
                world.objects.map(obj =>
                    object_post("new", obj.name, obj.description || "", obj.fields, obj.blueprint.id)
                )
            );
            const object_ids = objectResponses.map(o => o.id);


            const response = await world_post(
                world.id,
                world.name,
                world.description || "",
                world.settings.is_public,
                blueprint_ids,
                context_ids,
                object_ids
            );
            setWorld(response);

            if (route) {
                navigate(route);
            }
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <DetailLayout title={id === "new" ? "Create World" : "Edit World"} tabs={id === "new" ? ["Display", "Settings", "Codex", "Finish"] : ["Display", "Settings", "Codex"]} currentTab={currentTab} setCurrentTab={setCurrentTab}>
            <div className="w-100 h-100 d-flex flex-column gap-2 align-items-center">
                <div className="w-100 h-100 d-flex flex-column gap-3 px-4">
                    {currentTab === 0 && (
                        <WorldDisplay world={world} setWorld={setWorld} loadingWorld={loading} />
                    )}
                    {currentTab === 1 && (
                        <WorldSettings world={world} setWorld={setWorld} loadingWorld={loading} />
                    )}
                    {currentTab === 2 && (
                        <WorldCodex world={world} setWorld={setWorld} loadingWorld={loading} />
                    )}
                    {currentTab === 3 && (
                        <WorldFinish world={world} handleSave={handleSave} loadingWorld={loading} />
                    )}

                    {error && <MessageBox error={error} />}
                </div>  

                <div className="w-100 my-3">
                    {id === "new" ? (
                        <div className="w-100 d-flex flex-row justify-content-between">
                            {currentTab === 0 ? (
                                <button className="w-25 btn btn-danger" onClick={() => navigate("/library/worlds")} disabled={loading}>
                                    Cancel
                                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                                </button>
                            ) : (
                                <button className="w-25 btn btn-dark" onClick={() => setCurrentTab(currentTab - 1)} disabled={loading}>
                                    Previous
                                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                                </button>
                            )}

                            {currentTab === 3 ? (
                                null
                            ) : (
                                <button className="w-25 btn btn-dark" onClick={() => setCurrentTab(currentTab + 1)} disabled={loading}>
                                    Next
                                    {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                                </button>
                            )}
                        </div>
                    ) : (
                        <div className="w-100 d-flex flex-row justify-content-between">
                            <button className="w-25 btn btn-danger" onClick={() => navigate("/library/worlds")} disabled={loading}>
                                Cancel
                                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                            </button>

                            <button className="w-25 btn btn-primary" onClick={() => handleSave()} disabled={loading}>
                                Save
                                {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </DetailLayout>
    );
}

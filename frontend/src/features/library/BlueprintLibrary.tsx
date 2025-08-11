import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { blueprints_all_get } from "@apis/library_api";
import type { BlueprintResponse } from "@apis/_schemas";

import BlueprintEditor from "@/features/editors/BlueprintEditor";
import MessageBox from "@/components/MessageBox";
import GenericList from "@features/library/generic/GenericList";

export default function BlueprintLibrary() {
    const [allBlueprints, setAllBlueprints] = useState<BlueprintResponse[]>([]);

    const [showEditor, setShowEditor] = useState<boolean>(false);
    const [currentBlueprintID, setCurrentBlueprintID] = useState<string | "new">("new");

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>("");

    const fetchBlueprints = async () => {
        try {
            setLoading(true);
            setError("");
            const blueprints = await blueprints_all_get();
            setAllBlueprints(blueprints);
        } catch (error) {
            setError("Failed to load blueprints. Please try again later.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchBlueprints();
    }, []);

    const openCreator = () => {
        setCurrentBlueprintID("new");
        setShowEditor(true);
    }

    const openEditor = (blueprint: BlueprintResponse) => {
        setCurrentBlueprintID(blueprint.id);
        setShowEditor(true);
    }

    const renderDetails = (blueprint: BlueprintResponse) => {
        return (
            <>
                <div className="d-flex flex-column gap-2 w-100">
                    <h5 className="card-title">{blueprint.name}</h5>
                    <p className="card-text m-0">{blueprint.description}</p>
                    <p className="card-text m-0"><small className="text-muted">{blueprint.is_public ? "Public" : "Private"}</small></p>
                </div>
                <div className="d-flex flex-column gap-1 w-100">
                    <p className="card-text m-0"><small className="text-muted">{blueprint.fields.length} Fields</small></p>
                    <p className="card-text m-0"><small className="text-muted">Created by {blueprint.creator.username} on {new Date(blueprint.created_at).toLocaleDateString()}</small></p>
                    <p className="card-text m-0"><small className="text-muted">Last updated: {new Date(blueprint.updated_at || blueprint.created_at).toLocaleDateString()}</small></p>
                </div>
            </>
        );
    }

    return (
        <div className="w-100 h-100 d-flex flex-column gap-2 align-items-center">
            <h3>Your Blueprints</h3>
            <p>Here you can manage your blueprints, create new ones, and explore existing blueprints.</p>

            <hr className="text-light w-100 my-2" />

            <GenericList<BlueprintResponse>
                itemName="blueprint"
                items={allBlueprints}
                refresh={fetchBlueprints}
                openCreator={openCreator}
                openEditor={openEditor}
                renderDetails={renderDetails}
                loading={loading}
                search
                getItemName={(blueprint) => blueprint.name}
                viewSelector
                limitSelector
                pagination
            />

            {error && (
                <MessageBox error={error} />
            )}

            <BlueprintEditor
                showEditor={showEditor}
                setShowEditor={setShowEditor}
                blueprint_id={currentBlueprintID}
                availableBlueprints={allBlueprints}
                refresh={fetchBlueprints}
            />
        </div>
    );
}

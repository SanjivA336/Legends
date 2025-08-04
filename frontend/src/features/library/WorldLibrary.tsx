import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { worlds_all_get } from "@apis/library_api";
import type { WorldResponse } from "@apis/_schemas";

import MessageBox from "@/components/MessageBox";
import GenericList from "@features/library/generic/GenericList";

export default function WorldLibrary() {
    const navigate = useNavigate();

    const [allWorlds, setAllWorlds] = useState<WorldResponse[]>([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>("");

    const fetchWorlds = async () => {
        try {
            setLoading(true);
            setError("");
            const worlds = await worlds_all_get();
            setAllWorlds(worlds);
        } catch (error) {
            setError("Failed to load worlds. Please try again later.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchWorlds();
    }, []);

    const openCreator = () => {
        navigate("/details/world/new");
    }

    const openEditor = (world: WorldResponse) => {
        navigate(`/details/world/${world.id}`);
    }
    

    const renderDetails = (world: WorldResponse) => {
        return (
            <>
                <div className="d-flex flex-column gap-2 w-100">
                    <h5 className="card-title">{world.name}</h5>
                    <p className="card-text m-0">{world.description}</p>
                    <p className="card-text m-0"><small className="text-muted">{world.settings.is_public ? "Public" : "Private"}</small></p>
                </div>
                <div className="d-flex flex-column gap-1 w-100">
                    <p className="card-text m-0"><small className="text-muted">{world.contexts.length} Contexts</small></p>
                    <p className="card-text m-0"><small className="text-muted">{world.blueprints.length} Blueprints</small></p>
                    <p className="card-text m-0"><small className="text-muted">{world.objects.length} Objects</small></p>
                </div>
                <div className="d-flex flex-column gap-1 w-100">
                    <p className="card-text m-0"><small className="text-muted">Created by {world.creator.username} on {new Date(world.created_at).toLocaleDateString()}</small></p>
                    <p className="card-text m-0"><small className="text-muted">Last updated: {new Date(world.updated_at || world.created_at).toLocaleDateString()}</small></p>
                </div>
            </>
        );
    }

    return (
        <div className="w-100 h-100 d-flex flex-column gap-2 align-items-center">
            <h3>Your Worlds</h3>
            <p>Here you can manage your worlds, create new ones, and explore existing worlds.</p>

            <hr className="text-light w-100 my-2" />

            <GenericList<WorldResponse>
                itemName="world"
                items={allWorlds}
                refresh={fetchWorlds}
                openCreator={openCreator}
                openEditor={openEditor}
                renderDetails={renderDetails}
                loading={loading}
                search
                getItemName={(world) => world.name}
                viewSelector
                limitSelector
                pagination
            />

            {error && (
                <MessageBox error={error} />
            )}

        </div>
    );
}

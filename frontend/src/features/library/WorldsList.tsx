import { useState } from "react";
import type { WorldResponse } from "@/apis/_schemas";
import { useNavigate } from "react-router-dom";
import { worlds_all_get } from "@/apis/library_api";

type WorldsListProps = {
    numResults?: number;
}

const WorldsList = ({ numResults }: WorldsListProps) => {
    const [worlds, setWorlds] = useState<WorldResponse[]>([]);
    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);

    async function fetchWorlds() {
        setLoading(true);
        try {
            const response = await worlds_all_get();
            setWorlds(response);
        } catch (error) {
            console.error("Failed to fetch worlds:", error);
        } finally {
            setLoading(false);
        }
    }

    useState(() => {

        fetchWorlds();
    }, []);


    return (
        <div className="w-100 h-100 align-items-center" >
            {loading ? (
                <div className="d-grid gap-3" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))" }}>
                    {Array.from({ length: 20 }, (_, i) => (
                        <div key={i} className="card bg-dark text-light rounded-3 p-3">
                            <div className="placeholder-glow">
                                <h4 className="w-100 placeholder">Default World Name</h4>
                                <hr className="mx-5 my-2 text-light" />
                                <div className="text-start d-flex flex-column">
                                    <p className="w-100 placeholder">Default description for a default world</p>
                                    <p className="w-75 placeholder">Creator: creator_name</p>
                                    <p className="w-50 placeholder"># Context Cards</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (worlds.length === 0) ? (
                <div className="text-light text-center">
                    <p>No worlds found.</p>
                    <button className="btn btn-primary" onClick={() => navigate("/details/world/new")}>
                        Create one now!
                    </button>
                </div>
            ) : (
                <div className="d-grid gap-3" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))" }}>
                    {worlds.slice(0, numResults).map((world, i) => (
                        <a href={`/details/world/${world.id}`} key={i} className="bg-dark text-decoration-none text-light rounded-3 p-4">
                            <h4 className="text-center">{world.name}</h4>
                            <hr className="mx-5 my-2 text-light" />
                            <div className="text-start d-flex flex-column">
                                <p>{world.description}</p>
                                <p>Creator: {world.creator.username}</p>
                                <p># Context Cards</p>
                            </div>
                        </a>
                    ))}
                </div>
            )}
        </div>
    );
};

export default WorldsList;

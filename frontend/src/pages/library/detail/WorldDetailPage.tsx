import DetailLayout from "@layouts/DetailLayout";
import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { world_get, world_post} from "@apis/library_api";
import type { WorldPayload, WorldResponse, CampaignResponse } from "@apis/_schemas";

import TextField from "@/components/modular/TextField";
import ErrorBox from "@/components/modular/ErrorBox";

export default function WorldDetailPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [world, setWorld] = useState<WorldPayload>({
        name: "",
        description: "",
        is_public: false,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>("");

    useEffect(() => {
        async function fetchData() {
            try {
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
        fetchData();
    }, [id]);

    async function handleSubmit() {
        try {
            const response = await world_post(
                id ?? "new",
                world.name,
                world.description,
                world.is_public
            );
            navigate(`/library/worlds`);
        } catch (err: any) {
            alert(err.message);
        }
    }

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <DetailLayout>
            <div className="w-100 h-100 d-flex flex-column align-items-center">
                <h1 className="text-light">{id === "new" ? "Create World" : "Edit World"}</h1>

                <TextField
                    label="World Name"
                    value={world.name}
                    setValue={(value) => setWorld({ ...world, name: value })}
                    placeholder="Enter world name"
                    required={true}/>

                <TextField
                    label="Description"
                    value={world.description || ""}
                    setValue={(value) => setWorld({ ...world, description: value })}
                    placeholder="Enter world description"
                    required={false}/>

                <ErrorBox error={error} />

                <button className="btn btn-primary mt-3" onClick={handleSubmit}>
                    {id === "new" ? "Create World" : "Save Changes"}
                </button>
            </div>
        </DetailLayout>
    );
}

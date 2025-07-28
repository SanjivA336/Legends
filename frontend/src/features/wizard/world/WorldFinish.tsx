import type { WorldPayload } from "@apis/_schemas";
import { useNavigate } from "react-router-dom";

type WorldFinishProps = {
    world: WorldPayload;
    handleSave: () => Promise<void>;
};

export default function WorldFinish({ world, handleSave }: WorldFinishProps) {

    const navigate = useNavigate();
    const saveAndExit = async () => {
        await handleSave();
        navigate("/library/worlds");
    }
    
    const saveAndCampaign = async () => {
        await handleSave();
        navigate("/library/campaigns/new");
    }

    return (
        <div className="w-100 d-flex flex-column gap-2">
            <h2>Next Steps</h2>

            <div className="w-auto h-auto p-4 bg-dark rounded-4 d-flex flex-column gap-3 text-center">
                <p >
                    Your world, <strong>{world.name}</strong>, will now be created.
                    <br />
                    <br />
                    What would you like to do next?
                </p>

                <button className="btn btn-primary" onClick={saveAndExit}>
                    Save and go to library
                </button>
                
                <button className="btn btn-primary" onClick={saveAndCampaign}>
                    Save and create a new campaign
                </button>

            </div>
        </div>
    );
}
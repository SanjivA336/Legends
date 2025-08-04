import type { WorldResponse } from "@apis/_schemas";

import ButtonField from "@/components/fields/ButtonField";

import Loading from "@/components/Loading";

type WorldFinishProps = {
    world: WorldResponse | null;
    handleSave: (route: string) => Promise<void>;
    loadingWorld: boolean;
};

export default function WorldFinish({ world, handleSave, loadingWorld }: WorldFinishProps) {
    const saveAndExit = async () => {
        await handleSave("/library/worlds");
    }
    
    const saveAndCampaign = async () => {
        await handleSave("/library/campaigns/new");
    }

    return (
        <div className="w-100 d-flex flex-column gap-2">
            <h2 className="text-center">Next Steps</h2>

            {loadingWorld ? (
                <div className="w-100 h-100 d-flex flex-column align-items-center p-3">
                    <Loading />
                </div>
            ) : (
                <>
                    <div className="w-auto h-auto p-4 bg-dark rounded-4 d-flex flex-column gap-3 text-center">
                        <p >
                            Your world, <strong>{world?.name}</strong>, will now be created.
                            <br />
                            <br />
                            What would you like to do next?
                        </p>

                        <ButtonField
                            onClick={saveAndCampaign}
                            type="submit"
                            color="primary"
                            rounding="pill"
                        >
                            Save and Create Campaign
                        </ButtonField>

                        <ButtonField
                            onClick={saveAndExit}
                            type="submit"
                            color="primary"
                            rounding="pill"
                        >
                            Save and Exit
                        </ButtonField>
                    </div>
                </>
            )}
        </div>
    );
}
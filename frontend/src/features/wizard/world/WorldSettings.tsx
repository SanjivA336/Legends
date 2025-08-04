import type { WorldResponse } from "@apis/_schemas";

import ToggleField from "@/components/fields/ToggleField";

import Loading from "@/components/Loading";

type WorldSettingsProps = {
    world: WorldResponse | null;
    setWorld: (world: WorldResponse) => void;
    loadingWorld?: boolean;
};

export default function WorldSettings({ world, setWorld, loadingWorld }: WorldSettingsProps) {
    return (
        <div className="w-100 d-flex flex-column gap-2">
            <h2 className="text-center">World Settings</h2>
            
            {loadingWorld ? (
                <div className="w-100 h-100 d-flex flex-column align-items-center p-3">
                    <Loading />
                </div>
            ) : (
                <>
                    <ToggleField
                        value={world?.settings.is_public || false}
                        setValue={(value) => world && setWorld({ ...world, settings: { ...world.settings, is_public: value } })}
                        label="Public"
                        type="switch"
                    />
                </>
            )}

        </div>
    );
}
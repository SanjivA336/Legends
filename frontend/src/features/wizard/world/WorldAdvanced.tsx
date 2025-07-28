import type { WorldPayload } from "@apis/_schemas";

import ToggleField from "@/components/modular/ToggleField";

type WorldAdvancedProps = {
    world: WorldPayload;
    setWorld: (world: WorldPayload) => void;
};

export default function WorldAdvanced({ world, setWorld }: WorldAdvancedProps) {
    return (
        <div className="w-100 d-flex flex-column gap-2">
            <h2>Advanced World Settings</h2>

            <ToggleField
                label="Is Public"
                value={world.is_public || false}
                setValue={(value) => setWorld({ ...world, is_public: value })}
            />

        </div>
    );
}
import type { WorldPayload } from "@apis/_schemas";

import TextField from "@/components/modular/TextField";
import LongTextField from "@/components/modular/LongTextField";


type WorldGeneralProps = {
    world: WorldPayload;
    setWorld: (world: WorldPayload) => void;
};

export default function WorldGeneral({ world, setWorld }: WorldGeneralProps) {
    return (
        <div className="w-100 d-flex flex-column gap-2">
            <h2>General World Settings</h2>

            <TextField
                label="World Name"
                value={world.name}
                setValue={(value) => setWorld({ ...world, name: value })}
                placeholder="Enter world name"
                required={true}/>

            <LongTextField
                label="World Description"
                value={world.description || ""}
                setValue={(value) => setWorld({ ...world, description: value })}
                placeholder="Enter a brief description of your world"
                required={false}
                rows={3}/>
        </div>
    );
}
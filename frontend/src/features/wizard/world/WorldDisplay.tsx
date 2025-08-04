import type { WorldResponse } from "@apis/_schemas";

import ShortTextField from "@/components/fields/ShortTextField";
import LongTextField from "@/components/fields/LongTextField";

import Loading from "@/components/Loading";

type WorldDisplayProps = {
    world: WorldResponse | null;
    setWorld: (world: WorldResponse) => void;
    loadingWorld?: boolean;
};

export default function WorldDisplay({ world, setWorld, loadingWorld }: WorldDisplayProps) {
    return (
        <div className="w-100 d-flex flex-column gap-2">
            <h2 className="text-center">General World Settings</h2>

            {loadingWorld ? (
                <div className="w-100 h-100 d-flex flex-column align-items-center p-3">
                    <Loading />
                </div>
            ) : (
                <>
                    <ShortTextField
                        label="World Name"
                        value={world?.name || ""}
                        setValue={(value) => world && setWorld({ ...world, name: value })}
                        placeholder="Enter world name"
                        required={true}/>

                    <LongTextField
                        label="World Description"
                        value={world?.description || ""}
                        setValue={(value) => world && setWorld({ ...world, description: value })}
                        placeholder="Enter a brief description of your world"
                        required={false}
                        rows={3}/>
                </>
            )}
        </div>
    );
}
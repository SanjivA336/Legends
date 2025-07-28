import type { WorldPayload } from "@apis/_schemas";

type WorldContextProps = {
    world: WorldPayload;
    setWorld: (world: WorldPayload) => void;
};

export default function WorldContext({  }: WorldContextProps) {
    return (
        <div className="w-100 d-flex flex-column gap-2">
            <h2>World Context</h2>

            <h1>Nothing here yet :(</h1>

        </div>
    );
}
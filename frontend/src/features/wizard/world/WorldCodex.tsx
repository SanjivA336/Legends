import type { WorldResponse, BlueprintResponse, ContextResponse, ObjectResponse } from "@apis/_schemas";
import { useEffect, useState } from "react";

import { blueprints_all_get } from "@/apis/library_api";

import BlueprintEditor from "@/features/editors/BlueprintEditor";
import ContextEditor from "@/features/editors/ContextEditor";
import ObjectEditor from "@/features/editors/ObjectEditor";

import MessageBox from "@/components/MessageBox";
import ButtonField from "@/components/fields/ButtonField";
import Modal from "@/components/design/Modal";
import GenericList from "@/features/library/generic/GenericList";

import Loading from "@/components/Loading";
import DropdownField from "@/components/fields/DropdownField";

type WorldCodexProps = {
    world: WorldResponse | null;
    setWorld: (world: WorldResponse) => void;
    loadingWorld?: boolean;
};

export default function WorldCodex({ world, setWorld, loadingWorld }: WorldCodexProps) {

    const [availableBlueprints, setAvailableBlueprints] = useState<BlueprintResponse[]>([]);
    const [showBlueprintEditor, setShowBlueprintEditor] = useState<boolean>(false);
    const [currentBlueprint, setCurrentBlueprint] = useState<BlueprintResponse | null>(null);

    const [showBlueprintSelector, setShowBlueprintSelector] = useState<boolean>(false);
    const [highlightedBlueprint, setHighlightedBlueprint] = useState<BlueprintResponse | null>(null);

    const [loadingBlueprints, setLoadingBlueprints] = useState<boolean>(true);

    const [showContextEditor, setShowContextEditor] = useState<boolean>(false);
    const [currentContext, setCurrentContext] = useState<ContextResponse | null>(null);

    const [showObjectEditor, setShowObjectEditor] = useState<boolean>(false);
    const [currentObject, setCurrentObject] = useState<ObjectResponse | null>(null);

    const [filteredObjects, setFilteredObjects] = useState<ObjectResponse[]>(world?.objects || []);
    const [blueprintFilter, setBlueprintFilter] = useState<string>("");

    const [error, setError] = useState("");

    const fetchBlueprints = async () => {
        try {
            setLoadingBlueprints(true);
            setError("");
            const data: BlueprintResponse[] = await blueprints_all_get();
            setAvailableBlueprints(data);
        } catch (error) {
            setError("Failed to load blueprints. Please try again later.");
        } finally {
            setLoadingBlueprints(false);
        }
    }

    useEffect(() => {
        fetchBlueprints();
    }, []);

    const addBlueprint = () => {
        if (highlightedBlueprint && world) {
            setWorld({
                ...world,
                blueprints: [...(world.blueprints || []), highlightedBlueprint],
            });
        }
        setShowBlueprintSelector(false);
        setHighlightedBlueprint(null);
    }

    const filterObjects = () => {
        if (blueprintFilter === "" || blueprintFilter === null) {
            setFilteredObjects(world?.objects || []);
        } else {
            setFilteredObjects(world?.objects.filter(object => object.blueprint.id === blueprintFilter) || []);
        }
    }

    const blueprintRenderDetails = (blueprint: BlueprintResponse) => {
        return (
            <>
                <div className="d-flex flex-column gap-2 w-100">
                    <h5 className="card-title">{blueprint.name}</h5>
                    <p className="card-text m-0">{blueprint.description}</p>
                </div>
                <div className="d-flex flex-column gap-1 w-100">
                    <p className="card-text m-0"><small className="text-muted">{blueprint.fields.length} Fields</small></p>
                </div>
            </>
        );
    }

    const contextRenderDetails = (context: ContextResponse) => {
        return (
            <>
                <div className="d-flex flex-column gap-2 w-100">
                    <h5 className="card-title overflow-hidden">{context.name}</h5>
                </div>
                <div className="d-flex flex-column gap-1 w-100">
                    <p className="card-text m-0 overflow-hidden"><small className="text-muted">{context.content}</small></p>
                </div>
            </>
        );
    }

    const objectRenderDetails = (object: ObjectResponse) => {
        return (
            <>
                <div className="d-flex flex-column gap-2 w-100">
                    <h5 className="card-title">{object.name}</h5>
                    <p className="card-text m-0">{object.description}</p>
                </div>
                <div className="d-flex flex-column gap-1 w-100">
                    <p className="card-text m-0"><small className="text-muted">{object.fields.length} Fields</small></p>
                </div>
            </>
        );
    }

    return (
        <div className="w-100 d-flex flex-column gap-3">
            <h2 className="text-center">World Codex</h2>
            {loadingWorld ? (
                <div className="w-100 d-flex flex-column align-items-center p-3">
                    <Loading />
                </div>
            ) : (
                <>
                    
                    {/* Contexts */}
                    <div className="w-100 h-100 d-flex bg-darker p-4 border-darkish rounded-4 flex-column align-items-center justify-content-start gap-2">

                        <h3 className="text-center text-nowrap">Contexts</h3>

                        <GenericList<ContextResponse>
                            itemName="context"
                            items={world?.contexts || []}
                            openCreator={() => {setShowContextEditor(true); setCurrentContext(null)}}
                            openEditor={(context) => {setShowContextEditor(true); setCurrentContext(context);}}
                            renderDetails={contextRenderDetails}
                            search
                            getItemName={(context) => context.name}
                            defaultLimit={8}
                            defaultView="grid"
                            pagination
                        />

                        {/* Context Editor */}
                        <ContextEditor
                            showEditor={showContextEditor}
                            setShowEditor={setShowContextEditor}
                            context={currentContext || undefined}
                            setContext={setCurrentContext}
                            parentWorld={world}
                            setParentWorld={setWorld}
                        />

                    </div>

                    {/* Blueprints */}
                    <div className="w-100 h-100 d-flex bg-darker p-4 border-darkish rounded-4 flex-column align-items-center justify-content-start gap-2">

                        <h3 className="text-center text-nowrap">Blueprints</h3>

                        <GenericList<BlueprintResponse>
                            itemName="blueprint"
                            items={world?.blueprints || []}
                            openCreator={() => {setShowBlueprintEditor(true); setCurrentBlueprint(null)}}
                            renderDetails={blueprintRenderDetails}
                            search
                            getItemName={(blueprint) => blueprint.name}
                            defaultLimit={8}
                            defaultView="grid"
                            pagination
                        >
                            <ButtonField
                                onClick={() => setShowBlueprintSelector(true)}
                                className="p-2 text-nowrap">
                                Add Existing
                            </ButtonField>
                        </GenericList>

                        {/* Blueprint Editor */}
                        <BlueprintEditor
                            showEditor={showBlueprintEditor}
                            setShowEditor={setShowBlueprintEditor}
                            blueprint={currentBlueprint || undefined}
                            setBlueprint={setCurrentBlueprint}
                            availableBlueprints={world?.blueprints || []}
                            refresh={fetchBlueprints}
                            parentWorld={world}
                            setParentWorld={setWorld}
                        />

                        {/* Blueprint Selector */}
                        <Modal
                            title="Add Blueprint"
                            showModal={showBlueprintSelector}
                            setShowModal={setShowBlueprintSelector}
                            onClose={() => setHighlightedBlueprint(null)}>

                            <h1 className="text-center my-3">Select a Blueprint</h1>

                            <ButtonField
                                onClick={addBlueprint}
                                loading={loadingBlueprints}
                                disabled={highlightedBlueprint === null}
                                >
                                    <h4 className="m-0">Add Blueprint</h4>
                            </ButtonField>

                            <div className="w-100 bg-darkest p-3 rounded-4">
                                <GenericList<BlueprintResponse>
                                    itemName="blueprint"
                                    items={availableBlueprints.filter(blueprint => !world?.blueprints.some(b => b.id === blueprint.id))}
                                    refresh={fetchBlueprints}
                                    renderDetails={blueprintRenderDetails}
                                    loading={loadingBlueprints}
                                    search
                                    getItemName={(blueprint) => blueprint.name}
                                    viewSelector
                                    pagination
                                    highlighted={highlightedBlueprint}
                                    setHighlighted={setHighlightedBlueprint}
                                />
                            </div>
                        </Modal>
                    </div>

                    {/* Objects */}
                    <div className="w-100 h-100 d-flex bg-darker p-4 border-darkish rounded-4 flex-column align-items-center justify-content-start gap-2">

                        <h3 className="text-center text-nowrap">Objects</h3>

                        <GenericList<ObjectResponse>
                            itemName="object"
                            items={world?.objects || []}
                            openCreator={() => {setShowObjectEditor(true); setCurrentObject(null)}}
                            openEditor={(object) => {setShowObjectEditor(true); setCurrentObject(object);}}
                            renderDetails={objectRenderDetails}
                            search
                            getItemName={(object) => object.name}
                            defaultLimit={8}
                            defaultView="grid"
                            pagination
                        >
                            <DropdownField
                                value={blueprintFilter}
                                setValue={setBlueprintFilter}
                                prepend="Filter"
                                options={[...world?.blueprints || [], { id: "", name: "None" }]}
                                optionValue={(blueprint) => (blueprint.id)}
                                optionLabel={(blueprint) => (blueprint.name)}
                            />
                        </GenericList>

                        {/* Context Editor */}
                        <ObjectEditor
                            showEditor={showObjectEditor}
                            setShowEditor={setShowObjectEditor}
                            object={currentObject || undefined}
                            setObject={setCurrentObject}
                            parentWorld={world}
                            setParentWorld={setWorld}
                        />

                    </div>
                </>
            )}
        </div>
    );
}
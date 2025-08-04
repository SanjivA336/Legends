import { useEffect, useState } from "react";

import { blueprint_get, blueprint_post, blueprint_delete } from "@/apis/library_api";
import type { BlueprintResponse, WorldResponse } from "@apis/_schemas";
import { VALID_BLUEPRINT_TYPES } from "@apis/_schemas";

import ShortTextField from "@/components/fields/ShortTextField";
import LongTextField from "@/components/fields/LongTextField";
import DropdownField from "@/components/fields/DropdownField";

import ToggleField from "@/components/fields/ToggleField";
import NumberField from "@/components/fields/NumberField";

import TabGroup from "@/components/TabGroup";

import Loading from "@components/Loading";

import MessageBox from "@/components/MessageBox";
import Modal from "@/components/design/Modal";
import ButtonField from "@/components/fields/ButtonField";

import DeletePopup from "@/components/DeletePopup";

type BlueprintEditorProps = {
    showEditor: boolean;
    setShowEditor: (show: boolean) => void;
    blueprint?: BlueprintResponse;
    setBlueprint?: (blueprint: BlueprintResponse) => void;
    availableBlueprints?: BlueprintResponse[];
    refresh?: () => void;
    parentWorld?: WorldResponse | null;
    setParentWorld?: (world: WorldResponse) => void;
};

export default function BlueprintEditor({ showEditor, setShowEditor, blueprint, setBlueprint, availableBlueprints, refresh, parentWorld, setParentWorld }: BlueprintEditorProps) {
    const [localBlueprint, setLocalBlueprint] = useState<BlueprintResponse | null>(null);

    const [tabNumber, setTabNumber] = useState<number>(0);

    const [showDelete, setShowDelete] = useState<boolean>(false);

    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>("");

    const fetchBlueprint = async () => {
        setLoading(true);
        setError("");

        try{
            if (blueprint) {
                setLocalBlueprint(blueprint);
            } else {
                const data: BlueprintResponse = await blueprint_get("new")
                setLocalBlueprint(data);
            }
        } catch (err) {
                setError("Failed to fetch blueprint data.");
        } finally {
            setLoading(false);
        }
    }

    const handleSave = async () => {
        if (!localBlueprint) return;

        if(loading) return;

        try{
            setLoading(true);
            setError("");
            let savedBlueprint: BlueprintResponse | null = null;
            if(blueprint !== undefined){
                setBlueprint?.(localBlueprint);
                savedBlueprint = await blueprint_post(
                    localBlueprint.id, 
                    localBlueprint.name, 
                    localBlueprint.description || "", 
                    localBlueprint.fields
                );
            } else {
                savedBlueprint = await blueprint_post(
                    "new", 
                    localBlueprint.name, 
                    localBlueprint.description || "", 
                    localBlueprint.fields
                );
            }

            if (parentWorld && setParentWorld && savedBlueprint) {
                const existingBlueprints = parentWorld.blueprints || [];

                const updatedBlueprints = existingBlueprints.some(bp => bp.id === savedBlueprint.id)
                    ? existingBlueprints.map(bp =>
                        bp.id === savedBlueprint.id ? savedBlueprint : bp
                    )
                    : [...existingBlueprints, savedBlueprint];

                setParentWorld({
                    ...parentWorld,
                    blueprints: updatedBlueprints,
                });
            }

            setLocalBlueprint(null);
            setShowEditor(false);
            refresh?.();
        } catch (err) {
            setError("Failed to save blueprint data.");
        } finally {
            fetchBlueprint();
            setLoading(false);
        }
    }

    const handleDelete = async () => {
        if(blueprint){
            try{
                setLoading(true);
                await blueprint_delete(blueprint.id);
            }
            catch (err){
                setError(String(err));
            } finally{
                setLoading(false);
            }
            setShowEditor(false);
            refresh?.();
        }
    }

    useEffect(() => {
        refresh?.();
        fetchBlueprint();
    }, [blueprint]);

    
    const addField = () => {
        if (!localBlueprint) return;

        setError("");

        setLocalBlueprint({
            ...localBlueprint,
            fields: [...localBlueprint.fields, { name: "", type: "text", value: "" }]
        });
    }


    const removeField = (index: number) => {
        if (!localBlueprint) return;

        setError("");

        setLocalBlueprint({
        ...localBlueprint,
        fields: localBlueprint.fields.filter((_, i) => i !== index)
        });
    }


    const addOptionToField = (index: number, option: string) => {
        if (!localBlueprint) return;

        setError("");

        const newFields = [...localBlueprint.fields];
        const field = newFields[index];

        if (field.type !== "select") {
        setError("Only select fields can have options.");
        return;
        }

        if (!field.options) {
        field.options = [];
        }

        if (field.options.includes(option)) {
        setError("Option already exists.");
        return;
        }

        field.options.push(option);

        setLocalBlueprint({
            ...localBlueprint,
            fields: newFields
        });
    }


    const removeOptionFromField = (index: number, option: string) => {
        if (!localBlueprint) return;

        setError("");

        const newFields = [...localBlueprint.fields];
        const field = newFields[index];

        if (field.type !== "select") {
            setError("Only select fields can have options.");
            return;
        }

        if (!field.options || !field.options.includes(option)) {
            setError("Option does not exist.");
            return;
        }

        field.options = field.options.filter(opt => opt !== option);

        setLocalBlueprint({
            ...localBlueprint,
            fields: newFields
        });
    }

    return (
        <Modal
            title={blueprint ? "Edit Blueprint" : "Create Blueprint"}
            showModal={showEditor}
            setShowModal={setShowEditor}
            onClose={fetchBlueprint}
            >

            <DeletePopup
                showModal={showDelete}
                setShowModal={setShowDelete}
                title="Delete Blueprint"
                onConfirm={handleDelete}
            >
                <p>
                    Are you sure you want to delete this blueprint?
                    <br/>
                    All connected objects will also be deleted.
                    <br/>
                    The blueprint will be removed from all Worlds and Campaigns.
                </p>
            </DeletePopup>

            {loading ? (
                <Loading />
            ) : (localBlueprint ? (
                <form className="d-flex flex-column gap-3" onSubmit={handleSave}>
                    <h1 className="text-center">{blueprint?.name || "My Blueprint"}</h1>
                    <TabGroup
                        tabNumber={tabNumber}
                        setTabNumber={setTabNumber}
                        disabled={loading}
                        orientation="horizontal"
                        rounding="3"
                        tabNames={["General", "Fields"]}
                    />
                    { tabNumber === 0 && (
                        <div className="d-flex flex-column gap-3">
                            <h3 className="text-center">General</h3>
                            <ShortTextField
                                value={localBlueprint.name}
                                setValue={(value) => setLocalBlueprint({ ...localBlueprint, name: value })}
                                placeholder="Blueprint Name"
                                label="Name"
                                required={true}
                                />

                            <LongTextField
                                value={localBlueprint.description || ""}
                                setValue={(value) => setLocalBlueprint({ ...localBlueprint, description: value })}
                                placeholder="Description"
                                label="Description"
                                required={false}
                                />

                            <ToggleField
                                value={localBlueprint.is_public || false}
                                setValue={(value) => setLocalBlueprint({ ...localBlueprint, is_public: value })}
                                label="Public"
                                type="switch"
                            />
                        </div>
                    )}
                    { tabNumber === 1 && (
                        <div className="d-flex flex-column gap-3">
                            <h3 className="text-center">Fields</h3>
                            { /* Field Iterator*/}
                            {localBlueprint.fields.map((field, index) => (
                                <div key={index} className="d-flex flex-column gap-3 w-100">
                                    <div className="d-flex flex-row w-100 align-items-end">
                                        {/* Field Index */}
                                        <div className="col-2 text-center text-light d-flex flex-column p-2 px-4 bg-darkish rounded-pill text-nowrap overflow-hidden me-2">
                                            {field.name ? field.name : `Field ${index}`}
                                        </div>

                                        {/* Field Type */}
                                        <div className="w-100 px-1">
                                            <DropdownField
                                                value={field.type}
                                                setValue={(value) => {
                                                    const updatedFields = [...localBlueprint.fields];
                                                    updatedFields[index].type = value;
                                                    setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                }}
                                                label="Type"
                                                required
                                                options={[...VALID_BLUEPRINT_TYPES]}
                                                optionValue={(type) => type}
                                                optionLabel={(type) => type}
                                            />
                                        </div>

                                        {/* Field Name */}
                                        <div className="w-100 px-1">
                                            <ShortTextField
                                                value={field.name}
                                                setValue={(value) => {
                                                    const updatedFields = [...localBlueprint.fields];
                                                    updatedFields[index].name = value;
                                                    setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                }}
                                                placeholder="Name"
                                                label="Name"
                                                required
                                            />
                                        </div>

                                        {/* Field Default Value */}
                                        <div className="w-100 px-1">
                                            {field.type === "text" && (
                                                <ShortTextField
                                                    value={field.value || ""}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localBlueprint.fields];
                                                        updatedFields[index].value = value;
                                                        setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                    }}
                                                    placeholder="Default Value"
                                                    label="Default Value"
                                                    required
                                                />
                                            )}
                                            {field.type === "number" && (
                                                <NumberField
                                                    value={field.value ? Number(field.value) : 0}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localBlueprint.fields];
                                                        updatedFields[index].value = value.toString();
                                                        setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                    }}
                                                    placeholder="Default Value"
                                                    label="Default Value"
                                                    required
                                                    incrementer
                                                />
                                            )}
                                            {field.type === "boolean" && (
                                                <DropdownField
                                                    value={field.value ? field.value.toString() : "false"}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localBlueprint.fields];
                                                        updatedFields[index].value = (value === "true" ? "true" : "false");
                                                        setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                    }}
                                                    label="Default Value"
                                                    required
                                                    options={["true", "false"]}
                                                    optionValue={(option) => option}
                                                    optionLabel={(option) => option.charAt(0).toUpperCase() + option.slice(1)}
                                                />
                                            )}
                                            {field.type === "select" && (
                                                <DropdownField
                                                    value={field.value || ""}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localBlueprint.fields];
                                                        updatedFields[index].value = value;
                                                        setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                    }}
                                                    label="Default Value"
                                                    required
                                                    options={field.options || []}
                                                    optionValue={(option) => option}
                                                    optionLabel={(option) => option.charAt(0).toUpperCase() + option.slice(1)}
                                                />
                                            )}
                                            {field.type === "blueprint" && (
                                                <DropdownField
                                                    value={field.value || ""}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localBlueprint.fields];
                                                        updatedFields[index].value = value;
                                                        setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                    }}
                                                    label="Default Value"
                                                    required
                                                    options={availableBlueprints?.filter(bp => bp.id !== localBlueprint.id) || []}
                                                    optionValue={(blueprint) => blueprint.id}
                                                    optionLabel={(blueprint) => blueprint.name}
                                                />
                                            )}
                                        </div>


                                        {/* Remove Field Button */}
                                        <div className="w-25 px-1">
                                            <ButtonField
                                                onClick={() => removeField(index)}
                                                color="danger"
                                                rounding="pill"
                                                outlineVariant
                                                className="p-2"
                                            >
                                                Remove
                                            </ButtonField>
                                        </div>

                                    </div>
                                    {/* Field Options for Select Type */}
                                    {field.type === "select" && (
                                        <div className="d-flex flex-row gap-3">
                                            {/* Add Option Button */}
                                            <button className="btn btn-outline-primary w-25 h-100" onClick={() => addOptionToField(index, "")} type="button">
                                                Add Option
                                            </button>
                                            <div className="w-100 d-flex flex-column gap-1 me-1">
                                                {/* Options Iterator */}
                                                {field.options && field.options.map((option, optionIndex) => (
                                                    <div key={optionIndex} className="d-flex flex-row w-100 align-items-center my-1">
                                                        {/* Option Value */}
                                                        <ShortTextField
                                                            value={option}
                                                            setValue={(value) => {
                                                                const updatedFields = [...localBlueprint.fields];
                                                                updatedFields[index].options![optionIndex] = value;
                                                                setLocalBlueprint({ ...localBlueprint, fields: updatedFields });
                                                            }}
                                                            placeholder="Value"
                                                            prepend={`Option ${optionIndex + 1}`}
                                                            required
                                                            caps="start"
                                                        />

                                                        {/* Remove Option Button */}
                                                        <div>
                                                            <ButtonField
                                                                onClick={() => removeOptionFromField(index, option)}
                                                                color="danger"
                                                                outlineVariant
                                                                caps="end"
                                                                className="py-2 px-3"
                                                            >
                                                                ✖
                                                            </ButtonField>
                                                        </div>

                                                    </div>
                                                ))}
                                            </div>

                                        </div>
                                    )}
                                </div>
                                

                            ))}
                            <button className="btn btn-outline-primary" type="button" onClick={addField}>
                                Add Field
                            </button>
                        </div>
                    )}

                    {error && <MessageBox error={error} />}
                    <hr />

                    <div className="d-flex flex-row gap-3">
                        {blueprint ? (
                            <ButtonField
                                onClick={() => setShowDelete(true)}
                                color="danger"
                                rounding="3"
                            >
                                Delete
                            </ButtonField>
                        ) : (
                            <ButtonField
                                onClick={() => setShowEditor(false)}
                                color="danger"
                                rounding="3"
                            >
                                Cancel
                            </ButtonField>
                        )}
                        <ButtonField
                            onClick={handleSave}
                            color="primary"
                            loading={loading}
                            rounding="3"
                        >
                            {blueprint ? "Save Changes" : "Create Blueprint"}
                        </ButtonField>
                    </div>
                </form>
            ) : (
                <div className="w-100 h-100 text-center d-flex flex-column align-items-center justify-content-center">
                    {error && <MessageBox error={error} />}
                </div>
            ))}
            
        </Modal>
    );
}
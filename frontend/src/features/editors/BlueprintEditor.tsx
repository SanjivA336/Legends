import { use, useEffect, useState } from "react";

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
    blueprint_id?: string | "new";
    availableBlueprints?: BlueprintResponse[];
    refresh?: () => void;
    parentWorld?: WorldResponse | null;
    setParentWorld?: (world: WorldResponse) => void;
};

export default function BlueprintEditor({ showEditor, setShowEditor, blueprint_id="new", availableBlueprints, refresh, parentWorld, setParentWorld }: BlueprintEditorProps) {
    const [localBlueprint, setLocalBlueprint] = useState<BlueprintResponse | null>(null);

    const [tabNumber, setTabNumber] = useState<number>(0);

    const [showDelete, setShowDelete] = useState<boolean>(false);

    const [speedCreate, setSpeedCreate] = useState<boolean>(false);

    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>("");
    const [isDirty, setIsDirty] = useState<boolean>(false);

    const fetchBlueprint = async () => {
        setLoading(true);
        setError("");
        try{
            const data: BlueprintResponse = await blueprint_get(blueprint_id);
            setLocalBlueprint(data);
        } catch (err) {
            setError("Failed to fetch blueprint data: " + String(err));
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

            // Data Validation
            if (!localBlueprint.name) {
                setError("Blueprint name is required.");
                return;
            }

            if (!localBlueprint.fields || localBlueprint.fields.length === 0) {
                setError("At least one field is required.");
                return;
            }

            for (const field of localBlueprint.fields) {
                if (!field.name || field.name.trim() === "") {
                    setError("All fields must have a name.");
                    return;
                }
                if (!field.type || !VALID_BLUEPRINT_TYPES.includes(field.type as typeof VALID_BLUEPRINT_TYPES[number])) {
                    setError("All fields must have a valid type.");
                    return;
                }
                if (field.type === "select") {
                    if (!field.options || field.options.length === 0) {
                        setError("Select fields must have at least one option.");
                        return;
                    }
                    for (const option of field.options) {
                        if (!option || option.trim() === "") {
                            setError("All options must have a value.");
                            return;
                        }
                    }
                }
                if (!field.value || field.value.trim() === "") {
                    setError("All fields must have a default value.");
                    return;
                }
            }

            const savedBlueprint = await blueprint_post(
                localBlueprint.id,
                localBlueprint.name,
                localBlueprint.description || "",
                localBlueprint.is_public || false,
                localBlueprint.fields
            );

            if(parentWorld && setParentWorld && savedBlueprint) {
                // Update parent world with new blueprint, only if it isn't already included
                if (!parentWorld.blueprints.includes(savedBlueprint)) {
                    setParentWorld({
                        ...parentWorld,
                        blueprints: [...parentWorld.blueprints, savedBlueprint]
                    });
                }
            }

            setIsDirty(false);
            if(speedCreate) {
                fetchBlueprint();
            }
            else {
                setShowEditor(false);
            }
        } catch (err) {
            setError("Failed to save blueprint data: " + String(err));
        } finally {
            refresh?.();
            setLoading(false);
        }
    }

    const handleDelete = async () => {
        if(blueprint_id !== "new") {
            try{
                setLoading(true);
                await blueprint_delete(blueprint_id);
            }
            catch (err){
                setError("Failed to delete blueprint: " + String(err));
            } finally{
                setLoading(false);
            }
            setShowEditor(false);
        }
    };

    useEffect(() => {
        if(showEditor) {
            fetchBlueprint();
            setIsDirty(false);
        }
        else {
            refresh?.();
        }
        setSpeedCreate(false);
    }, [showEditor]);

    const addField = () => {
        if (!localBlueprint) return;

        setError("");
        setIsDirty(true);

        setLocalBlueprint({
            ...localBlueprint,
            fields: [...localBlueprint.fields, { name: "", type: "text", value: "" }]
        });
    }


    const removeField = (index: number) => {
        if (!localBlueprint) return;

        setError("");
        setIsDirty(true);

        setLocalBlueprint({
        ...localBlueprint,
        fields: localBlueprint.fields.filter((_, i) => i !== index)
        });
    }


    const addOptionToField = (index: number, option: string) => {
        if (!localBlueprint) return;

        setError("");
        setIsDirty(true);

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
        setIsDirty(true);

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
            title={blueprint_id === "new" ? "Create Blueprint" : "Edit Blueprint"}
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
                    <span className="w-100 d-flex flex-row align-items-center justify-content-center">
                        <div className="w-25"/>
                        <h1 className="w-50 text-center">{localBlueprint.name || "My Blueprint"}</h1>
                        <div className="w-25">
                            { blueprint_id === "new" && (
                                <ToggleField
                                    value={speedCreate}
                                    setValue={setSpeedCreate}
                                    label="Speed Create"
                                    type="button"
                                />
                            )}
                        </div>
                    </span>
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
                                setValue={(value) => {
                                    setLocalBlueprint({ ...localBlueprint, name: value });
                                    setIsDirty(true);
                                }}
                                placeholder="Blueprint Name"
                                label="Name"
                                required={true}
                                />

                            <LongTextField
                                value={localBlueprint.description || ""}
                                setValue={(value) => {
                                    setLocalBlueprint({ ...localBlueprint, description: value });
                                    setIsDirty(true);
                                }}
                                placeholder="Description"
                                label="Description"
                                required={false}
                                />

                            <ToggleField
                                value={localBlueprint.is_public || false}
                                setValue={(value) => {
                                    setLocalBlueprint({ ...localBlueprint, is_public: value });
                                    setIsDirty(true);
                                }}
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
                                                    setIsDirty(true);
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
                                                    setIsDirty(true);
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
                                                        setIsDirty(true);
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
                                                        setIsDirty(true);
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
                                                        setIsDirty(true);
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
                                                        setIsDirty(true);
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
                                                        setIsDirty(true);
                                                    }}
                                                    label="Default Value"
                                                    required
                                                    options={availableBlueprints?.filter(bp => bp.id !== localBlueprint.id) || []}
                                                    optionValue={(bp) => bp.id}
                                                    optionLabel={(bp) => bp.name}
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
                                                                setIsDirty(true);
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
                    {isDirty && <MessageBox warning="You have unsaved changes." />}
                    <hr />

                    <div className="d-flex flex-row gap-3">
                        {blueprint_id === "new" ? (
                            <ButtonField
                                onClick={() => setShowEditor(false)}
                                color="danger"
                                rounding="3"
                            >
                                Cancel
                            </ButtonField>
                        ) : (
                            <ButtonField
                                onClick={() => setShowDelete(true)}
                                color="danger"
                                rounding="3"
                            >
                                Delete
                            </ButtonField>
                        )}
                        <ButtonField
                            onClick={handleSave}
                            color="primary"
                            loading={loading}
                            rounding="3"
                            disabled={!isDirty}
                        >
                            {blueprint_id === "new" ? "Create Blueprint" : "Save Changes"}
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
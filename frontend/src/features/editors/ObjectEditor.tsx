import { useEffect, useState } from "react";

import { object_get } from "@/apis/library_api";
import type { ObjectResponse, WorldResponse } from "@apis/_schemas";

import ShortTextField from "@/components/fields/ShortTextField";
import LongTextField from "@/components/fields/LongTextField";
import DropdownField from "@/components/fields/DropdownField";

import NumberField from "@/components/fields/NumberField";

import TabGroup from "@/components/TabGroup";

import Loading from "@components/Loading";

import MessageBox from "@/components/MessageBox";
import Modal from "@/components/design/Modal";

type ObjectEditorProps = {
    showEditor: boolean;
    setShowEditor: (show: boolean) => void;
    object?: ObjectResponse;
    setObject?: (object: ObjectResponse) => void;
    parentWorld?: WorldResponse | null;
    setParentWorld?: (world: WorldResponse) => void;
};

export default function ObjectEditor({ showEditor, setShowEditor, object, setObject, parentWorld, setParentWorld }: ObjectEditorProps) {
    const [localObject, setLocalObject] = useState<ObjectResponse | null>(null);

    const [tabNumber, setTabNumber] = useState<number>(0);

    const selectedBlueprintId = localObject?.blueprint?.id || "";

    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>("");

    const handleSave = async () => {
        if (!localObject) return;

        if(loading) return;

        try{
            setLoading(true);
            setError("");
            if(object !== undefined){
                setObject?.(localObject);
            }

            if (parentWorld && setParentWorld && localObject) {
                const existingObjects = parentWorld.objects || [];

                const updatedObjects = existingObjects.some(ctx => ctx.id === localObject.id)
                    ? existingObjects.map(ctx =>
                        ctx.id === localObject.id ? localObject : ctx
                    )
                    : [...existingObjects, localObject];

                setParentWorld({
                    ...parentWorld,
                    objects: updatedObjects,
                });
            }

            setLocalObject(null);
            setShowEditor(false);
        } catch (err) {
            setError("Failed to save object data.");
        } finally {
            setLoading(false);
        }
    }

    const fetchObject = async () => {
        setLoading(true);
        setError("");

        try {
            let obj: ObjectResponse;
            if (object) {
                obj = object;
            } else {
                obj = await object_get("new");
            }
            setLocalObject(obj);
            resetFields();
        } catch (err) {
            setError("Failed to fetch object data.");
        } finally {
            setLoading(false);
        }
    }

    const resetFields = () => {
        if (localObject?.blueprint) {
            setLocalObject({
                ...localObject,
                fields: structuredClone(localObject.blueprint.fields)
            });
        }
    }

    useEffect(() => {
        resetFields();
    }, [localObject?.blueprint]);

    useEffect(() => {
        fetchObject();
    }, [object]);


    return (
        <Modal
            title={object ? "Edit Object" : "Create Object"}
            showModal={showEditor}
            setShowModal={setShowEditor}
            onClose={fetchObject}
            >

            {loading ? (
                <Loading />
            ) : (localObject ? (
                <form className="d-flex flex-column gap-3" onSubmit={handleSave}>
                    <h1 className="text-center">{object?.name || "My Object"}</h1>
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

                            <DropdownField
                                value={selectedBlueprintId}
                                setValue={(id) => {
                                    const selectedBlueprint = parentWorld?.blueprints.find(bp => bp.id === id);
                                    if (selectedBlueprint) {
                                        setLocalObject({ ...localObject, blueprint: selectedBlueprint });
                                    }
                                }}
                                label="Blueprint"
                                required={true}
                                options={parentWorld?.blueprints || []}
                                optionValue={(bp) => bp.id}
                                optionLabel={(bp) => bp.name}
                            />

                            <ShortTextField
                                value={localObject.name}
                                setValue={(value) => setLocalObject({ ...localObject, name: value })}
                                placeholder="Object Name"
                                label="Name"
                                required={true}
                                />

                            <LongTextField
                                value={localObject.description || ""}
                                setValue={(value) => setLocalObject({ ...localObject, description: value })}
                                placeholder="Description"
                                label="Description"
                                required={false}
                                />

                        </div>
                    )}
                    { tabNumber === 1 && (
                        <div className="d-flex flex-column gap-3">
                            <h3 className="text-center">Fields</h3>
                            { /* Field Iterator*/}
                            {localObject.fields.map((field, index) => (
                                <div key={index} className="d-flex flex-column gap-3 w-100">
                                    <div className="d-flex flex-row w-100 align-items-end">
                                        {/* Field Index */}
                                        <div className="col-2 text-center text-light d-flex flex-column p-2 px-4 bg-darkish rounded-pill text-nowrap overflow-hidden me-2">
                                            {field.name ? field.name : `Field ${index}`}
                                        </div>

                                        {/* Field Current Value */}
                                        <div className="w-100 px-1">
                                            {field.type === "text" && (
                                                <ShortTextField
                                                    value={field.value || ""}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localObject.fields];
                                                        updatedFields[index].value = value;
                                                        setLocalObject({ ...localObject, fields: updatedFields });
                                                    }}
                                                    placeholder="Current Value"
                                                    label="Current Value"
                                                    prepend={field.type.charAt(0).toUpperCase() + field.type.slice(1)}
                                                    required
                                                />
                                            )}
                                            {field.type === "number" && (
                                                <NumberField
                                                    value={field.value ? Number(field.value) : 0}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localObject.fields];
                                                        updatedFields[index].value = value.toString();
                                                        setLocalObject({ ...localObject, fields: updatedFields });
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
                                                        const updatedFields = [...localObject.fields];
                                                        updatedFields[index].value = (value === "true" ? "true" : "false");
                                                        setLocalObject({ ...localObject, fields: updatedFields });
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
                                                        const updatedFields = [...localObject.fields];
                                                        updatedFields[index].value = value;
                                                        setLocalObject({ ...localObject, fields: updatedFields });
                                                    }}
                                                    label="Default Value"
                                                    required
                                                    options={field.options || []}
                                                    optionValue={(option) => option}
                                                    optionLabel={(option) => option.charAt(0).toUpperCase() + option.slice(1)}
                                                />
                                            )}
                                            {field.type === "object" && (
                                                <DropdownField
                                                    value={field.value || ""}
                                                    setValue={(value) => {
                                                        const updatedFields = [...localObject.fields];
                                                        updatedFields[index].value = value;
                                                        setLocalObject({ ...localObject, fields: updatedFields });
                                                    }}
                                                    label="Current Value"
                                                    required
                                                    options={parentWorld?.objects.filter(obj => obj.id !== localObject.id) || []}
                                                    optionValue={(object) => object.id}
                                                    optionLabel={(object) => object.name}
                                                />
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {error && <MessageBox error={error} />}
                    <hr />

                    <div className="d-flex flex-row gap-3">
                        <button className="w-100 btn btn-danger" type="button" onClick={() => setShowEditor(false)} disabled={loading}>
                            Cancel
                            {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                        </button>
                        <button className="w-100 btn btn-primary" type="button" onClick={handleSave} disabled={loading}>
                            {object ? "Save Changes" : "Create Object"}
                            {loading && <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>}
                        </button>
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
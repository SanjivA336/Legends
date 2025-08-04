import React, { use, useEffect, useState } from "react";

import { context_delete, context_get } from "@/apis/library_api";
import type { ContextResponse, WorldResponse } from "@apis/_schemas";

import ShortTextField from "@/components/fields/ShortTextField";
import LongTextField from "@/components/fields/LongTextField";

import Loading from "@components/Loading";

import MessageBox from "@/components/MessageBox";
import Modal from "@/components/design/Modal";
import DeletePopup from "@/components/DeletePopup";
import ButtonField from "@/components/fields/ButtonField";

type ContextEditorProps = {
    showEditor: boolean;
    setShowEditor: (show: boolean) => void;
    context?: ContextResponse;
    setContext?: (context: ContextResponse) => void;
    parentWorld?: WorldResponse | null;
    setParentWorld?: (world: WorldResponse) => void;
};

export default function ContextEditor({ showEditor, setShowEditor, context, setContext, parentWorld, setParentWorld }: ContextEditorProps) {
    const [localContext, setLocalContext] = useState<ContextResponse | null>(null);

    const [showDelete, setShowDelete] = useState<boolean>(false);

    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>("");

    const fetchContext = async () => {
        setLoading(true);
        setError("");

        try{
            if (context) {
                setLocalContext(context);
            } else {
                const data: ContextResponse = await context_get("new")
                setLocalContext(data);
            }
        } catch (err) {
                setError("Failed to fetch context data.");
        } finally {
            setLoading(false);
        }
    }

    const handleSave = async () => {
        if (!localContext) return;

        if(loading) return;

        try{
            setLoading(true);
            setError("");
            if(context !== undefined){
                setContext?.(localContext);
            }

            if (parentWorld && setParentWorld && localContext) {
                const existingContexts = parentWorld.contexts || [];

                const updatedContexts = existingContexts.some(ctx => ctx.id === localContext.id)
                    ? existingContexts.map(ctx =>
                        ctx.id === localContext.id ? localContext : ctx
                    )
                    : [...existingContexts, localContext];

                setParentWorld({
                    ...parentWorld,
                    contexts: updatedContexts,
                });
            }

            setLocalContext(null);
            setShowEditor(false);
        } catch (err) {
            setError("Failed to save context data.");
        } finally {
            setLoading(false);
        }
    }

    const handleDelete = async () => {
        if(context){
            try{
                setLoading(true);
                await context_delete(context.id);
            }
            catch (err){
                setError(String(err));
            } finally{
                try{
                    //remove from parentWorld
                    if (parentWorld && setParentWorld) {
                        const updatedContexts = (parentWorld.contexts || []).filter(ctx => ctx.id !== context.id);
                        setParentWorld({
                            ...parentWorld,
                            contexts: updatedContexts,
                        });
                    }
                }
                catch (err) {
                    setError(String(err))
                }
                finally{
                    setLoading(false);
                    setShowEditor(false);
                }
            }
        }
    }

    useEffect(() => {
        fetchContext();
    }, [context]);


    return (
        <Modal
            title={context ? "Edit Context" : "Create Context"}
            showModal={showEditor}
            setShowModal={setShowEditor}
            onClose={fetchContext}
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
            ) : (localContext ? (
                <form className="d-flex flex-column gap-3" onSubmit={handleSave}>
                    <h1 className="text-center">{context?.name || "My Context"}</h1>

                    <div className="d-flex flex-column gap-3">
                        <h3 className="text-center">General</h3>
                        <ShortTextField
                            value={localContext.name}
                            setValue={(value) => setLocalContext({ ...localContext, name: value })}
                            placeholder="Context Name"
                            label="Name"
                            required={true}
                            />

                        <LongTextField
                            value={localContext.content || ""}
                            setValue={(value) => setLocalContext({ ...localContext, content: value })}
                            placeholder="Content"
                            label="Content"
                            required={false}
                            />
                    </div>

                    {error && <MessageBox error={error} />}
                    <hr />

                    <div className="d-flex flex-row gap-3">
                        {context ? (
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
                            {context ? "Save Changes" : "Create Context"}
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
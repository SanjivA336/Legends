import { GET_ENDPOINT, POST_ENDPOINT } from "./_api_core";
import type { WorldPayload, WorldResponse, BlueprintPayload, BlueprintResponse, CustomField, ContextPayload, ContextResponse, ObjectPayload, ObjectResponse} from "./_schemas";

// === World Endpoints ===
export async function worlds_all_get(): Promise<WorldResponse[]> {
    return GET_ENDPOINT<WorldResponse[]>(`/worlds`);
}

export async function world_get(id: string): Promise<WorldResponse> {
    return GET_ENDPOINT<WorldResponse>(`/world/${id}`);
}

export async function world_post(id: string, name: string, description?: string, is_public?: boolean, blueprint_ids?: string[], context_ids?: string[], object_ids?: string[]): Promise<WorldResponse> {
    const payload: WorldPayload = {
        id: id,
        name: name,
        description: description,
        settings: { is_public: is_public ?? false },
        blueprint_ids: blueprint_ids,
        context_ids: context_ids,
        object_ids: object_ids
    };
    return POST_ENDPOINT<WorldPayload, WorldResponse>(`/world/${id}`, payload);
}

export async function blueprints_all_get(): Promise<BlueprintResponse[]> {
    return GET_ENDPOINT<BlueprintResponse[]>(`/blueprints`);
}

export async function blueprint_get(id: string): Promise<BlueprintResponse> {
    return GET_ENDPOINT<BlueprintResponse>(`/blueprint/${id}`);
}

export async function blueprint_post(id: string, name: string, description?: string, fields?: CustomField[]): Promise<BlueprintResponse> {
    const payload: BlueprintPayload = {
        id: id,
        name: name,
        description: description,
        fields: fields,
    };
    return POST_ENDPOINT<BlueprintPayload, BlueprintResponse>(`/blueprint/${id}`, payload);
}

export async function blueprint_delete(id: string): Promise<void> {
    return GET_ENDPOINT<void>(`/blueprint/${id}/delete`);
}

export async function context_get(id: string): Promise<ContextResponse> {
    return GET_ENDPOINT<ContextResponse>(`/context/${id}`);
}

export async function context_post(id: string, name: string, content: string): Promise<ContextResponse> {
    const payload: ContextPayload = {
        id: id,
        name: name,
        content: content,
    };
    return POST_ENDPOINT<ContextPayload, ContextResponse>(`/context/${id}`, payload);
}

export async function context_delete(id: string): Promise<void> {
    return GET_ENDPOINT<void>(`/context/${id}/delete`);
}

export async function object_get(id: string): Promise<ObjectResponse> {
    return GET_ENDPOINT<ObjectResponse>(`/object/${id}`);
}

export async function object_post(id: string, name: string, description?: string, fields?: CustomField[], blueprint_id?: string): Promise<ObjectResponse> {
    const payload: ObjectPayload = {
        id: id,
        name: name,
        description: description,
        fields: fields,
        blueprint_id: blueprint_id,
    };
    return POST_ENDPOINT<ObjectPayload, ObjectResponse>(`/object/${id}`, payload);
}
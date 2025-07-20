import { GET_ENDPOINT, POST_ENDPOINT } from "./_api_core";
import type { WorldPayload, WorldResponse } from "./_schemas";


// === Endpoints ===
export async function world_get(id: string) {
    return GET_ENDPOINT<WorldResponse>(`/world/${id}`);
}

export async function world_post(id: string, name: string, description?: string, is_public?: boolean, context?: Record<string, any>, settings?: Record<string, any>) {
    return POST_ENDPOINT<WorldPayload, WorldResponse>(`/world/${id}`, {
        name,
        description,
        is_public,
        context,
        settings
    });
}

export async function worlds_all_get() {
    return GET_ENDPOINT<WorldResponse[]>(`/worlds`);
}
    
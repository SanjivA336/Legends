import { GET_ENDPOINT, POST_ENDPOINT } from "./_api_core";
import type { WorldPayload, WorldResponse, CampaignPayload, CampaignResponse } from "./_schemas";


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

export async function campaign_get(id: string) {
    return GET_ENDPOINT<CampaignResponse>(`/campaign/${id}`);
}

export async function campaign_post(id: string, name: string, description?: string, world_id?: string, is_public?: boolean, context?: Record<string, any>, settings?: Record<string, any>) {
    return POST_ENDPOINT<CampaignPayload, CampaignResponse>(`/campaign/${id}`, {
        name,
        description,
        world_id,
        is_public,
        context,
        settings
    });
}

export async function campaigns_all_get() {
    return GET_ENDPOINT<CampaignResponse[]>(`/campaigns`);
}
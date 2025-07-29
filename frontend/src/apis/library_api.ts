import { GET_ENDPOINT, POST_ENDPOINT } from "./_api_core";
import type { WorldPayload, WorldResponse, CampaignPayload, CampaignResponse} from "./_schemas";

// === World Endpoints ===
export async function world_get(id: string) {
    return GET_ENDPOINT<WorldResponse>(`/world/${id}`);
}

export async function world_post(id: string, name: string, description?: string, is_public?: boolean) {
    const payload: WorldPayload = {
        id: id,
        name: name,
        description: description,
        settings: { is_public: is_public ?? false },
    };
    return POST_ENDPOINT<WorldPayload, WorldResponse>(`/world`, payload);
}

export async function worlds_all_get() {
    return GET_ENDPOINT<WorldResponse[]>(`/worlds`);
}

// === Campaign Endpoints ===
export async function campaign_get(id: string) {
    return GET_ENDPOINT<CampaignResponse>(`/campaign/${id}`);
}

export async function campaign_post(id: string, name: string, description?: string, world?: WorldPayload, is_public?: boolean) {
    const payload: CampaignPayload = {
        id: id,
        name: name,
        description: description,
        world: world,
        settings: { is_public: is_public ?? false },
    };
    return POST_ENDPOINT<CampaignPayload, CampaignResponse>(`/campaign`, payload);
}

export async function campaigns_all_get() {
    return GET_ENDPOINT<CampaignResponse[]>(`/campaigns`);
}
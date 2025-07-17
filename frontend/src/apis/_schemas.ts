// Payload: Client (frontend) to Server (backend)
// Response: Server (backend) to Client (frontend)

// === User Schemas ===
export interface UserPayload {
    username?: string;
    email?: string;
    password?: string;
    password_new?: string;
}

export interface UserResponse {
    id: string;
    username?: string;
    email?: string;
}

// === Campaign Schemas ===
export interface CampaignCard {
    id: string;
    name: string;
    description?: string;
    is_public: boolean;
}

// === Page Schemas ===
export interface HomePage {
    user: UserResponse;
    campaigns: CampaignCard[];
}

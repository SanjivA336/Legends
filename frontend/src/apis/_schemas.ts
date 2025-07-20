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

// === World Schemas ===
export interface WorldPayload {
    name: string;
    description?: string;
    is_public?: boolean;
    context?: Record<string, any>;
    settings?: Record<string, any>;
}

export interface WorldResponse {
    id: string;
    name: string;
    description?: string;
    creator: UserResponse;
    is_public: boolean;
    context: Record<string, any>;
    settings: Record<string, any>;
}

// === Campaign Schemas ===
export interface CampaignPayload {
    name: string;
    description?: string;
    is_public?: boolean;
    context?: Record<string, any>;
    settings?: Record<string, any>;
}

export interface CampaignResponse {
    id: string;
    world?: WorldResponse | null;
    name: string;
    description?: string;
    creator: UserResponse;
    is_public: boolean;
    context: Record<string, any>;
    settings: Record<string, any>;
    members: Record<string, string>;
    turn_queue: string[];
    eras: string[];
}

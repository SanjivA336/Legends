import { GET_ENDPOINT, POST_ENDPOINT } from "./_api_core";
import type { UserPayload, UserResponse } from "./_schemas";

// === Endpoints ===
export async function account_get() {
    return GET_ENDPOINT<UserResponse>('/account');
}

export async function profile_update(username: string) {
    const payload: UserPayload = { 
        username: username
    };
    return POST_ENDPOINT<UserPayload, null>('/account/profile', payload);
}

export async function security_update(email: string, password_current: string, password_new: string) {
    const payload: UserPayload = { 
        email: email, 
        password_current: password_current, 
        password_new: password_new 
    };
    return POST_ENDPOINT<UserPayload, null>('/account', payload);
}
import { GET_ENDPOINT, POST_ENDPOINT } from "./_api_core";
import type { UserResponse, UserPayload } from "./_schemas";

// === Endpoints ===
export async function account_get() {
    return GET_ENDPOINT<UserResponse>('/profile');
}

export async function profile_update(username: string) {
    return POST_ENDPOINT<UserPayload>('/profile', {
        username
    });
}

export async function security_update(email: string, password: string, password_new?: string) {
    return POST_ENDPOINT<UserPayload>('/profile', {
        email,
        password,
        password_new
    });
}

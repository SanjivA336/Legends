import { POST_ENDPOINT } from "./_api_core";
import type { UserPayload } from "./_schemas";


// === Endpoints ===
export async function login(email: string, password: string) {
    return POST_ENDPOINT<UserPayload, null>('/login', {
        email,
        password,
    });
}

export async function register(username: string, email: string, password: string) {
    return POST_ENDPOINT<UserPayload, null>('/register', {
        username,
        email,
        password,
    });
}

export async function authenticate() {
    return POST_ENDPOINT('/authenticate', {});
}

export async function refresh() {
    return POST_ENDPOINT('/refresh', {});
}

export async function logout() {
    return POST_ENDPOINT('/logout', {});
}
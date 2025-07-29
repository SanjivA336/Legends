import { POST_ENDPOINT } from "./_api_core";
import type { UserPayload } from "./_schemas";


// === Endpoints ===
export async function login(email: string, password_current: string) {
    const payload: UserPayload = { 
        email: email, 
        password_current: password_current
    };
    return POST_ENDPOINT<UserPayload, null>('/login', payload);
}

export async function register(username: string, email: string, password_current: string) {
    const payload: UserPayload = {
        username: username,
        email: email,
        password_current: password_current,
    };
    return POST_ENDPOINT<UserPayload, null>('/register', payload);
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
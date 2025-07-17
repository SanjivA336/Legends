import { GET_ENDPOINT} from "./_api_core";
import type { HomePage } from "./_schemas";

// === Endpoints ===
export async function home_get() {
    return GET_ENDPOINT<HomePage>('/home');
}


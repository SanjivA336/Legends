import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
    plugins: [
        react(),
        tsconfigPaths() // 🔁 Automatically reads from `tsconfig.json` or `tsconfig.app.json`
    ]
});

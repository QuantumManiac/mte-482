/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */
await import("./src/env.js");

/** @type {import("next").NextConfig} */
const config = {
    images: {
        remotePatterns: [{
            hostname: "192.168.0.114" 
        },
        {
            hostname: "localhost"
        },
        {
            hostname: "192.168.137.10"
        }
        ],
    }
};

export default config;

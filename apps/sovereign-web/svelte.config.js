import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			fallback: 'index.html' // may differ based on your framework
		}),
		alias: {
			"@age-protocol/types": "../../packages/age-types/src/index",
			"@age-protocol/agents-sdk": "../../packages/age-agents-sdk/src/index",
			"@age-protocol/equational": "../../packages/age-equational/src/index",
			"@age-protocol/forensics": "../../packages/age-forensics/src/index",
			"@age-protocol/navy": "../../packages/age-navy/src/index"
		}
	}
};

export default config;

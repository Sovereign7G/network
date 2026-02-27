import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
	plugins: [sveltekit()],
	resolve: {
		alias: {
			$lib: path.resolve('./src/lib'),
			$stores: path.resolve('./src/lib/stores'),
			'@age-protocol/types': path.resolve('../../packages/age-types'),
			'@age-protocol/sensory': path.resolve('../../packages/age-sensory/src/index'),
			'@age-protocol/forensics': path.resolve('../../packages/age-forensics/src/index'),
			'@age-protocol/equational': path.resolve('../../packages/age-equational/src/index'),
			'@age-protocol/atlas': path.resolve('../../packages/age-atlas'),
			'@age-protocol/vault': path.resolve('../../packages/age-vault'),
			'@age-protocol/api-client': path.resolve('../../packages/age-api-client'),
			'@age-protocol/store': path.resolve('./src/lib/stores/master-store'),
			'@age-protocol/ui': path.resolve('./src/lib/components/ui'),
			'@age-protocol/agents-sdk': path.resolve('../../packages/age-agents-sdk/src/index'),
		}
	},
	worker: {
		format: 'es'
	},
	server: {
		proxy: {
			'/api': {
				target: 'http://localhost:3000',
				changeOrigin: true
			},
			'/socket': {
				target: 'http://localhost:3000',
				ws: true
			}
		}
	},
	build: {
		chunkSizeWarningLimit: 300,
		rollupOptions: {
			output: {
				manualChunks: (id) => {
					if (id.includes('node_modules')) {
						if (id.includes('three')) return 'vendor-three';
						if (id.includes('d3')) return 'vendor-d3';
						return 'vendor';
					}
					if (id.includes('src/lib/stores/master-store')) return 'master-store';
					if (id.includes('src/lib/engine')) return 'fastcode-engine';
				}
			}
		}
	}
});

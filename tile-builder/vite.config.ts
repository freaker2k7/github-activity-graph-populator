import { defineConfig } from 'vite';
import { ViteMinifyPlugin } from 'vite-plugin-minify';
import { viteSingleFile } from 'vite-plugin-singlefile';

const isProd = process.env.NODE_ENV === 'production' && !process.env.DEV;

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [viteSingleFile(), ViteMinifyPlugin()],
	define: {
		global: 'globalThis',
	},
	resolve: {
		alias: {
			'readable-stream': 'vite-compatible-readable-stream',
		},
	},
	build: {
		sourcemap: !isProd,
		minify: 'terser',
		terserOptions: {
			compress: {
				drop_console: isProd,
				drop_debugger: isProd,
			},
		},
	},
});

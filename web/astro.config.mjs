import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  site: 'https://mass-gap.github.io',
  base: '/UIDT-Framework-v3.9-Canonical',
  output: 'static',
  integrations: [react()],
  build: {
    assets: 'assets'
  }
});
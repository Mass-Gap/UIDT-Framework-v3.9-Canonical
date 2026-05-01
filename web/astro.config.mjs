import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://mass-gap.github.io',
  base: '/UIDT-Framework-v3.9-Canonical',
  output: 'static',
  build: {
    assets: 'assets'
  }
});
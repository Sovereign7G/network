#!/usr/bin/env bun
/**
 * 🏛️ AGE REPUBLIC :: AXON CLI
 * Programmatic sovereign link from the command line.
 */

import { AxonEngine, defineConfig } from "./axon.ts";
import { zettoVersion, zettoSeal } from "./zetto_bridge.ts";
import { resolve } from "path";
import { writeFileSync, mkdirSync, existsSync } from "fs";

const args = process.argv.slice(2);
const root = args[0] || resolve(import.meta.dir, "../../..");
const outDir = resolve(root, "04_SUBSTRATES/sovereign_trinity/out");

console.log("🏛️ ═══════════════════════════════════════════");
console.log("   AXON SOVEREIGN LINKER CLI");
console.log(`   Zetto ${zettoVersion()} | Bun ${Bun.version}`);
console.log("═══════════════════════════════════════════════\n");

const config = defineConfig({
  root,
  entries: ["index", "main", "app"],
  trustBoundaries: {
    "axon_teles": "axon::teles",
    "axon_vision": "axon::vision",
    "02_CORE": "sovereign::core",
    "03_LOGIC": "sovereign::logic",
  },
});

const engine = new AxonEngine(config);
await engine.scanModules();
const result = await engine.link();

// Write sealed chunks to disk
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });

for (const chunk of result.chunks) {
  const path = resolve(outDir, `${chunk.id}.sealed.js`);
  writeFileSync(path, chunk.code);
  console.log(`   💾 Written: ${path}`);
}

// Write manifest
const manifestPath = resolve(outDir, "link_manifest.json");
writeFileSync(manifestPath, JSON.stringify(result, null, 2));
console.log(`   📋 Manifest: ${manifestPath}`);
console.log(`\n✅ ${result.total_chunks} sealed chunks written to ${outDir}`);

/**
 * 🏛️ AGE REPUBLIC :: AXON SOVEREIGN ORCHESTRATOR
 * Analog: Vite in the Voidzero Trinity.
 */

import { resolve, dirname, basename, extname } from "path";
import { readFileSync, readdirSync, statSync, existsSync } from "fs";
import {
  zettoInit, zettoAddModule, zettoLink, zettoVersion,
  type SovereignModule, type LinkResult, type SealedChunk,
} from "./zetto_bridge.ts";

export interface AxonConfig {
  root: string;
  entries: string[];
  trustBoundaries?: Record<string, string>;
  treeShake?: boolean;
  fullBundleDev?: boolean;
  plugins?: AxonPlugin[];
}

export interface AxonPlugin {
  name: string;
  buildStart?: () => void | Promise<void>;
  transform?: (code: string, id: string) => string | Promise<string>;
  renderChunk?: (chunk: SealedChunk) => SealedChunk | Promise<SealedChunk>;
  buildEnd?: (result: LinkResult) => void | Promise<void>;
}

function extractImports(source: string): string[] {
  const imports: string[] = [];
  const re = /import\s+.*?\s+from\s+['"]([^'"]+)['"]/g;
  let m;
  while ((m = re.exec(source)) !== null) imports.push(m[1]);
  return imports;
}

function extractExports(source: string): string[] {
  const exports: string[] = [];
  const re = /export\s+(?:function|const|let|var|class)\s+(\w+)/g;
  let m;
  while ((m = re.exec(source)) !== null) exports.push(m[1]);
  if (/export\s+default/.test(source)) exports.push("default");
  return exports;
}

function resolveTrustBoundary(path: string, map?: Record<string, string>): string {
  if (map) {
    for (const [pat, boundary] of Object.entries(map)) {
      if (path.includes(pat)) return boundary;
    }
  }
  const parts = dirname(path).split("/").filter(Boolean);
  return parts.slice(-2).join("::") || "sovereign::core";
}

export class AxonEngine {
  private config: AxonConfig;
  private modules: Map<string, SovereignModule> = new Map();

  constructor(config: AxonConfig) {
    this.config = { treeShake: true, fullBundleDev: false, ...config };
  }

  async scanModules(): Promise<void> {
    console.log(`\n🔍 [Axon] Scanning modules from: ${this.config.root}`);
    if (!existsSync(this.config.root)) throw new Error(`Root not found: ${this.config.root}`);
    const files = this.walkDir(this.config.root);
    const exts = [".ts", ".js", ".mjs", ".mojo", ".py"];

    for (const file of files) {
      if (!exts.includes(extname(file))) continue;
      let source = readFileSync(file, "utf-8");
      const id = basename(file, extname(file));
      const isEntry = this.config.entries.includes(id);

      for (const p of this.config.plugins || []) {
        if (p.transform) source = await p.transform(source, id);
      }

      this.modules.set(id, {
        id, path: file, source,
        imports: extractImports(source),
        exports: extractExports(source),
        trust_boundary: resolveTrustBoundary(file, this.config.trustBoundaries),
        is_entry: isEntry,
      });
    }
    console.log(`   📦 Discovered ${this.modules.size} sovereign modules`);
  }

  addModule(module: SovereignModule): void {
    this.modules.set(module.id, module);
  }

  async link(): Promise<LinkResult> {
    const t0 = performance.now();
    for (const p of this.config.plugins || []) { if (p.buildStart) await p.buildStart(); }

    console.log(`\n⚡ [Axon] Sovereign Trinity link pipeline...`);
    console.log(`   Zetto version: ${zettoVersion()}`);

    zettoInit();
    let n = 0;
    for (const [, mod] of this.modules) {
      if (zettoAddModule(mod)) n++;
    }
    console.log(`   📤 Pushed ${n} modules to Zetto`);

    const t1 = performance.now();
    const result = zettoLink();
    console.log(`\n🔗 [Zetto] Link: ${(performance.now() - t1).toFixed(2)}ms (${result.link_time_us}µs native)`);
    console.log(`   📊 ${result.total_modules} modules, ${result.dead_modules_eliminated} shaken`);
    console.log(`   📦 ${result.total_chunks} chunks, ${result.module_graph_edges} edges`);

    for (let i = 0; i < result.chunks.length; i++) {
      for (const p of this.config.plugins || []) {
        if (p.renderChunk) result.chunks[i] = await p.renderChunk(result.chunks[i]);
      }
    }

    console.log(`\n✅ [Axon] Pipeline complete in ${(performance.now() - t0).toFixed(2)}ms`);
    for (const c of result.chunks) {
      console.log(`   🧱 ${c.id} | ${c.modules.length} mods | ${(c.size_bytes/1024).toFixed(1)}KB | ${c.keccak_seal.slice(0,18)}...`);
    }

    for (const p of this.config.plugins || []) { if (p.buildEnd) await p.buildEnd(result); }
    return result;
  }

  private walkDir(dir: string): string[] {
    const results: string[] = [];
    try {
      for (const e of readdirSync(dir)) {
        if (e.startsWith(".") || e === "node_modules" || e === "target") continue;
        const full = resolve(dir, e);
        try {
          const s = statSync(full);
          if (s.isDirectory()) results.push(...this.walkDir(full));
          else results.push(full);
        } catch { /* skip */ }
      }
    } catch { /* skip */ }
    return results;
  }
}

export function defineConfig(config: AxonConfig): AxonConfig { return config; }

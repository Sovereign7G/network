// Sovereign 7G TypeScript SDK v2 — browser, Node, and React Native.
// Covers: calls, messaging, nodes, beamforming, analytics, identity,
//         LoRA IoT, ICP mesh, cross-chain, AI spec KB, Virtual DSA.

const API_BASE = process.env.S7G_API || 'https://api.7g.network';

export interface CallOptions { to: string; type?: 'voice'|'video'; quality?: 'hd'|'standard'|'low'; payment?: { method: string; currency: string }; }
export interface MessageOptions { to: string; text: string; priority?: 'normal'|'high'|'urgent'; }
export interface BeamOptions { source: { lat: number; lon: number }; target: { lat: number; lon: number }; nodes?: string[]; }
export interface QualityMetrics { mos: number; packetLoss: number; latency: number; jitter: number; }

type EventHandler = (...args: any[]) => void;

export class S7GCall {
  sessionId: string; status: string = 'initiating'; duration: number = 0;
  quality: QualityMetrics = { mos: 0, packetLoss: 0, latency: 0, jitter: 0 };
  private handlers: Map<string, EventHandler[]> = new Map();
  private client: S7GClient;
  constructor(sessionId: string, client: S7GClient) { this.sessionId = sessionId; this.client = client; }
  on(event: string, handler: EventHandler): this { if(!this.handlers.has(event)) this.handlers.set(event,[]); this.handlers.get(event)!.push(handler); return this; }
  emit(event: string, ...args: any[]) { this.handlers.get(event)?.forEach(h => h(...args)); }
  async hangup(): Promise<void> { await this.client.request('POST','/api/call/hangup',{session_id:this.sessionId}); this.status='ended'; this.emit('ended',this.duration); }
}

export class S7GClient {
  identity: string; network: string; private base: string;
  constructor(opts: { identity?: string; network?: string } = {}) { this.identity = opts.identity||''; this.network = opts.network||'base'; this.base = API_BASE; }

  async request(method: string, path: string, body?: any): Promise<any> {
    const res = await fetch(`${this.base}${path}`, { method,
      headers: { 'Content-Type':'application/json','X-Identity':this.identity },
      body: body ? JSON.stringify(body) : undefined });
    return res.json();
  }

  // ── Core ──────────────────────────────────────────────────────
  async call(opts: CallOptions): Promise<S7GCall> {
    const r = await this.request('POST','/api/call/initiate',{ caller:this.identity,callee:opts.to,
      type:opts.type||'voice',quality:opts.quality||'hd',payment:opts.payment||{method:'x402',currency:'USD'} });
    const c = new S7GCall(r.session_id||'',this); c.status='connected'; c.emit('connected'); return c;
  }
  async message(opts: MessageOptions): Promise<any> { return this.request('POST','/api/message/send',{ from:this.identity,to:opts.to,text:opts.text,priority:opts.priority||'normal' }); }
  async nodeRegister(lat: number, lon: number, stake: number = 1000): Promise<any> { return this.request('POST','/api/node/register',{ identity:this.identity,lat,lon,stake }); }
  async nodeStatus(nodeId: string): Promise<any> { return this.request('GET',`/api/node/status?node_id=${nodeId}`); }
  async beamCompute(opts: BeamOptions): Promise<any> { return this.request('POST','/api/beam/calculate',{source:opts.source,target:opts.target,nodes:opts.nodes}); }
  async analyticsHealth(metric: string = 'avg_mos', region: string = 'global'): Promise<any> { return this.request('GET',`/api/analytics/health?metric=${metric}&region=${region}`); }
  async analyticsRisk(): Promise<any> { return this.request('GET','/api/analytics/risk'); }
  async identityResolve(name: string): Promise<any> { return this.request('GET',`/api/identity/resolve?name=${name}`); }

  // ── LoRA IoT ──────────────────────────────────────────────────
  async loraRegister(devEui: string, location?: string): Promise<any> { return this.request('POST','/api/lora/register',{ devEui,location,identity:this.identity }); }
  async loraTelemetry(devEui: string): Promise<any> { return this.request('GET',`/api/lora/telemetry?deveui=${devEui}`); }

  // ── Virtual DSA ───────────────────────────────────────────────
  async dsaObserve(target: string, freqHz: number, bandwidth: number, nodes?: string[]): Promise<any> { return this.request('POST','/api/dsa/observe',{target,freq_hz:freqHz,bandwidth,nodes:nodes||[],duration_s:30}); }
  async dsaFRB(minutes: number = 60): Promise<any> { return this.request('GET',`/api/dsa/frb?minutes=${minutes}`); }
  async dsaRFI(nodeId?: string): Promise<any> { return this.request('GET',`/api/dsa/rfi${nodeId?`?node_id=${nodeId}`:''}`); }

  // ── AI / Spec ─────────────────────────────────────────────────
  async specContext(specId: string, clause?: string): Promise<any> { return this.request('GET',`/api/spec/context?spec=${specId}&clause=${clause||''}`); }
  async specForComponent(component: string): Promise<any> { return this.request('GET',`/api/spec/component?name=${component}`); }

  // ── Contracts & Canisters ─────────────────────────────────────
  readonly CONTRACTS = Object.freeze({
    s7g: '0x54951D5021a2774567412fB8DB6FDF4A1EaE2611',
    license: '0x45bD704f371bc593f38Bd76D43D356A14Febe477',
    staking: '0xEfc2803E088e287b4013abB37358e3cf760A4747',
    session: '0x6afd8D26dF226980a932439948DEefBd33301bf6',
    registry: '0x2606fEbB30deE751DfFbCa538df20Eed5E379410',
    roaming: '0x367d9481CfF6e7E18fAE5b11aA524dbbE139f443',
    dao: '0xC5aF1EE3d5812a7255C27ff11579Fe49E7454588',
  });

  readonly CANISTERS = Object.freeze({
    moveVm: 'gqshy-7qaaa-aaaaa-qhjua-cai',
    aetherdb: 'h54dw-qyaaa-aaaaa-qhjtq-cai',
    swarm: 'oyipx-nyaaa-aaaab-qhbja-cai',
  });

  readonly DSA_BANDS = Object.freeze({
    l_band: [1.2e9, 1.7e9], s_band: [2.3e9, 3.0e9],
    c_band: [4.8e9, 5.5e9], x_band: [8.0e9, 8.8e9],
    ku_band: [12.0e9, 12.75e9],
  });
}

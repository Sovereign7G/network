import type { BridgeQuote } from '$lib/types/blockchain';

export class BridgeStore {
    state = $state({
        error: null as string | null,
        isBridging: false,
        connectedChains: [] as string[]
    });

    connectChain(chain: string) {
        if (!this.state.connectedChains.includes(chain)) {
            this.state.connectedChains.push(chain);
        }
    }

    disconnectChain(chain: string) {
        this.state.connectedChains = this.state.connectedChains.filter(c => c !== chain);
    }

    async getQuote(fromChain: string, toChain: string, asset: string, amount: number): Promise<BridgeQuote | null> {
        this.state.error = null;
        try {
            // Mock quote
            return {
                fromChain,
                toChain,
                asset,
                amount,
                fee: amount * 0.01,
                estimatedTime: 2 // 2 minutes
            };
        } catch (e: any) {
            this.state.error = e.message;
            return null;
        }
    }

    async executeBridge(_quote: BridgeQuote, _fromAddress: string, _toAddress: string) {
        this.state.isBridging = true;
        this.state.error = null;
        try {
            // Mock execution delay
            await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (e: any) {
            this.state.error = e.message;
        } finally {
            this.state.isBridging = false;
        }
    }
}

export const bridgeStore = new BridgeStore();

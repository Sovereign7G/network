# 🏛️ AGE REPUBLIC: SOVEREIGN SUPPLIER ONBOARDING GUIDE (ERA 216.0)
## Low-Latency, Zero-Friction Web3 Stablecoin Payments on Base L2

Welcome to the **AGE REPUBLIC** sovereign procurement network. This guide outlines the simple, low-cost steps for suppliers and vendors to configure decentralized wallets, accept stablecoin payments on **Base L2**, and integrate with our automated on-chain clearing house.

---

## 🗺️ Why Base L2 Stablecoins (USDC / USDT)?

Traditional wire transfers and commercial cards carry high merchant fees, slow settlement times, and unnecessary banking gatekeepers. By settling CapEx invoices on-chain using Base L2, both parties enjoy:
*   **Sub-Cent Fees**: Transaction gas costs are typically less than $0.01 per payment.
*   **Instant Finality**: Payments clear and settle in under 2 seconds, with full cryptographic proof.
*   **Direct Settlement**: Funds settle directly into your custody without intermediary holds.

---

## 🛠️ Step 1: Supplier Wallet Setup

To receive payments, you need a standard Ethereum Virtual Machine (EVM) compatible wallet. We officially support and recommend:
1.  **Brave Wallet** (Native sovereign privacy wallet)
2.  **MetaMask** (Industry standard)
3.  **Coinbase Wallet** (Optimal mobile interface)

### Base Network Configuration:
If your wallet does not automatically support Base L2, add the network manually with the following parameters:
*   **Network Name**: Base
*   **RPC URL**: `https://mainnet.base.org`
*   **Chain ID**: `8453`
*   **Currency Symbol**: ETH
*   **Block Explorer**: `https://basescan.org`

---

## 🪙 Step 2: Adding Stablecoins to Your Wallet

Stablecoins on Base L2 use standard ERC20 contract addresses. Ensure your wallet is configured to display these assets:

| Token | Contract Address (Base L2 Checksum) | Decimals |
| :--- | :--- | :---: |
| **USDC** | `0x833589fCD6eDb35d2614DE169306772617EE011D` | 6 |
| **USDT** | `0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2` | 6 |

---

## 🚀 Step 3: Executing Payments via `execute_transfer.py`

Once the supplier EVM address is registered, the AGE REPUBLIC swarm automates payments using the secure Web3 ERC20 stablecoin bridge.

### 1. Testnet Verification (Base Sepolia)
Before executing high-value mainnet transactions, we verify connectivity on the Base Sepolia Testnet.

```bash
# Execute testnet USDC transfer
python3 06_INFRA/execute_transfer.py \
  --recipient "0xYOUR_SUPPLIER_WALLET_ADDRESS" \
  --amount 10.0 \
  --token "0x036CbD53842c5426634e7929541eC2318f3dCF7e" \
  --rpc "https://sepolia.base.org"
```
*(Testnet USDC Address: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`)*

### 2. Live Mainnet CapEx Settlement (Base L2)
To settle a live procurement invoice (e.g. buying a GPU node):

```bash
# Execute live USDC transfer of $4,850.00
python3 06_INFRA/execute_transfer.py \
  --recipient "0xYOUR_SUPPLIER_WALLET_ADDRESS" \
  --amount 4850.00 \
  --token "USDC"
```

---

## 📊 Step 4: Swarm Invoice Reconciliation

After a transaction is successfully mined into block finality, the on-chain receipt replaces the pending mock parameters in your database to ensure clean, immutable book-keeping.

### Automated Reconciliation Loop:
Our script captures the transaction details and performs an automated check:
```python
# The swarm matches block metadata and writes permanent proof of payment:
{
    "status": "MINED",
    "tx_hash": "0x8fa3bc9d2b7c4e8f71b16fbe82e269152b7c4e8f71b16fbe82e269152b7c4e8f",
    "network": "Base L2 Mainnet",
    "token_contract": "0x833589fCD6eDb35d2614DE169306772617EE011D",
    "sender": "0x3b784f71b16fbe82e269152b7c4e8f71b16fbe82",
    "recipient": "0xYOUR_SUPPLIER_WALLET_ADDRESS",
    "amount_token": 4850.00,
    "timestamp": "2026-05-25T22:53:40Z",
    "verdict": "RECONCILED"
}
```

---

## 🏛️ Continuous Economic Sovereignty
By utilizing on-chain settlement networks, the AGE REPUBLIC ensures that creative workflows, rendering compute, and hardware procurement exist outside central bank friction, maintaining full resource sovereign control.

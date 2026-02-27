export type OrderSide = 'BUY' | 'SELL';
export type OrderType = 'limit' | 'market' | 'stop' | 'stop_limit';

export interface Order {
    id: string;
    side: OrderSide;
    type: OrderType;
    price: number;
    quantity: number;
    filled: number;
    status: 'open' | 'filled' | 'cancelled' | 'expired';
    timestamp: number;
    expiry?: number;
}

export interface OrderBook {
    bids: Order[];
    asks: Order[];
    spread: number;
    lastPrice: number;
    volume24h: number;
}

export interface Trade {
    id: string;
    price: number;
    quantity: number;
    total: number;
    timestamp: number;
    buyer: string;
    seller: string;
}

import argparse
import json
import struct

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    print(f"📖 Loading TOON model from {args.input}...")
    with open(args.input, "r") as f:
        model_data = json.load(f)

    num_layers = model_data["num_layers"]
    threads_per_block = model_data.get("threads_per_block", 256)
    
    print(f"⚙️ Packing weights for {num_layers} layers with {threads_per_block} threads...")
    
    weights_pos = []
    weights_neg = []
    
    for layer in model_data["layers"]:
        weights = layer["weights"]
        # Ensure we have exactly threads_per_block weights, pad with 0 if necessary
        if len(weights) < threads_per_block:
            weights = weights + [0] * (threads_per_block - len(weights))
        else:
            weights = weights[:threads_per_block]
            
        for w in weights:
            if w == 1:
                weights_pos.append(0xFFFFFFFF)
                weights_neg.append(0)
            elif w == -1:
                weights_pos.append(0)
                weights_neg.append(0xFFFFFFFF)
            else:
                weights_pos.append(0)
                weights_neg.append(0)

    print(f"💾 Writing binary SPAT model to {args.output}...")
    with open(args.output, "wb") as f:
        # 1. Header
        f.write(b"SPAT")
        # 2. Version
        f.write(struct.pack("<I", 1))
        # 3. Num Layers
        f.write(struct.pack("<I", num_layers))
        # 4. Threads per block
        f.write(struct.pack("<I", threads_per_block))
        # 5. Weights length
        weights_len = len(weights_pos)
        f.write(struct.pack("<I", weights_len))
        
        # 6. Pos weights
        for val in weights_pos:
            f.write(struct.pack("<I", val))
            
        # 7. Neg weights
        for val in weights_neg:
            f.write(struct.pack("<I", val))

    print(f"✅ SPAT conversion complete: {args.output}")

if __name__ == "__main__":
    main()

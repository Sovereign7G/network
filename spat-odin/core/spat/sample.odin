package spat

import "core:math"
import "core:math/rand"

sample_token :: proc(logits: []f32, temperature: f32) -> u32 {
    if len(logits) == 0 {
        return 0
    }
    
    if temperature < 0.001 {
        max_val := logits[0]
        max_idx: u32 = 0
        for val, idx in logits {
            if val > max_val {
                max_val = val
                max_idx = u32(idx)
            }
        }
        return max_idx
    }
    
    max_logit := logits[0]
    for val in logits {
        if val > max_logit {
            max_logit = val
        }
    }
    
    probs := make([]f32, len(logits))
    defer delete(probs)
    
    exp_sum: f32 = 0.0
    for val, idx in logits {
        e := math.exp((val - max_logit) / temperature)
        probs[idx] = e
        exp_sum += e
    }
    
    if exp_sum <= 0.0 {
        return 0
    }
    
    for val, idx in probs {
        probs[idx] = val / exp_sum
    }
    
    r := rand.float32()
    cum: f32 = 0.0
    for prob, idx in probs {
        cum += prob
        if r <= cum {
            return u32(idx)
        }
    }
    
    return u32(len(probs) - 1)
}

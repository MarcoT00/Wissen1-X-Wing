# Wissen1-X-Wing

T = {1, 2, ..., N} (endliche Menge)

S = {s = (position, velocity)}
- position = (x, y)
- velocity = (v_x, v_y)

A = {
    (B, B), (B, H), (B, V),
    (H, B), (H, H), (H, V),
    (V, B), (V, H), (V, V)
}

p

c: S x S -> R
- Die Kosten is von dem aktuellen Zeitschritt, aktuellen Position, und Folgeposition abhängig.
- c(s_i, s_j) = 1 if 
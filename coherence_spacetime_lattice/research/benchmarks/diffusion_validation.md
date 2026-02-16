# Analytical Diffusion Benchmark

For pure diffusion:

∂t κ = Dκ ∇²κ

Initial delta pulse solution:

κ(r,t) = (1 / (4πDκ t)) exp(−r²/(4Dκ t))

Validation procedure:

1. Disable reaction terms.
2. Initialize narrow Gaussian.
3. Measure variance σ²(t).
4. Verify σ²(t) ≈ 2Dκ t.

Convergence test:

Error ∼ O(Δx² + Δt)

Results confirm second-order spatial accuracy.


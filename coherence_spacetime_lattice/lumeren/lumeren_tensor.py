"""
lumeren_tensor.py

Minimal symbolic–geometric layer that can actually encode equations and export LaTeX.
Not a CAS replacement; it is an internal representation that keeps:
  - semantic roles (κ, τ, Σ, Φ, Ω, etc.)
  - tensor indices
  - algebraic structure (sum, product, derivative, laplacian)

This makes docs and code share the same "equation objects".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Union, Literal


Op = Literal["sym", "add", "mul", "neg", "pow", "d", "lap"]


@dataclass(frozen=True)
class LumerenSymbol:
    name: str
    role: str
    arity: int = 0
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Expr:
    op: Op
    sym: Optional[LumerenSymbol] = None
    args: List["Expr"] = field(default_factory=list)
    power: Optional[float] = None
    var: Optional[str] = None  # for derivatives

    @staticmethod
    def Sym(s: LumerenSymbol) -> "Expr":
        return Expr(op="sym", sym=s)

    @staticmethod
    def Add(*terms: "Expr") -> "Expr":
        flat: List[Expr] = []
        for t in terms:
            if t.op == "add":
                flat.extend(t.args)
            else:
                flat.append(t)
        return Expr(op="add", args=flat)

    @staticmethod
    def Mul(*factors: "Expr") -> "Expr":
        flat: List[Expr] = []
        for f in factors:
            if f.op == "mul":
                flat.extend(f.args)
            else:
                flat.append(f)
        return Expr(op="mul", args=flat)

    @staticmethod
    def Neg(x: "Expr") -> "Expr":
        return Expr(op="neg", args=[x])

    @staticmethod
    def Pow(x: "Expr", p: float) -> "Expr":
        return Expr(op="pow", args=[x], power=float(p))

    @staticmethod
    def D(x: "Expr", var: str) -> "Expr":
        return Expr(op="d", args=[x], var=str(var))

    @staticmethod
    def Lap(x: "Expr") -> "Expr":
        return Expr(op="lap", args=[x])

    def latex(self) -> str:
        if self.op == "sym":
            return self.sym.name if self.sym else "<?>"
        if self.op == "add":
            return " + ".join(a.latex() for a in self.args) if self.args else "0"
        if self.op == "mul":
            return " ".join(_wrap_mul(a) for a in self.args) if self.args else "1"
        if self.op == "neg":
            return "-" + _wrap_atom(self.args[0]).latex()
        if self.op == "pow":
            base = _wrap_atom(self.args[0]).latex()
            return f"{base}^{{{self.power}}}"
        if self.op == "d":
            inner = self.args[0].latex()
            return f"\\partial_{{{self.var}}} {inner}"
        if self.op == "lap":
            inner = self.args[0].latex()
            return f"\\nabla^2 {inner}"
        return "<?>"

    def __add__(self, other: "Expr") -> "Expr":
        return Expr.Add(self, other)

    def __mul__(self, other: "Expr") -> "Expr":
        return Expr.Mul(self, other)

    def __neg__(self) -> "Expr":
        return Expr.Neg(self)


def _wrap_atom(x: Expr) -> Expr:
    if x.op in ("sym", "pow", "lap", "d"):
        return x
    return Expr(op="mul", args=[x])  # marker for parentheses in wrapper


def _wrap_mul(x: Expr) -> str:
    if x.op in ("add", "neg"):
        return f"({x.latex()})"
    return x.latex()


def default_lumeren_symbols() -> Dict[str, LumerenSymbol]:
    return {
        "kappa": LumerenSymbol(name="\\kappa", role="coherence_density", arity=0),
        "tau": LumerenSymbol(name="\\tau", role="temporal_responsibility", arity=0),
        "sigma": LumerenSymbol(name="\\Sigma", role="systemic_separation", arity=0),
        "phi": LumerenSymbol(name="\\Phi", role="coherence_potential", arity=0),
        "omega": LumerenSymbol(name="\\Omega", role="metric_scale", arity=0),
    }


def unified_pde_expressions() -> Dict[str, Expr]:
    """
    Returns symbolic PDE cores in Luméren form (without choosing fκ,fτ,fΣ explicitly).
    """
    S = default_lumeren_symbols()
    k = Expr.Sym(S["kappa"])
    t = Expr.Sym(S["tau"])
    s = Expr.Sym(S["sigma"])

    Dk = Expr.Sym(LumerenSymbol(name="D_\\kappa", role="diffusion"))
    Dt = Expr.Sym(LumerenSymbol(name="D_\\tau", role="diffusion"))
    Ds = Expr.Sym(LumerenSymbol(name="D_\\Sigma", role="diffusion"))

    Fk = Expr.Sym(LumerenSymbol(name="F_\\kappa(\\kappa,\\tau,\\Sigma)", role="reaction"))
    Ft = Expr.Sym(LumerenSymbol(name="F_\\tau(\\kappa,\\tau,\\Sigma)", role="reaction"))
    Fs = Expr.Sym(LumerenSymbol(name="F_\\Sigma(\\kappa,\\tau,\\Sigma)", role="reaction"))

    return {
        "kappa": Expr.Add(Expr.Mul(Dk, Expr.Lap(k)), Fk),
        "tau": Expr.Add(Expr.Mul(Dt, Expr.Lap(t)), Ft),
        "sigma": Expr.Add(Expr.Mul(Ds, Expr.Lap(s)), Fs),
    }

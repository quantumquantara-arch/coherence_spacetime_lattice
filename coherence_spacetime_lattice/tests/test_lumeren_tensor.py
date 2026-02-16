import unittest

from src.lumeren_tensor import (
    LumerenSymbol,
    LumerenTensor,
    default_lumeren_symbols,
)


class TestLumerenTensor(unittest.TestCase):

    def test_symbol_creation(self):
        sym = LumerenSymbol(name="κ", role="coherence", arity=2)
        self.assertEqual(sym.name, "κ")
        self.assertEqual(sym.role, "coherence")
        self.assertEqual(sym.arity, 2)
        self.assertIsInstance(sym.metadata, dict)

    def test_tensor_basic_structure(self):
        sym = LumerenSymbol(name="τ", role="temporal_responsibility", arity=1)
        tensor = LumerenTensor(symbol=sym, indices=["μ"])
        self.assertEqual(tensor.symbol.name, "τ")
        self.assertEqual(tensor.indices, ["μ"])
        self.assertEqual(tensor.connections, [])

    def test_tensor_connections(self):
        sym_k = LumerenSymbol(name="κ", role="coherence", arity=2)
        sym_s = LumerenSymbol(name="Σ", role="systemic_separation", arity=2)

        t1 = LumerenTensor(symbol=sym_k, indices=["μ", "ν"])
        t2 = LumerenTensor(symbol=sym_s, indices=["μ", "ν"])

        t1.add_connection(t2)

        self.assertEqual(len(t1.connections), 1)
        self.assertIs(t1.connections[0], t2)

    def test_describe_output(self):
        sym = LumerenSymbol(name="E", role="cosmic_cycle", arity=4)
        t = LumerenTensor(symbol=sym, indices=["α", "β", "γ", "δ"])
        desc = t.describe()

        self.assertIn("E_αβγδ", desc)
        self.assertIn("role=cosmic_cycle", desc)

    def test_default_symbols_dictionary(self):
        symbols = default_lumeren_symbols()
        self.assertIn("kappa", symbols)
        self.assertIn("tau", symbols)
        self.assertIn("sigma", symbols)
        self.assertIn("evercycle", symbols)

        self.assertEqual(symbols["kappa"].name, "κ")
        self.assertEqual(symbols["tau"].role, "temporal_responsibility")
        self.assertEqual(symbols["evercycle"].role, "cosmic_cycle")


if __name__ == "__main__":
    unittest.main()

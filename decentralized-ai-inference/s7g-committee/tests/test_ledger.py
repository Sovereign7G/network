import sys
import tempfile
from pathlib import Path

# Add the parent directories to path so we can import 'consensus'
sys.path.insert(0, str(Path(__file__).parent.parent))

from consensus.ledger import Ledger

def test_ledger_append_and_retrieve():
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger = Ledger(Path(tmpdir))
        assert ledger.count() == 0
        ledger.append(1, "req-1", {"model": "llama"}, {"tokens": 10}, 1600000000, 1)
        assert ledger.count() == 1
        blocks = ledger.get_all()
        assert blocks[0]["request_id"] == "req-1"
        assert blocks[0]["payload"]["model"] == "llama"
        ledger.close()

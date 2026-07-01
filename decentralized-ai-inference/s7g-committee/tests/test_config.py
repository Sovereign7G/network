import sys
from pathlib import Path

# Add the parent directories to path so we can import 'node'
sys.path.insert(0, str(Path(__file__).parent.parent))

from node.config import settings

def test_default_settings():
    assert settings.NODE_ID == 1
    assert settings.NODE_ROLE == "follower"
    assert settings.COMMITTEE_SIZE == 4

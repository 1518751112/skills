import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import client
from adapters.v2ex import _normalize


class ScanTests(unittest.TestCase):
    def test_sov2ex_scalar_node_and_member_are_normalized(self):
        post = _normalize({"id": 123, "title": "t", "content": "c", "node": 17, "member": "alice", "replies": 2})
        self.assertEqual("alice", post["author"])
        self.assertEqual("", post["node"])
        self.assertEqual({"comment_count": 2}, post["metrics"])

    def test_known_urls_are_saved_but_not_returned_by_default(self):
        post = {"platform": "v2ex", "external_id": "1", "url": "http://www.v2ex.com/t/1/", "title": "t", "content": "c", "node": "", "author": "", "published_at": None, "metrics": {}, "raw": {"large_provider_payload": True}}
        with tempfile.TemporaryDirectory() as directory:
            database = os.path.join(directory, "nested", "monitor.sqlite3")
            original = client.ADAPTERS["v2ex"]
            client.ADAPTERS["v2ex"] = lambda request: [post]
            try:
                config = {"platform": "v2ex", "database": database, "requests": [{"mode": "hot"}]}
                first_scan = client.scan(config)
                self.assertEqual(1, first_scan["counts"]["returned"])
                self.assertNotIn("raw", first_scan["posts"][0])
                self.assertEqual(0, client.scan(config)["counts"]["returned"])
                self.assertEqual(1, client.scan(config, include_known=True)["counts"]["returned"])
            finally:
                client.ADAPTERS["v2ex"] = original


if __name__ == "__main__":
    unittest.main()

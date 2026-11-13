"""资料与现有领域接口的核对。"""
import unittest,tempfile,json
from pathlib import Path
from lake.storage import Storage
from lake.patterns import inspect

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.store=Storage(self.root/'objects')
        self.data=json.loads(Path('data/source.json').read_text(encoding='utf-8'))
    def test_existing_reader(self):
        self.assertTrue(inspect(self.data,self.store,self.root))

    def test_ast_empty_and_label(self):
        from lake.patterns import nullable
        self.assertFalse(nullable(self.data['pattern'],self.data['labels']))
        with self.assertRaises(ValueError):nullable({'label':'missing'},self.data['labels'])
        with self.assertRaises(ValueError):nullable({'repeat':{'min':0,'max':None,'greedy':True,'node':{'repeat':{'min':0,'max':1,'greedy':True,'node':{'label':'A'}}}}},self.data['labels'])

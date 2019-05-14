import unittest
from InventoryAllocator import InventoryAllocator

class TestInventoryAllocator(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInventoryAllocator, self).__init__(*args, **kwargs)
        self.ia = InventoryAllocator()

    def test_exact_match(self):
        # test exact match
        self.ia.set_items({'apple': 1})
        self.ia.set_warehouse([{ 'name': 'owd', 'inventory': { 'apple': 1}}])
        self.assertEqual(self.ia.cheapest_shipment(), [{'owd': {'apple': 1}}])

        # test exact match at two warehouses
        self.ia.set_items({'apple': 1, 'pear': 2})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'apple': 1}}, {'name': 'dm', 'inventory': {'pear': 2}}])
        self.assertEqual(self.ia.cheapest_shipment(), [{'owd': {'apple': 1}}, {'dm': {'pear': 2}}])

        # test exact match at same warehouse
        self.ia.set_items({'apple': 1, 'pear': 2})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'apple': 1, 'pear': 2}}])
        self.assertEqual(self.ia.cheapest_shipment(), [{'owd':{'apple': 1, 'pear': 2}}])

    def test_inexact_match(self):
        # test inexact match at one warehouse
        self.ia.set_items({'apple': 3})
        self.ia.set_warehouse([{ 'name': 'owd', 'inventory': { 'apple': 11}}])
        self.assertEqual(self.ia.cheapest_shipment(), [{'owd': {'apple': 3}}])

        # test exact match at two warehouses
        self.ia.set_items({'apple': 3})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'apple': 1}}, {'name': 'dm', 'inventory': {'apple': 10}}])
        self.assertEqual(self.ia.cheapest_shipment(), [{'owd': {'apple': 1}}, {'dm': {'apple': 2}}])

    def test_insufficent_inventory(self):
        # test not listed at any warehouses
        self.ia.set_items({'apple':1})
        self.ia.set_warehouse([{'name':'dm', 'inventory': {'pear': 2}}])
        self.assertEqual(self.ia.cheapest_shipment(), [])

        # test insufficent at one warehouse
        self.ia.set_items({'apple':1})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'apple': 0}}, {'name':'dm', 'inventory': {'pear': 2}}])
        self.assertEqual(self.ia.cheapest_shipment(), [])

        # test insufficent count at multiple warehouses
        self.ia.set_items({'apple':10})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'apple': 5}}, {'name':'dm', 'inventory': {'apple': 4}}])
        self.assertEqual(self.ia.cheapest_shipment(), [])

        # test only one item insufficient
        self.ia.set_items({'apple':1, 'pear':2})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'pear': 2}}, {'name':'dm', 'inventory': {'pear': 0}}])
        self.assertEqual(self.ia.cheapest_shipment(), [])

    def test_split_inventory(self):
        # test one item split
        self.ia.set_items({'apple': 10})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'apple': 5}}, {'name':'dm', 'inventory': {'apple': 5}}])
        self.assertEqual(self.ia.cheapest_shipment(), [{'owd': {'apple': 5}}, {'dm': {'apple': 5}}])

        # test multiple items split
        self.ia.set_items({'apple': 10, 'pear': 10})
        self.ia.set_warehouse([{'name': 'owd', 'inventory': {'apple': 5, 'pear': 6}}, {'name': 'dm', 'inventory': {'apple': 5}}, {'name': 'po', 'inventory': {'pear': 4}}])
        self.assertEqual(self.ia.cheapest_shipment(), [{'owd': {'apple': 5, 'pear': 6}}, {'dm': {'apple': 5}}, {'po': {'pear': 4}}])


if __name__ == '__main__':
    unittest.main()
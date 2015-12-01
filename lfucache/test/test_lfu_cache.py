import unittest

import lfucache.lfu_cache as lfu_cache


class TestLfuCache(unittest.TestCase):

    def setUp(self):
        self.cache = lfu_cache.Cache()

    def test_insert_freq_nodes(self):
        node2 = self.cache.insert_freq_node(2, None, None)
        node1 = self.cache.insert_freq_node(1, None, node2)
        node4 = self.cache.insert_freq_node(4, node2, None)
        node3 = self.cache.insert_freq_node(3, node2, node4)

        nodes_data = self.cache.get_nodes_data()
        self.assertEqual(nodes_data, [1, 2, 3, 4])
        self.assertEqual(self.cache.count, 4)

        self.cache.remove_freq_node(node1)
        nodes_data = self.cache.get_nodes_data()
        self.assertEqual(nodes_data, [2, 3, 4])
        self.assertEqual(self.cache.count, 3)

        self.cache.remove_freq_node(node3)
        nodes_data = self.cache.get_nodes_data()
        self.assertEqual(nodes_data, [2, 4])

    def test_add_freq_item_nodes(self):
        freq_node1 = self.cache.insert_freq_node(1, None, None)
        freq_node2 = self.cache.insert_freq_node(2, freq_node1, None)
        freq_node1_item_node1 = freq_node1.insert_item_node('a', None, None)
        freq_node1.insert_item_node('b', freq_node1_item_node1, None)
        freq_node2_item_node2 = freq_node2.insert_item_node('d', None, None)
        freq_node2_item_node1 = freq_node2.insert_item_node(
            'c', None,
            freq_node2_item_node2)
        freq_node2_item_node4 = freq_node2.insert_item_node(
            'f', freq_node2_item_node2, None)
        freq_node2_item_node3 = freq_node2.insert_item_node(
            'e', freq_node2_item_node2, freq_node2_item_node4)
        freq_node2.add_item_node('g')

        nodes_data = freq_node1.get_nodes_data()
        self.assertEqual(nodes_data, ['a', 'b'])

        nodes_data = freq_node2.get_nodes_data()
        self.assertEqual(nodes_data, ['c', 'd', 'e', 'f', 'g'])

        freq_node2.remove_item_node(freq_node2_item_node1)
        nodes_data = freq_node2.get_nodes_data()
        self.assertEqual(nodes_data, ['d', 'e', 'f', 'g'])

        freq_node2.remove_item_node(freq_node2_item_node3)
        nodes_data = freq_node2.get_nodes_data()
        self.assertEqual(nodes_data, ['d', 'f', 'g'])

        freq_node2.remove_item_node_by_data('f')
        nodes_data = freq_node2.get_nodes_data()
        self.assertEqual(nodes_data, ['d', 'g'])

    def test_insert(self):
        self.cache.insert('k1', 'd1')
        self.cache.insert('k2', 'd2')
        self.cache.insert('k3', 'd3')

        nodes_data = self.cache.get_nodes_data()
        self.assertEqual(nodes_data, [1, ])

        nodes_data = self.cache.head.get_nodes_data()
        self.assertEqual(nodes_data, ['k1', 'k2', 'k3'])

        self.assertEqual(self.cache.items['k1'].data, 'd1')
        self.assertEqual(self.cache.items['k1'].parent, self.cache.head)
        self.assertEqual(self.cache.items['k1'].node, self.cache.head.head)
        self.assertEqual(self.cache.items['k2'].data, 'd2')
        self.assertEqual(self.cache.items['k2'].parent, self.cache.head)
        self.assertEqual(self.cache.items['k2'].node,
                         self.cache.head.head.next)
        self.assertEqual(self.cache.items['k3'].data, 'd3')
        self.assertEqual(self.cache.items['k3'].parent, self.cache.head)
        self.assertEqual(self.cache.items['k3'].node,
                         self.cache.head.head.next.next)

        self.assertRaises(lfu_cache.DuplicateException, self.cache.insert,
                          'k3', 'd3')

    def test_access(self):
        self.cache.insert('k1', 'd1')
        self.cache.insert('k2', 'd2')
        self.cache.insert('k3', 'd3')

        self.assertEqual(self.cache.access('k2'), 'd2')
        self.assertEqual(self.cache.access('k3'), 'd3')
        self.assertEqual(self.cache.access('k3'), 'd3')

        nodes_data = self.cache.get_nodes_data()
        self.assertEqual(nodes_data, [1, 2, 3])

        nodes_data = self.cache.head.get_nodes_data()
        self.assertEqual(nodes_data, ['k1'])
        nodes_data = self.cache.head.next.get_nodes_data()
        self.assertEqual(nodes_data, ['k2'])
        nodes_data = self.cache.head.next.next.get_nodes_data()
        self.assertEqual(nodes_data, ['k3'])

        self.assertEqual(str(self.cache), "1: ['k1']\n2: ['k2']\n3: ['k3']\n")

        self.assertEqual(self.cache.access('k1'), 'd1')
        self.assertEqual(self.cache.access('k3'), 'd3')

        nodes_data = self.cache.get_nodes_data()
        self.assertEqual(nodes_data, [2, 4])

        nodes_data = self.cache.head.get_nodes_data()
        self.assertEqual(nodes_data, ['k2', 'k1'])
        nodes_data = self.cache.head.next.get_nodes_data()
        self.assertEqual(nodes_data, ['k3'])

        self.assertRaises(lfu_cache.NotFoundException, self.cache.access, 'k4')

    def test_get_lfu(self):
        self.assertRaises(lfu_cache.NotFoundException,
                          self.cache.get_lfu)

        self.cache.insert('k1', 'd1')
        self.cache.insert('k2', 'd2')
        self.cache.insert('k3', 'd3')

        self.assertEqual(self.cache.access('k2'), 'd2')
        self.assertEqual(self.cache.access('k3'), 'd3')
        self.assertEqual(self.cache.access('k3'), 'd3')

        self.assertEqual(self.cache.get_lfu(), ('k1', 'd1'))

        self.assertEqual(self.cache.access('k1'), 'd1')

        self.assertEqual(self.cache.get_lfu(), ('k2', 'd2'))

    def test_delete_lfu(self):
        self.assertRaises(lfu_cache.NotFoundException,
                          self.cache.delete_lfu)

        self.cache.insert('k1', 'd1')
        self.cache.insert('k2', 'd2')
        self.cache.insert('k3', 'd3')
        self.assertEqual(self.cache.access('k2'), 'd2')
        self.assertEqual(self.cache.get_lfu(), ('k1', 'd1'))

        self.cache.delete_lfu()
        self.assertEqual(self.cache.get_lfu(), ('k3', 'd3'))

        self.cache.delete_lfu()
        self.assertEqual(self.cache.get_lfu(), ('k2', 'd2'))


if __name__ == '__main__':
    unittest.main()

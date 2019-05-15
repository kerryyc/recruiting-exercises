class InventoryAllocator():
    def __init__(self, imap = {}, wmap = {}):
        self.imap = imap
        self.wmap = wmap
        self.shipment = []

    def cheapest_shipment(self):
        # return the warehouses and inventory amounts that produces the cheapest shipment
        self.shipment = []
        shipped_warehouses = []
        temp_imap = self.imap
        temp_wmap = self.wmap

        for warehouse in range(len(self.wmap)):
            for item in list(self.imap.keys()):

                # if the warehouse inventory contains the item
                if item in self.wmap[warehouse]['inventory']:
                    self._update_shipment(shipped_warehouses, warehouse, item)

                # delete if the item needs no further shipments
                if self.imap[item] == 0:
                    del self.imap[item]

            # return shipment when all items are allocated
            if len(self.imap) == 0:
                return self.shipment

        # if shipment not returned in loop, then inventory could not be allocated
        # reset item and warehouse maps
        self.imap = temp_imap
        self.wmap = temp_wmap
        return []

    def _update_shipment(self, shipped_warehouses, warehouse, item):
        requested = self.imap[item]
        warehouse_name = self.wmap[warehouse]['name']

        # get index of warehouse in the shipment list
        if warehouse not in shipped_warehouses:
            shipped_warehouses.append(warehouse)
            self.shipment.append({warehouse_name : {}})
            windex = -1
        else:
            windex = shipped_warehouses.index(warehouse)

        # update shipment, warehouse_map, and item_map
        inventory = self.wmap[warehouse]['inventory'][item]
        if inventory >= requested:
            self.shipment[windex][warehouse_name][item] = self.shipment[windex][warehouse_name].get(item, 0) + requested
            self.wmap[warehouse]['inventory'][item] -= requested
            self.imap[item] = 0
        else:
            self.shipment[windex][warehouse_name][item] = self.shipment[windex][warehouse_name].get(item, 0) + inventory
            self.wmap[warehouse]['inventory'][item] -= inventory
            self.imap[item] -= inventory

        # if no more item, delete item from inventory of warehouse
        if self.wmap[warehouse]['inventory'][item] == 0:
            del self.wmap[warehouse]['inventory'][item]

    # Get/Set Methods
    def get_items(self):
        return self.imap

    def get_warehouse(self):
        return self.wmap

    def set_items(self, imap):
        self.imap = imap

    def set_warehouse(self, wmap):
        self.wmap = wmap
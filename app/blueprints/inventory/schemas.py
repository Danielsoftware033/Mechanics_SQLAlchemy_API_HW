from app.extensions import ma
from app.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


class Ticket_InventoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory

ticket_inventory_schema = Ticket_InventoriesSchema()
ticket_inventories_schema = Ticket_InventoriesSchema(many=True)
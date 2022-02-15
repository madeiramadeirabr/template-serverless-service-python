import datetime
import uuid

from flambda_app.helper import datetime_now_with_timezone
from flambda_app.vos import AbstractVO


class ProductVO(AbstractVO):
    """

    """
    def __init__(self, data: dict = None):
        """
        Always the dateobjects must be datetime instances
        """
        self.id = data.get('id') if data and "id" in data else None
        self.uuid = data.get('uuid') if data and "uuid" in data else str(uuid.uuid4())
        self.sku = data.get('sku') if data and "sku" in data else None
        self.name = data.get('name') if data and "name" in data else None
        self.description = data.get('description') if data and 'description' in data else None
        self.supplier_id = data.get('supplier_id') if data and 'supplier_id' in data else None
        self.created_at = data.get('created_at') if data and 'created_at' in data else datetime_now_with_timezone()
        self.updated_at = data.get('updated_at') if data and 'updated_at' in data else None
        self.deleted_at = data.get('deleted_at') if data and 'deleted_at' in data else None

    def to_json(self):
        """
        Transform before convert
        """
        # iso date format
        if isinstance(self.created_at, datetime.datetime):
            self.created_at = self.created_at.isoformat()

        # iso date format
        if isinstance(self.updated_at, datetime.datetime):
            self.updated_at = self.updated_at.isoformat()

        # iso date format
        if isinstance(self.deleted_at, datetime.datetime):
            self.deleted_at = self.deleted_at.isoformat()

        return super(ProductVO, self).to_json()

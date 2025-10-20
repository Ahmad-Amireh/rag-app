from .BaseDataModel import BaseDataModel
from .db_schemas import Asset
from .enums.data_base_enums import DataBaseEnum
from bson import ObjectId

class AssetModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object): # this is a way to make an init with async funciton
        instance= cls(db_client)
        await instance.init_collection()
        return instance


    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for indx in indexes : 
                await self.collection.create_index(
                    indx["key"],
                    name = indx["name"],
                    unique = indx["unique"]

                )

    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.model_dump(by_alias = True, exclude_unset= True))
        asset.id = result.inserted_id
        return asset


    async def get_all_projects(self, assert_project_id: str):
        return self.collection.find({
            "asset_project_id": ObjectId(assert_project_id) if isinstance (assert_project_id, str) else assert_project_id
        }).to_list(length=None)

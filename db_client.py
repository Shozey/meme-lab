import pymongo

# local imports
from config import MONGO_URI, STATIC_DB


class DbClientMeme:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        db = self.client[STATIC_DB]
        self.collection_name = 'meimei'
        self.collection = db[self.collection_name]

    def __len__(self):
        return self.collection.count_documents({})

    def add_image(self, img_url: str, text_pos: list):
        new_image = {
            'img_url': img_url,
            'text_pos': text_pos
        }
        inserted_document = self.collection.insert_one(new_image)
        print(f'Inserted document ID: {inserted_document.inserted_id}')

    def get_rand_image(self):
        return self.collection.aggregate([{'$sample': {'size': 1}}])

    def remove_image(self, img_url):
        self.collection.remove({'img_url': img_url})

    def close(self):
        self.client.close()

    def __del__(self):
        self.client.close()


class DbClientTemp:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        db = self.client[STATIC_DB]
        self.collection_name = 'temp'
        self.collection = db[self.collection_name]

    def __len__(self):
        return self.collection.count_documents({})

    def add_meme(self, img_url: str, text: str):
        new_image = {
            'img_url': img_url,
            'text': text,
            'upvote': 0,
            'downvote': 0
        }
        inserted_document = self.collection.insert_one(new_image)
        print(f'Inserted document ID: {inserted_document.inserted_id}')

    def get_all_memes(self):
        all_memes = self.collection.find({})
        return all_memes

    def close(self):
        self.client.close()

    def __del__(self):
        self.client.close()


client = DbClientMeme()
client.add_image(img_url='https://cdn.discordapp.com/attachments/453517620696711178/931038252926922782/video0-52.mov',
                 text_pos=[20, 30])
client.close()

import falcon

from falcon.http_status import HTTPStatus

from db.manager import DBManager


class HookDBMiddleware(object):

    def __init__(self, connection: str):
        self.connection = connection

    async def process_startup(self, scope, event):
        manager = DBManager(self.connection)
        await manager.create_all()


class CORSMiddleware(object):

    async def process_response(self, req, resp, resource, req_succeded):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')

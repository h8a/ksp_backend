import falcon
import logging
from datetime import datetime

from db.models import EmployeesModel
from resources import BaseResource

class EmployeesResource(BaseResource):

    async def on_get(self, req, resp):

        employees_db = await EmployeesModel.get_list_with_childrens_by(self.db.session, status='1')

        employees = [ employee.as_dict_with_children for employee in employees_db ]

        resp.status = falcon.HTTP_200
        resp.media = {
            'status': True,
            'data': employees
        }

    async def on_get_get_employee(self, req, resp, employee_id):

        employees_db = await EmployeesModel.get_list_with_childrens_by(self.db.session, status='1', id=str(employee_id))

        if len(employees_db) < 1:
            resp.status = falcon.HTTP_404
            resp.media = {
                'status': True,
                'message': 'Employee not fount'
            }
            return

        employees = [ employee.as_dict_with_children for employee in employees_db ]

        resp.status = falcon.HTTP_200
        resp.media = {
            'status': True,
            'data': employees[0]
        }

    async def on_post(self, req, resp):
        data = await req.get_media()

        employess_model = EmployeesModel(
            hire_date=datetime.strptime(data.get('hire_date'), '%Y-%M-%d'),
            job=data.get('job'),
            name=data.get('name'),
            salary=data.get('salary')
        )

        try:
            employees_db = await employess_model.save(self.db.session)
        except Exception:
            logging.getLogger('db').error('Error to save employees data: ', exc_info=True)
            resp.status = falcon.HTTP_503
            resp.media = {
                'status': False,
                'message': 'Error to try save employees data'
            }
            return

        resp.status = falcon.HTTP_201
        resp.media = {
            'status': True,
            'data': employees_db.as_dict
        }

    async def on_delete(self, req, resp, employee_id):
        try:
            await EmployeesModel.update(
                self.db.session,
                id=str(employee_id),
                status='0'
            )
        except Exception:
            logging.getLogger('db').error('Error to try to delete employees: ', exc_info=True)
            resp.status = falcon.HTTP_404
            resp.media = {
                'status': False,
                'message': 'Error to try delete employees'
            }
            return

        resp.status = falcon.HTTP_202
        resp.media = {
            'status': True,
        }

    async def on_put(self, req, resp, employee_id):

        data = await req.get_media()

        if 'hire_date' in data.keys():
            data['hire_date'] = datetime.strptime('hire_date', '%Y-%M-%d')

        try:
            await EmployeesModel.update(
                self.db.session,
                id=str(employee_id),
                **data
            ) 
        except Exception:
            logging.getLogger('db').error('Error to try update employees: ', exc_info=True)
            resp.status = falcon.HTTP_503
            resp.media = {
                'status': False,
                'message': 'Error to try update employees'
            }
            return

        resp.status = falcon.HTTP_202
        resp.media = {
            'status': True
        }

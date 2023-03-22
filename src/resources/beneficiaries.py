import falcon
import logging

from datetime import datetime

from db.models import EmployeesModel, EmployeesBeneficiariesModel
from resources import BaseResource


class BeneficiariesResource(BaseResource):

    async def on_get(self, req, resp):
        beneficiaries_db = await EmployeesBeneficiariesModel.get_list_by(self.db.session, status='1')

        beneficiaries = [ beneficiary.as_dict for beneficiary in beneficiaries_db ]

        resp.status = falcon.HTTP_200
        resp.media = {
            'status': True,
            'data': beneficiaries
        }

    async def on_post(self, req, resp):

        data = await req.get_media()

        employee = await EmployeesModel.get(self.db.session, id=data.get('employee_id'))
        if not employee:
            resp.status = falcon.HTTP_404
            resp.media = {
                'status': True,
                'message': 'Employee not found'
            }
            return

        employee_beneficiary_model = EmployeesBeneficiariesModel(
            name=data.get('name'),
            relationship=data.get('relationship'),
            birthdate=datetime.strptime(data.get('birthdate'), '%Y-%M-%d'),
            gender=data.get('gender'),
            employee_id=str(employee.id)
        )

        try:
            employee_beneficiary_db = await employee_beneficiary_model.save(self.db.session)
        except Exception:
            logging.getLogger('db').error('Error to try save beneficiary', exc_info=True)
            resp.status = falcon.HTTP_503
            resp.media = {
                'status': False,
                'message': 'Error to try save beneficiary'
            }
            return

        resp.status = falcon.HTTP_201
        resp.media = {
            'status': True,
            'data': employee_beneficiary_db.as_dict
        }

    async def on_delete(self, req, resp, beneficiary_id):

        try:
            await EmployeesBeneficiariesModel.update(
                self.db.session,
                id=str(beneficiary_id),
                status='0'
            )
        except Exception:
            logging.getLogger('db').error('Error to try delete beneficiary')
            resp.status = falcon.HTTP_404
            resp.media = {
                'status': False,
                'message': 'Error to try delete beneficiary'
            }
            return

        resp.status = falcon.HTTP_202
        resp.media = {
            'status': True
        }

    async def on_put(self, req, resp, beneficiary_id):
        data = await req.get_media()

        if 'birthdate' in data.keys():
            data['birthdate'] = datetime.strptime(data.get('birthdate'), '%Y-%M-%d')

        try:
            await EmployeesBeneficiariesModel.update(
                self.db.session,
                id=str(beneficiary_id),
                **data
            )
        except Exception:
            logging.getLogger('db').error('Error to try update beneficiary', exc_info=True)
            resp.status = falcon.HTTP_503
            resp.media = {
                'status': False,
                'message': 'Error to try update beneficiary'
            }
            return

        resp.status = falcon.HTTP_202
        resp.media = {
            'status': True
        }
import falcon.asgi

from config import cfg
from db.manager import DBManager
from middleware.hooks import HookDBMiddleware, CORSMiddleware
from resources.employees import EmployeesResource
from resources.beneficiaries import BeneficiariesResource


class Service(falcon.asgi.App):

    def __init__(self, *args, **kwargs) -> None:

        self._cors_enable = True

        super(Service, self).__init__(
            middleware=[
                falcon.CORSMiddleware(
                    allow_credentials='*',
                ),
                HookDBMiddleware(cfg.db),
                CORSMiddleware()
            ]
        )

        mgr = DBManager(cfg.db, debug=cfg.service.debug)

        employees_res = EmployeesResource(db_manager=mgr)
        employees_beneficiaries_res = BeneficiariesResource(db_manager=mgr)

        self.add_route(f'/api/{cfg.api.version}/employees', employees_res)
        self.add_route(f'/api/{cfg.api.version}/employees'+'/{employee_id}/put', employees_res, suffix='put_employee')
        self.add_route(f'/api/{cfg.api.version}/employees'+'/{employee_id}/delete', employees_res, suffix='delete_employee')
        self.add_route(f'/api/{cfg.api.version}/employees'+'/{employee_id}/get', employees_res, suffix='get_employee')
        self.add_route(f'/api/{cfg.api.version}/employees/beneficiaries/create', employees_beneficiaries_res, suffix='create_beneficiary')
        self.add_route(f'/api/{cfg.api.version}/employees/beneficiaries/list', employees_beneficiaries_res, suffix='list_beneficiary')
        self.add_route(f'/api/{cfg.api.version}/employees/beneficiaries/put'+'/{beneficiary_id}', employees_beneficiaries_res, suffix='put_beneficiary')
        self.add_route(f'/api/{cfg.api.version}/employees/beneficiaries/delete'+'/{beneficiary_id}', employees_beneficiaries_res, suffix='delete_beneficiary')

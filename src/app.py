import falcon.asgi

from config import cfg
from db.manager import DBManager
from middleware.hooks import HookDBMiddleware
from resources.employees import EmployeesResource
from resources.beneficiaries import BeneficiariesResource


class Service(falcon.asgi.App):

    def __init__(self, *args, **kwargs) -> None:

        self._cors_enable = True

        super(Service, self).__init__(
            middleware=[
                falcon.CORSMiddleware(
                    allow_credentials='*'
                ),
                HookDBMiddleware(cfg.db)
            ]
        )

        mgr = DBManager(cfg.db, debug=cfg.service.debug)

        employees_res = EmployeesResource(db_manager=mgr)
        employees_beneficiaries_res = BeneficiariesResource(db_manager=mgr)

        self.add_route(f'/api/{cfg.api.version}/employees', employees_res)
        self.add_route(f'/api/{cfg.api.version}/employees'+'/{employee_id}', employees_res)
        self.add_route(f'/api/{cfg.api.version}/employees/beneficiaries', employees_beneficiaries_res)
        self.add_route(f'/api/{cfg.api.version}/employees/beneficiaries'+'/{beneficiary_id}', employees_beneficiaries_res)

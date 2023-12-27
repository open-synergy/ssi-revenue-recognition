# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

{
    "name": "Revenue Recognition + Project Integration",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_revenue_recognition",
        "ssi_project",
    ],
    "data": [
        "views/service_type_views.xml",
        "views/service_contract_performance_obligation_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}

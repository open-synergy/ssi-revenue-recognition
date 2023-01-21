# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

{
    "name": "Revenue Recognition",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_financial_accounting",
        "ssi_cost_accounting",
        "ssi_master_data_mixin",
    ],
    "data": [
        "menu.xml",
        "views/account_analytic_account_views.xml",
    ],
    "demo": [
        "demo/account_account_demo.xml",
        "demo/account_journal_demo.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}

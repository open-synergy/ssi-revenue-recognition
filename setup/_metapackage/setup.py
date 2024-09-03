import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-revenue-recognition",
    description="Meta package for open-synergy-ssi-revenue-recognition Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_performance_obligation_quality_control',
        'odoo14-addon-ssi_revenue_recognition',
        'odoo14-addon-ssi_revenue_recognition_full',
        'odoo14-addon-ssi_revenue_recognition_project',
        'odoo14-addon-ssi_revenue_recognition_work_log',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)

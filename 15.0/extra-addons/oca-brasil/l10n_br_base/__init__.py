# Copyright (C) 2009  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from .hooks import pre_init_hook

# Remover a importação do models aqui
# from . import models

from odoo.addons import account
from odoo import api, tools, SUPERUSER_ID

# Função para carregar o modelo quando necessário
def load_models():
    from . import models

# Instalar o Template do Simple Chart of Account para Empresas Brasileiras
_auto_install_l10n_original = account._auto_install_l10n

def _auto_install_l10n_br_generic_module(env):
    country_code = env.company.country_id.code
    if country_code and country_code.upper() == "BR":
        if (
            hasattr(env.user.company_id, "tax_framework")
            and env.company.tax_framework == "3"
        ):
            module_name_domain = [("name", "=", "l10n_br_coa_generic")]
        else:
            module_name_domain = [("name", "=", "l10n_br_coa_simple")]

        # Carregar todos os COA l10n_br em modo demo:
        env.cr.execute("select demo from ir_module_module where name='l10n_br_base';")
        if env.cr.fetchone()[0]:
            module_name_domain = [
                (
                    "name",
                    "in",
                    ("l10n_br_coa_simple", "l10n_br_coa_generic", "l10n_generic_coa"),
                )
            ]

        module_ids = env["ir.module.module"].search(
            module_name_domain + [("state", "=", "uninstalled")]
        )
        module_ids.sudo().button_install()
    else:
        _auto_install_l10n_original(env)

account._auto_install_l10n = _auto_install_l10n_br_generic_module

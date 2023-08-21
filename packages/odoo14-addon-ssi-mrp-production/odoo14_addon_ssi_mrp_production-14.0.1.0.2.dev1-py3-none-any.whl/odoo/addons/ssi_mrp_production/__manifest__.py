# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "MRP Production",
    "version": "14.0.1.0.1",
    "category": "Manufacturing/Manufacturing",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "website": "https://simetri-sinergi.id",
    "depends": [
        "mrp",
        "stock_move_backdating",
    ],
    "data": [
        "views/mrp_production_views.xml",
    ],
    "installable": True,
}

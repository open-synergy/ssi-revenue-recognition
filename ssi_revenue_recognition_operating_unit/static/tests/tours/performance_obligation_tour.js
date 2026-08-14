/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_revenue_recognition_operating_unit.performance_obligation_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/performance_obligation/01-create.md (delta of
        // ssi_revenue_recognition's own 01-create.md). Delta-only tour: open
        // the menu, open a new form, assert the Operating Unit field is
        // shown and can be filled in, then stop — it does not continue to
        // Save/Confirm/Approve, which are already covered by the base
        // module's own create tour.
        tour.register(
            "ssi_revenue_recognition_operating_unit_performance_obligation_create",
            {test: true, url: "/web"},
            [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Cost Accounting app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
                },
                {
                    content: "Open the Revenue Recognition menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.menu_revenue_recognition"]',
                },
                {
                    content: "Open the Performance Obligations menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.performance_obligation_menu"]',
                },
                {
                    content: "Performance Obligations list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Performance Obligations)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Click the New button.
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Additional Fields — Operating Unit is shown next to
                // Company and can be filled in.
                {
                    content: "Operating Unit field is shown on the form",
                    trigger: ".o_field_widget[name='operating_unit_id']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Open the Operating Unit dropdown",
                    trigger: ".o_field_many2one[name='operating_unit_id'] input",
                    run: "text Main Operating Unit",
                },
                {
                    content: "Pick Main Operating Unit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Main Operating Unit)",
                    in_modal: false,
                },
                {
                    // `operating.unit.name_get()` prefixes the code, e.g.
                    // "[OU1] Main Operating Unit" — match on a substring of
                    // the input's value instead of the exact display name,
                    // so the tour does not depend on that code.
                    content: "Operating Unit is filled in on the form",
                    trigger:
                        ".o_field_many2one[name='operating_unit_id'] input[value*='Main Operating Unit']",
                    run: function () {
                        // Assertion only. The tour stops here — Save/
                        // Confirm/Approve are out of scope for this delta.
                    },
                },
            ]
        );
    }
);

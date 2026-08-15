/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_revenue_recognition_project_operating_unit.performance_obligation_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/performance_obligation/05-approve.md (delta of
        // ssi_revenue_recognition_project_operating_unit -- Additional
        // Post-Condition, itself extending the delta already documented
        // by ssi_revenue_recognition_project). Navigation is scaffolded
        // from the base module's own "05-approve" tour Flow
        // (ssi_revenue_recognition); this delta adds no Flow step of
        // its own -- per the Keputusan Desain of issue #57, the tour
        // only runs the Flow through to Open and stops there. It does
        // not open the Project tab or inspect the created project's
        // Operating Unit -- that value is unit test territory (see
        // tests/test_data_performance_obligation.yaml in this module).
        tour.register(
            "ssi_revenue_recognition_project_operating_unit_performance_obligation_approve",
            {test: true, url: "/web"},
            [
                // Base Flow 1 -- Open the Cost Accounting > Revenue
                // Recognition > Performance Obligations menu.
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

                // Base Flow 2 -- Open the record to approve.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR-POB-PROJECT-OU-APPROVE) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Base Flow 3 -- Click the Approve button.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Base Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Additional Post-Condition (docs/performance_obligation/
                // 05-approve.md of this module) -- the single approval
                // level is fulfilled, so the record is auto-opened
                // (action_open), which also runs the OU-propagation
                // side effect this module adds. Per the Keputusan
                // Desain, the tour stops at this statusbar assertion --
                // it does not inspect the created project's Operating
                // Unit value.
                {
                    content: "Status is Open",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);

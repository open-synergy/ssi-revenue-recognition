/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_revenue_recognition_work_log.performance_obligation_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/performance_obligation/01-create.md (delta of
    // ssi_revenue_recognition's own 01-create.md). Delta-only tour: open
    // the menu, open a new form, open the added Work Log tab, and
    // assert its fields are rendered — then stop. It does not continue
    // to Save/Confirm/Approve, which are already covered by the base
    // module's own create tour, and it does not assert any computed
    // value (Total/Remaining/Excess), which is unit test territory.
    tour.register(
        "ssi_revenue_recognition_work_log_performance_obligation_create",
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

            // Modified Flow — the Work Log tab is added by this
            // module, present from the moment the form opens.
            {
                content: "Work Log tab is displayed",
                trigger: ".o_notebook .nav-link:contains(Work Log)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Work Log Analytic Account field is shown on the tab",
                trigger: ".o_field_widget[name='work_log_analytic_account_id']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Estimation field is shown on the tab",
                trigger: ".o_field_widget[name='work_estimation']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Work Logs list is shown on the tab",
                trigger: ".o_field_widget[name='work_log_ids']",
                run: function () {
                    // Assertion only. The tour stops here — the list
                    // stays empty in this delta (picking/creating a
                    // work log line is out of scope for this
                    // module's Design Decision), and Save/Confirm/
                    // Approve are covered by the base create tour.
                },
            },
        ]
    );
});

/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_performance_obligation_quality_control.performance_obligation_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/performance_obligation/01-create.md (delta of
    // ssi_revenue_recognition's own 01-create.md). Delta-only tour: open
    // the menu, open a new form, open the added Quality Control tab, and
    // assert its fields are rendered — then stop. It does not continue
    // to Save/Confirm/Approve, which are already covered by the base
    // module's own create tour, and it does not assert any computed
    // value (Automatic/Final result), which is unit test territory. It
    // also does not click the Create Worksheet From Set / Open QC
    // Worksheet buttons — operating the worksheet itself is governed by
    // ssi_quality_control, out of scope for this module's Design
    // Decision.
    tour.register(
        "ssi_performance_obligation_quality_control_performance_obligation_create",
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

            // Modified Flow — the Quality Control tab is added by this
            // module, present from the moment the form opens.
            {
                content: "Quality Control tab is displayed",
                trigger: ".o_notebook .nav-link:contains(Quality Control)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Worksheet Set field is shown on the tab",
                trigger: ".o_field_widget[name='qc_worksheet_set_id']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Result Computation Method field is shown on the tab",
                trigger: ".o_field_widget[name='qc_result_computation_method']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "QC Worksheets list is shown on the tab",
                trigger: ".o_field_widget[name='qc_worksheet_ids']",
                run: function () {
                    // Assertion only. The tour stops here — it does not
                    // click Create Worksheet From Set / Open QC
                    // Worksheet (governed by ssi_quality_control), and
                    // Save/Confirm/Approve are covered by the base
                    // create tour.
                },
            },
        ]
    );
});

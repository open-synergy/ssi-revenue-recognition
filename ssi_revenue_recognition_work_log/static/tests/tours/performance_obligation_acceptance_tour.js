/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_revenue_recognition_work_log.performance_obligation_acceptance_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/performance_obligation_acceptance/01-create.md (delta of
        // ssi_revenue_recognition's own 01-create.md). Delta-only tour: open
        // the menu, open a new form, fill in just enough of the base Flow
        // (Partner / # Performance Obligation / Date Start / Date End) for
        // `allowed_work_log_ids` to have something to offer, then assert
        // both added tabs — Work Log and Fulfillment Work Logs — and that
        // a work log within the allowed set can actually be picked. It
        // does not continue to Save/Confirm/Approve, which are already
        // covered by the base module's own create tour, and it does not
        // assert `qty_work_log`'s resulting value, which is unit test
        // territory.
        tour.register(
            "ssi_revenue_recognition_work_log_performance_obligation_acceptance_create",
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
                    content: "Open the Performance Obligation Acceptances menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.performance_obligation_acceptance_menu"]',
                },
                {
                    content: "Performance Obligation Acceptances list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Performance Obligation Acceptances)",
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

                // Base Flow 3 (partial) — just enough for
                // `allowed_work_log_ids` to be computed.
                {
                    content: "Select the Partner",
                    trigger: ".o_field_many2one[name='partner_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-POBAWL-PARTNER",
                },
                {
                    content: "Pick the Partner from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-POBAWL-PARTNER)",
                    in_modal: false,
                },
                {
                    content: "Select the # Performance Obligation",
                    trigger:
                        ".o_field_many2one[name='performance_obligation_id'] input",
                    run: "text PB-TOUR-POBAWL-1",
                },
                {
                    content: "Pick the PoB from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(PB-TOUR-POBAWL-1)",
                    in_modal: false,
                },
                {
                    content: "Fill in Date Start",
                    trigger: ".o_field_widget[name='date_start'] input",
                    run: "text 01/01/2026",
                },
                {
                    content: "Fill in Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    run: "text 01/31/2026",
                },

                // Modified Flow — the Work Log tab (shared with
                // Performance Obligation and Revenue Recognition; see
                // docs/performance_obligation/01-create.md in this
                // module).
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

                // Modified Flow — the Fulfillment Work Logs tab is
                // specific to Acceptance.
                {
                    content: "Fullfilment Work Logs tab is displayed",
                    trigger: ".o_notebook .nav-link:contains(Fullfilment Work Logs)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Work Qty field is shown on the tab",
                    trigger: ".o_field_widget[name='qty_work_log']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // The work log list offered here is restricted to
                // `allowed_work_log_ids`: only the fixture booked
                // against the linked PoB's analytic account, dated
                // within Date Start/Date End, and Done is selectable.
                {
                    content: "Open the Add dialog on the Work Logs list",
                    trigger:
                        ".o_field_widget[name='poa_work_log_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "The allowed work log is offered in the dialog",
                    trigger:
                        ".modal .o_list_view .o_data_row:contains(TOUR-POBAWL-WORKLOG-1)",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Select the allowed work log's row",
                    trigger:
                        ".modal .o_list_view .o_data_row:contains(TOUR-POBAWL-WORKLOG-1) .o_list_record_selector input",
                },
                {
                    content: "Confirm the selection",
                    trigger: ".modal-footer .o_select_button",
                    in_modal: true,
                },

                // Post-Condition of this delta — the picked work log now
                // appears in the tab's own list. The tour stops here: it
                // does not assert the resulting Work Qty value (unit
                // test territory), and does not continue to Save.
                {
                    content: "The picked work log now appears on the tab",
                    trigger:
                        ".o_field_widget[name='poa_work_log_ids'] .o_data_row:contains(TOUR-POBAWL-WORKLOG-1)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);

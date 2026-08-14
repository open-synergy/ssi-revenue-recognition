/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_revenue_recognition.performance_obligation_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every tour below — Open the Cost Accounting > Revenue
    // Recognition > Performance Obligations menu.
    var openMenuSteps = function () {
        return [
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
        ];
    };

    // IK: docs/performance_obligation/01-create.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_create",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Click the New button.
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

            // Flow 3 — Fill in the required fields.
            {
                content: "Fill in the Title",
                trigger: ".o_field_widget[name='title']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-POB-CREATE",
            },
            {
                content: "Select the Source Analytic Account",
                trigger: ".o_field_many2one[name='source_analytic_account_id'] input",
                run: "text TOUR-POB-SOURCE-AA",
            },
            {
                content: "Pick the Source Analytic Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-POB-SOURCE-AA)",
                in_modal: false,
            },

            // Flow 4 — Transaction Price Allocation tab.
            {
                content: "Open the Transaction Price Allocation tab",
                trigger: ".o_notebook .nav-link:contains(Transaction Price Allocation)",
            },
            {
                content: "Fill in the Price Unit",
                trigger: ".o_field_widget[name='price_unit'] input",
                run: "text 100.00",
            },

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },

            // Post-Condition — A new record is created in Draft status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation/02-edit.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_edit",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-POB-EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Edit button.
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 4 — Change the required fields.
            {
                content: "Change the Title",
                trigger: ".o_field_widget[name='title']",
                run: "text TOUR-POB-EDIT-UPDATED",
            },

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // Post-Condition — The record is updated with the new values.
            {
                content: "Go back to the list",
                trigger:
                    ".breadcrumb-item:not(.active):contains(Performance Obligations)",
            },
            {
                content: "The updated title is shown in the list",
                trigger: ".o_data_row:contains(TOUR-POB-EDIT-UPDATED)",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation/03-delete.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_delete",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to delete.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-POB-DELETE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Open the Action menu.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },

            // Flow 4 — Click Delete.
            {
                content: "Click Delete",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },

            // Flow 5 — Click OK to confirm.
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // Odoo sometimes leaves a clickable back button on the
            // breadcrumb after a delete, and sometimes returns straight
            // to the list on its own. Click the back button only if one
            // is actually there.
            {
                content: "Return to the list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Performance Obligations), .o_list_view:not(:has(.o_data_row:contains(TOUR-POB-DELETE)))",
                run: function () {
                    var $back = $(
                        ".breadcrumb-item.o_back_button a:contains(Performance Obligations)"
                    );
                    if ($back.length) {
                        $back[0].click();
                    }
                },
            },

            // Post-Condition — The record is permanently removed.
            {
                content: "The record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-POB-DELETE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation/04-confirm.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_confirm",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-POB-CONFIRM) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Waiting for Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation/05-approve.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_approve",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-POB-APPROVE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — the single approval level is fulfilled,
            // so the record is auto-opened (action_open).
            {
                content: "Status is Open",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation/06-reject.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_reject",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to reject.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-POB-REJECT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Rejected.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation/10-cancel.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_cancel",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to cancel.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-POB-CANCEL) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Cancel button (type="action").
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
            },
            {
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 4 — Select the Reason.
            {
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:has(label:contains(TOUR Cancel Reason)) input.o_radio_input",
                run: "click",
            },

            // Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Cancelled.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation/12-restart.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_restart",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to restart.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-POB-RESTART) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status returns to Draft.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});

/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_revenue_recognition.performance_obligation_acceptance_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every tour below — Open the Cost Accounting > Revenue
    // Recognition > Performance Obligation Acceptances menu.
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
        ];
    };

    // IK: docs/performance_obligation_acceptance/01-create.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_create",
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
                content: "Select the Partner",
                trigger: ".o_field_many2one[name='partner_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-POBA-PARTNER",
            },
            {
                content: "Pick the Partner from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-POBA-PARTNER)",
                in_modal: false,
            },
            {
                content: "Select the # Performance Obligation",
                trigger: ".o_field_many2one[name='performance_obligation_id'] input",
                run: "text PB-TOUR-POBA-1",
            },
            {
                content: "Pick the PoB from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(PB-TOUR-POBA-1)",
                in_modal: false,
            },
            {
                content: "Fill in the Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/15/2026",
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

            // Post-Condition — A new record is created in Draft.
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

    // IK: docs/performance_obligation_acceptance/02-edit.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_edit",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(POA-TOUR-EDIT) .o_data_cell:first",
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
                content: "Change the Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/20/2026",
            },

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // Post-Condition — The record is updated.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation_acceptance/03-delete.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_delete",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to delete.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(POA-TOUR-DELETE) .o_data_cell:first",
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
            {
                content: "Back to the list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Performance Obligation Acceptances)",
            },

            // Post-Condition — The record is permanently removed.
            {
                content: "The record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(POA-TOUR-DELETE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation_acceptance/04-confirm.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_confirm",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(POA-TOUR-CONFIRM) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
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

    // IK: docs/performance_obligation_acceptance/05-approve.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_approve",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(POA-TOUR-APPROVE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // The single approval level is fulfilled, so the
            // record is auto-finished (action_done).
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/performance_obligation_acceptance/06-reject.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_reject",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(POA-TOUR-REJECT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
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

    // IK: docs/performance_obligation_acceptance/10-cancel.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_cancel",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(POA-TOUR-CANCEL) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
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
            {
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:has(label:contains(TOUR Cancel Reason)) input.o_radio_input",
                run: "click",
            },
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
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

    // IK: docs/performance_obligation_acceptance/12-restart.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_restart",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(POA-TOUR-RESTART) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
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

    // IK: docs/performance_obligation_acceptance/14-restart-approval.md
    tour.register(
        "ssi_revenue_recognition_performance_obligation_acceptance_restart_approval",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record whose approval process will
            // be restarted.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(POA-TOUR-RESTARTAPPROVAL) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Restart Approval Process button.
            {
                content: "Click the Restart Approval Process button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reload_approval_template']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status remains Waiting for Approval.
            {
                content: "Status is still Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});

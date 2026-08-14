/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_revenue_recognition.revenue_recognition_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every tour below — Open the Cost Accounting > Revenue
    // Recognition > Revenue Recognitions menu.
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
                content: "Open the Revenue Recognitions menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.revenue_recognition_menu"]',
            },
            {
                content: "Revenue Recognitions list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Revenue Recognitions)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    };

    // IK: docs/revenue_recognition/01-create.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_create",
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

            // Flow 3 — Fill in the required fields. Partner and # Performance
            // Obligation are selected before Type so that `product_id`
            // (related through the PoB) is already resolved when Type's
            // onchange looks up the Unearned Income/Income Account.
            {
                content: "Select the Partner",
                trigger: ".o_field_many2one[name='partner_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-RR-PARTNER",
            },
            {
                content: "Pick the Partner from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-RR-PARTNER)",
                in_modal: false,
            },
            {
                content: "Select the # Performance Obligation",
                trigger: ".o_field_many2one[name='performance_obligation_id'] input",
                run: "text PB-TOUR-RR-1",
            },
            {
                content: "Pick the PoB from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(PB-TOUR-RR-1)",
                in_modal: false,
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR-RR-TYPE",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-RR-TYPE)",
                in_modal: false,
            },
            {
                content: "Journal is auto-filled from Type",
                trigger: ".o_field_many2one[name='journal_id'] input[value!='']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content:
                    "Fill in the Unearned Income Account (no account mapping is configured for the product, so it was not auto-resolved)",
                trigger: ".o_field_many2one[name='unearned_income_account_id'] input",
                run: "text TOUR RR Unearned Income Account",
            },
            {
                content: "Pick the Unearned Income Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR RR Unearned Income Account)",
                in_modal: false,
            },
            {
                content:
                    "Fill in the Income Account (no account mapping is configured for the product, so it was not auto-resolved)",
                trigger: ".o_field_many2one[name='income_account_id'] input",
                run: "text TOUR RR Income Account",
            },
            {
                content: "Pick the Income Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR RR Income Account)",
                in_modal: false,
            },
            {
                content: "Fill in the Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/31/2026",
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

            // Flow 5 — Click Populate.
            {
                content: "Click Populate",
                trigger: "button[name='action_populate']:enabled",
                extra_trigger: ".o_form_view.o_form_editable",
            },

            // Flow 6 — Click Save.
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

    // IK: docs/revenue_recognition/02-edit.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_edit",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(RR-TOUR-EDIT) .o_data_cell:first",
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
                run: "text 01/30/2026",
            },

            // Flow 5 — Click Populate to refresh linked data.
            {
                content: "Click Populate",
                trigger: "button[name='action_populate']:enabled",
                extra_trigger: ".o_form_view.o_form_editable",
            },

            // Flow 6 — Click Save.
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

    // IK: docs/revenue_recognition/03-delete.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_delete",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(RR-TOUR-DELETE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
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
                    ".breadcrumb-item.o_back_button a:contains(Revenue Recognitions), .o_list_view:not(:has(.o_data_row:contains(RR-TOUR-DELETE)))",
                run: function () {
                    var $back = $(
                        ".breadcrumb-item.o_back_button a:contains(Revenue Recognitions)"
                    );
                    if ($back.length) {
                        $back[0].click();
                    }
                },
            },
            {
                content: "The record no longer appears in the list",
                trigger: ".o_list_view:not(:has(.o_data_row:contains(RR-TOUR-DELETE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/revenue_recognition/04-confirm.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_confirm",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(RR-TOUR-CONFIRM) .o_data_cell:first",
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

    // IK: docs/revenue_recognition/05-approve.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_approve",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(RR-TOUR-APPROVE) .o_data_cell:first",
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
            // The single approval level is fulfilled, so the record is
            // auto-finished (action_done) and its accounting entry is
            // posted.
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

    // IK: docs/revenue_recognition/06-reject.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_reject",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(RR-TOUR-REJECT) .o_data_cell:first",
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

    // IK: docs/revenue_recognition/10-cancel.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_cancel",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(RR-TOUR-CANCEL) .o_data_cell:first",
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

    // IK: docs/revenue_recognition/12-restart.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_restart",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(RR-TOUR-RESTART) .o_data_cell:first",
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

    // IK: docs/revenue_recognition/14-restart-approval.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_restart_approval",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(RR-TOUR-RESTARTAPPROVAL) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Restart Approval Process button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reload_approval_template']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
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

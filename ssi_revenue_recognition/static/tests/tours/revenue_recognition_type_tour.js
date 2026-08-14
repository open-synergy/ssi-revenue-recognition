/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_revenue_recognition.revenue_recognition_type_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/revenue_recognition_type/01-create.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Cost Accounting > Configuration > Revenue
            // Recognition > Revenue Recognition Types menu. The "Revenue
            // Recognition" level is a level-3 grouping header without its
            // own action or data-menu-xmlid, so it has no step.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Cost Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_cost_accounting_configuration"]',
            },
            {
                content: "Open the Revenue Recognition Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.revenue_recognition_type_menu"]',
            },
            {
                content: "Revenue Recognition Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Revenue Recognition Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

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
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-RRT-CREATE",
            },
            {
                content: "Select the Journal",
                trigger: ".o_field_many2one[name='journal_id'] input",
                run: "text TOUR RRT Journal",
            },
            {
                content: "Pick the Journal from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR RRT Journal)",
                in_modal: false,
            },
            {
                content: "Select the Unearned Income Usage",
                trigger: ".o_field_many2one[name='unearned_income_usage_id'] input",
                run: "text TOUR RRT Unearned Usage",
            },
            {
                content: "Pick the Unearned Income Usage from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR RRT Unearned Usage)",
                in_modal: false,
            },
            {
                content: "Select the Income Usage",
                trigger: ".o_field_many2one[name='income_usage_id'] input",
                run: "text TOUR RRT Income Usage",
            },
            {
                content: "Pick the Income Usage from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR RRT Income Usage)",
                in_modal: false,
            },

            // Flow 5 — Click Generate Code to assign a document code.
            {
                content: "Click Generate Code",
                trigger: ".o_form_view button[name='action_generate_code']",
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

            // Post-Condition — A new record is created and active.
            {
                content: "The type is active (no Archived ribbon)",
                trigger: ".o_form_view:not(:has(.ribbon:visible:contains(Archived)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/revenue_recognition_type/02-edit.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_type_edit",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Cost Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_cost_accounting_configuration"]',
            },
            {
                content: "Open the Revenue Recognition Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.revenue_recognition_type_menu"]',
            },
            {
                content: "Revenue Recognition Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Revenue Recognition Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-RRT-EDIT) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
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

            // Flow 3 — Change the required fields.
            {
                content: "Change the Name",
                trigger: ".o_field_widget[name='name']",
                run: "text TOUR-RRT-EDIT-UPDATED",
            },

            // Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // Post-Condition — The record is updated with the new values.
            {
                content: "Go back to the list",
                trigger:
                    ".breadcrumb-item:not(.active):contains(Revenue Recognition Types)",
            },
            {
                content: "The updated name is shown in the list",
                trigger: ".o_data_row:contains(TOUR-RRT-EDIT-UPDATED)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/revenue_recognition_type/03-delete.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_type_delete",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Cost Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_cost_accounting_configuration"]',
            },
            {
                content: "Open the Revenue Recognition Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.revenue_recognition_type_menu"]',
            },
            {
                content: "Revenue Recognition Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Revenue Recognition Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Select one or more records to delete.
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-RRT-DELETE) .o_list_record_selector input",
                extra_trigger: ".o_list_view",
            },

            // Flow 3 — Click Action > Delete.
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

            // Flow 4 — Click OK to confirm.
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — The record is permanently removed.
            {
                content: "The record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-RRT-DELETE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/revenue_recognition_type/04-deactivate.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_type_deactivate",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Cost Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_cost_accounting_configuration"]',
            },
            {
                content: "Open the Revenue Recognition Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.revenue_recognition_type_menu"]',
            },
            {
                content: "Revenue Recognition Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Revenue Recognition Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Select one or more records to deactivate.
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-RRT-DEACTIVATE) .o_list_record_selector input",
                extra_trigger: ".o_list_view",
            },

            // Flow 3 — Click Action > Archive.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Archive",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $archive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Archive";
                        }
                    );
                    $archive[0].click();
                },
            },

            // Flow 4 — Click OK to confirm.
            {
                content: "Confirm archiving",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — The record is archived and no longer listed.
            {
                content: "The record no longer appears in the default list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-RRT-DEACTIVATE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/revenue_recognition_type/05-activate.md
    tour.register(
        "ssi_revenue_recognition_revenue_recognition_type_activate",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Cost Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_cost_accounting_configuration"]',
            },
            {
                content: "Open the Revenue Recognition Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_revenue_recognition.revenue_recognition_type_menu"]',
            },
            {
                content: "Revenue Recognition Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Revenue Recognition Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Enable the Archived filter.
            {
                content: "Open the Filters menu",
                trigger: ".o_search_options .o_filter_menu button",
            },
            {
                content: "Enable the Archived filter",
                trigger: ".o_filter_menu .dropdown-item:contains(Archived)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Archived filter is active",
                trigger:
                    ".o_filter_menu .dropdown-item:contains(Archived)[aria-checked='true']",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Select one or more records to reactivate.
            {
                content: "Select the record",
                trigger:
                    ".o_data_row:contains(TOUR-RRT-ACTIVATE) .o_list_record_selector input",
                extra_trigger: ".o_list_view",
            },

            // Flow 4 — Click Action > Unarchive. No confirmation dialog.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Unarchive",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $unarchive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Unarchive";
                        }
                    );
                    $unarchive[0].click();
                },
            },

            // Post-Condition — The record is restored, appears in the
            // default list again.
            {
                content: "Disable the Archived filter to see the default list",
                trigger: ".o_search_options .o_filter_menu button",
            },
            {
                content: "Open the Archived filter toggle again",
                trigger: ".o_filter_menu .dropdown-item:contains(Archived)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "The record appears again in the default list",
                trigger: ".o_data_row:contains(TOUR-RRT-ACTIVATE)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});

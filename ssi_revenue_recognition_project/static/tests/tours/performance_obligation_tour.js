/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_revenue_recognition_project.performance_obligation_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/performance_obligation/05-approve.md (delta of
    // ssi_revenue_recognition_project -- Additional Post-Condition).
    // Navigation is scaffolded from the base module's own
    // "05-approve" tour Flow (ssi_revenue_recognition); the only
    // new assertion is the delta's Post-Condition: the Project
    // field is filled once the record reaches Open. It does not
    // open the linked project record or inspect any of its own
    // fields -- that is unit test territory.
    tour.register(
        "ssi_revenue_recognition_project_performance_obligation_approve",
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
                    ".o_data_row:contains(TOUR-POB-PROJECT-APPROVE) .o_data_cell:first",
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
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Base Flow 4 -- Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Base Post-Condition -- the single approval level is
            // fulfilled, so the record is auto-opened (action_open).
            {
                content: "Status is Open",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },

            // Delta Additional Post-Condition (docs/performance_obligation/
            // 05-approve.md) -- the Project tab (added by this
            // module) must be opened before its fields can be
            // inspected; notebook panes outside the active tab stay
            // hidden until clicked (patterns.md).
            {
                content: "Open the Project tab",
                trigger: ".o_notebook .nav-link:contains(Project)",
            },

            // Auto Create Project was checked on this record, so
            // opening the PoB also created a project.project record
            // and linked it through Project. Anchored on the known
            // fixture title -- also used as the created project's
            // own name (see _prepare_project_data) -- so the trigger
            // only matches once the field actually holds a value: an
            // empty readonly many2one collapses to a zero-size box
            // and jQuery's `:visible` never matches it (see the UI
            // test skill's patterns.md).
            {
                content: "Project field shows the auto-created project",
                trigger:
                    ".o_field_widget[name='project_id']:contains(TOUR-POB-PROJECT-APPROVE)",
                run: function () {
                    // Assertion only; do not open the linked
                    // project record.
                },
            },
        ]
    );
});

"""
CSS design system tokens and comprehensive dark theme styling for GenAI Video Intelligence Studio.
Eliminates text visibility issues, white-out hover/focus/active bugs, and enforces high-contrast
readability across all components, states, and interactive elements.
"""

STUDIO_CSS = """
:root {
    --primary: #6366F1;
    --primary-hover: #4F46E5;
    --secondary: #EC4899;
    --secondary-hover: #DB2777;
    --accent: #10B981;
    --bg-dark: #0B0F19;
    --card-bg: #131A2B;
    --card-border: #1E293B;
    --surface-elevated: #162036;
    --surface-hover: #1E293B;
    --surface-active: #312E81;
    --input-bg: #0F172A;
    --input-focus: #162036;
    --border-subtle: #1E293B;
    --border-interactive: #334155;
    --border-hover: #475569;
    --border-focus: #6366F1;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --text-dim: #64748B;
}

/* =========================================================================
   1. GLOBAL CONTAINER & BASE RESET
   ========================================================================= */
html, body, .gradio-container, .gradio-container.dark {
    background-color: var(--bg-dark) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--text-main) !important;
}

::selection {
    background-color: var(--primary) !important;
    color: #FFFFFF !important;
}

/* Header Banner */
.studio-header {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 16px !important;
    padding: 24px 32px !important;
    margin-bottom: 24px !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35) !important;
}

.division-badge-a {
    display: inline-block;
    background: linear-gradient(90deg, #3B82F6 0%, #6366F1 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 0.8px !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    text-transform: uppercase !important;
}

.division-badge-b {
    display: inline-block;
    background: linear-gradient(90deg, #EC4899 0%, #8B5CF6 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 0.8px !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    text-transform: uppercase !important;
}

/* KPI Cards */
.kpi-card {
    background: #131A2B !important;
    border: 1px solid #1E293B !important;
    border-radius: 12px !important;
    padding: 18px !important;
    text-align: center !important;
    transition: transform 0.2s ease, border-color 0.2s ease, background-color 0.2s ease !important;
}
.kpi-card:hover {
    transform: translateY(-2px) !important;
    border-color: #6366F1 !important;
    background: #162036 !important;
}

.kpi-number {
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #F8FAFC !important;
    margin-top: 4px !important;
}

.kpi-label {
    font-size: 12px !important;
    color: #94A3B8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
}

/* =========================================================================
   2. TABS & NAVIGATION (Zero White-Out on Hover / Select)
   ========================================================================= */
.tabs, div[role="tablist"], .tab-nav {
    background: #0B0F19 !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 6px !important;
    padding: 6px 4px !important;
}

button[role="tab"], .tab-nav button {
    background: #131A2B !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}

button[role="tab"]:hover, .tab-nav button:hover {
    background: var(--surface-hover) !important;
    color: #FFFFFF !important;
    border-color: var(--primary) !important;
}

button[role="tab"][aria-selected="true"],
button[role="tab"].selected,
.tab-nav button.selected,
.tab-nav button[aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--primary) !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3) !important;
}

.tabitem, div[role="tabpanel"] {
    background: transparent !important;
    padding-top: 16px !important;
}

/* =========================================================================
   3. BUTTONS (Primary, Secondary, Quick Actions)
   ========================================================================= */
/* Primary Buttons */
.action-btn-primary, button.primary {
    background: linear-gradient(90deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: 1px solid #6366F1 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.2s ease !important;
}

.action-btn-primary:hover, button.primary:hover {
    background: linear-gradient(90deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border-color: #818CF8 !important;
    box-shadow: 0 6px 18px rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-1px) !important;
}

.action-btn-primary:active, button.primary:active {
    background: #3730A3 !important;
    color: #FFFFFF !important;
    transform: translateY(0px) !important;
}

.action-btn-primary:focus, .action-btn-primary:focus-visible,
button.primary:focus, button.primary:focus-visible {
    outline: 2px solid #A5B4FC !important;
    outline-offset: 2px !important;
    color: #FFFFFF !important;
}

/* Secondary & Generic Buttons */
.action-btn-secondary, button.secondary, .secondary, button[variant="secondary"], button.sm, button.lg, .gr-button-secondary, button:not(.primary):not(.action-btn-primary) {
    background: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid var(--border-interactive) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.action-btn-secondary:hover, button.secondary:hover, .secondary:hover, button[variant="secondary"]:hover, button.sm:hover, button.lg:hover, .gr-button-secondary:hover, button:not(.primary):not(.action-btn-primary):hover {
    background: #334155 !important;
    color: #FFFFFF !important;
    border-color: var(--primary) !important;
    transform: translateY(-1px) !important;
}

.action-btn-secondary:active, button.secondary:active, .secondary:active, button[variant="secondary"]:active, button:not(.primary):not(.action-btn-primary):active {
    background: #1E293B !important;
    color: #FFFFFF !important;
    transform: translateY(0px) !important;
}

.action-btn-secondary:focus, button.secondary:focus, .secondary:focus, button[variant="secondary"]:focus, button:not(.primary):not(.action-btn-primary):focus {
    outline: 2px solid var(--primary) !important;
    outline-offset: 2px !important;
    color: #FFFFFF !important;
}

button:disabled, button[disabled] {
    opacity: 0.5 !important;
    cursor: not-allowed !important;
    background: #1E293B !important;
    color: var(--text-dim) !important;
}

/* =========================================================================
   4. INPUTS, TEXTAREAS & SEARCH BOXES
   ========================================================================= */
input[type="text"], input[type="number"], input[type="search"], textarea, .gr-input, .gr-text-input {
    background: var(--input-bg) !important;
    color: #F8FAFC !important;
    border: 1px solid var(--border-interactive) !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}

input[type="text"]:hover, input[type="number"]:hover, textarea:hover {
    background: #131C30 !important;
    border-color: var(--border-hover) !important;
    color: #FFFFFF !important;
}

input[type="text"]:focus, input[type="text"]:focus-visible,
input[type="number"]:focus, input[type="number"]:focus-visible,
textarea:focus, textarea:focus-visible {
    background: var(--input-focus) !important;
    border-color: var(--primary) !important;
    color: #FFFFFF !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
}

input::placeholder, textarea::placeholder {
    color: var(--text-dim) !important;
}

input:disabled, textarea:disabled, input[readonly], textarea[readonly] {
    background: #0B1120 !important;
    color: var(--text-muted) !important;
    border-color: var(--border-subtle) !important;
    cursor: not-allowed !important;
}

/* =========================================================================
   5. DROPDOWNS & SELECT MENUS (High-Contrast, Visible Items)
   ========================================================================= */
div[data-testid="dropdown"] .wrap,
.dropdown-item,
div[role="combobox"] {
    background: var(--input-bg) !important;
    border: 1px solid var(--border-interactive) !important;
    color: #F8FAFC !important;
    border-radius: 8px !important;
}

div[data-testid="dropdown"] .wrap:hover {
    background: #131C30 !important;
    border-color: var(--border-hover) !important;
    color: #FFFFFF !important;
}

div[data-testid="dropdown"] .wrap:focus-within {
    background: var(--input-focus) !important;
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
}

/* Dropdown Options Popup List */
ul.options,
div[role="listbox"],
.dropdown-options {
    background: #131A2B !important;
    border: 1px solid var(--border-interactive) !important;
    border-radius: 8px !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.75) !important;
    max-height: 280px !important;
    overflow-y: auto !important;
    z-index: 1000 !important;
}

/* Individual Option Items */
ul.options li,
div[role="option"],
.dropdown-options .item {
    background: #131A2B !important;
    color: #E2E8F0 !important;
    padding: 8px 12px !important;
    cursor: pointer !important;
    transition: background 0.15s ease, color 0.15s ease !important;
}

ul.options li:hover,
ul.options li.hovered,
div[role="option"]:hover,
.dropdown-options .item:hover {
    background: #1E293B !important;
    color: #FFFFFF !important;
}

ul.options li.selected,
ul.options li.active,
div[role="option"][aria-selected="true"],
.dropdown-options .item.selected {
    background: #312E81 !important;
    color: #A5B4FC !important;
    font-weight: 600 !important;
}

/* =========================================================================
   6. ACCORDIONS (No White Flashes)
   ========================================================================= */
.accordion, div.accordion-item {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
}

.label-wrap, button.label-wrap, .accordion-button {
    background: var(--card-bg) !important;
    color: #F8FAFC !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding: 12px 16px !important;
    font-weight: 600 !important;
    transition: background 0.2s ease !important;
}

.label-wrap:hover, button.label-wrap:hover {
    background: #1E293B !important;
    color: #FFFFFF !important;
}

.label-wrap:focus, button.label-wrap:focus {
    outline: none !important;
    background: #1E293B !important;
    color: #FFFFFF !important;
}

/* =========================================================================
   7. CHECKBOXES, RADIOS & SLIDERS
   ========================================================================= */
label.checkbox-label, .gr-checkbox label, span.label-text {
    color: #F8FAFC !important;
    cursor: pointer !important;
}

input[type="checkbox"], input[type="radio"] {
    background-color: var(--input-bg) !important;
    border: 1.5px solid var(--border-interactive) !important;
    border-radius: 4px !important;
    accent-color: var(--primary) !important;
    cursor: pointer !important;
}

input[type="checkbox"]:hover, input[type="radio"]:hover {
    border-color: var(--primary) !important;
}

input[type="checkbox"]:checked, input[type="radio"]:checked {
    background-color: var(--primary) !important;
    border-color: var(--primary) !important;
}

input[type="range"] {
    accent-color: var(--primary) !important;
}

/* =========================================================================
   8. TABLES & DATAFRAMES
   ========================================================================= */
table, .dataframe {
    background: var(--card-bg) !important;
    color: #F8FAFC !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
}

thead, thead th {
    background: #0F172A !important;
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding: 10px 14px !important;
}

tbody tr {
    background: #131A2B !important;
    color: #F8FAFC !important;
    transition: background 0.15s ease !important;
}

tbody tr:nth-child(even) {
    background: #0F172A !important;
}

tbody tr:hover {
    background: #1E293B !important;
    color: #FFFFFF !important;
}

tbody td {
    border-bottom: 1px solid var(--border-subtle) !important;
    color: #F8FAFC !important;
    padding: 10px 14px !important;
}

td:focus, td.focus, .cell.focus {
    background: #312E81 !important;
    color: #FFFFFF !important;
    outline: 2px solid var(--primary) !important;
}

/* =========================================================================
   9. CHATBOT COMPONENT
   ========================================================================= */
div[data-testid="chatbot"], .chatbot {
    background: #0F172A !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
}

.user, [data-testid="user"] {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border-radius: 12px 12px 2px 12px !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
}

.bot, [data-testid="bot"], .assistant {
    background: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid var(--border-interactive) !important;
    border-radius: 12px 12px 12px 2px !important;
}

/* =========================================================================
   10. FILE UPLOADS, CARDS & PANELS
   ========================================================================= */
div.block {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
}

div.block:hover {
    border-color: #334155 !important;
}

span[data-testid="block-info"], label span, .block-title, .label-wrap span {
    color: var(--text-muted) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Upload Container */
div[data-testid="file-upload"], .file-upload, .upload-container {
    background: #0F172A !important;
    border: 2px dashed var(--border-interactive) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}

div[data-testid="file-upload"]:hover, .upload-container:hover {
    background: #162036 !important;
    border-color: var(--primary) !important;
}
"""

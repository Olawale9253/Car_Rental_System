// ===== DOM Elements =====
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleSidebar');
const navItems = document.querySelectorAll('.sidebar-nav li');
const tabContents = document.querySelectorAll('.tab-content');
const pageTitle = document.getElementById('pageTitle');

// ===== Sidebar Toggle (Mobile) =====
toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
});

// ===== Tab Navigation =====
navItems.forEach(item => {
    item.addEventListener('click', function() {
        const tabId = this.dataset.tab;
        if (!tabId) return;

        // Update nav active state
        navItems.forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');

        // Update tab content
        tabContents.forEach(content => content.classList.remove('active'));
        const targetContent = document.getElementById(tabId);
        if (targetContent) {
            targetContent.classList.add('active');
            // Update page title
            pageTitle.textContent = this.querySelector('span')?.textContent || tabId;
        }

        // Close sidebar on mobile
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('open');
        }
    });
});

// ===== Quick Action: Open Tab =====
function openTab(tabId) {
    const navItem = document.querySelector(`.sidebar-nav li[data-tab="${tabId}"]`);
    if (navItem) {
        navItem.click();
    }
}

// ===== Search Bar Functionality =====
document.querySelectorAll('.table-search input, .search-bar input').forEach(input => {
    input.addEventListener('keyup', function(e) {
        const searchTerm = this.value.toLowerCase();
        const table = this.closest('.card')?.querySelector('.data-table tbody');
        
        if (table) {
            const rows = table.querySelectorAll('tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        }
    });
});

// ===== Action Button Alerts (Demo) =====
document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!this.closest('.tab-header')) return;
        const action = this.textContent.trim();
        alert(`🚀 "${action}" clicked! This would open a modal/form in production.`);
    });
});

// ===== Action Icon Alerts (Demo) =====
document.querySelectorAll('.action-icon').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const icon = this.querySelector('i');
        let action = icon?.className || 'action';
        
        // Determine action type
        if (action.includes('eye')) action = 'View';
        else if (action.includes('edit')) action = 'Edit';
        else if (action.includes('trash')) {
            if (confirm('⚠️ Are you sure you want to delete this item?')) {
                alert('🗑️ Item deleted (demo)');
                const row = this.closest('tr');
                if (row) row.style.opacity = '0.3';
            }
            return;
        } else if (action.includes('check')) action = 'Complete';
        else if (action.includes('print')) action = 'Print';
        else action = 'Action';
        
        alert(`🔧 ${action} clicked (demo)`);
    });
});

// ===== Status Badge Click =====
document.querySelectorAll('.status-badge').forEach(badge => {
    badge.addEventListener('click', function() {
        const status = this.textContent.trim();
        alert(`📊 Status: ${status} (click to change in production)`);
    });
});

// ===== Row Click Highlight =====
document.querySelectorAll('.data-table tbody tr').forEach(row => {
    row.addEventListener('click', function(e) {
        if (e.target.closest('.action-icon')) return;
        this.classList.toggle('selected');
    });
});

// Add selected row styles dynamically
const style = document.createElement('style');
style.textContent = `
    .data-table tbody tr.selected {
        background: var(--primary-light) !important;
    }
    .data-table tbody tr {
        cursor: pointer;
        transition: 0.15s;
    }
`;
document.head.appendChild(style);

// ===== Notification Bell Click =====
document.querySelector('.icon-btn .fa-bell')?.closest('.icon-btn')?.addEventListener('click', () => {
    alert('🔔 You have 3 new notifications');
});

// ===== Settings Icon Click =====
document.querySelector('.icon-btn .fa-cog')?.closest('.icon-btn')?.addEventListener('click', () => {
    alert('⚙️ Settings panel would open here');
});

// ===== Logout Button =====
document.querySelector('.logout-btn')?.addEventListener('click', () => {
    if (confirm('Are you sure you want to logout?')) {
        alert('👋 Logged out successfully (demo)');
    }
});

// ===== Quick Action Buttons (Dashboard) =====
document.querySelectorAll('.action-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const text = this.querySelector('span')?.textContent || 'Action';
        alert(`🚀 "${text}" form would open here`);
    });
});

// ===== Report Cards Click =====
document.querySelectorAll('.report-card .btn-outline').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const title = this.closest('.report-card')?.querySelector('h3')?.textContent || 'Report';
        alert(`📊 Generating "${title}"... (demo)`);
    });
});

// ===== Brand Card Edit Buttons =====
document.querySelectorAll('.brand-card .action-icon').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const brand = this.closest('.brand-header')?.querySelector('h3')?.textContent || 'Brand';
        alert(`✏️ Editing "${brand}" (demo)`);
    });
});

// ===== Add Brand/Model Buttons =====
document.querySelector('#brands .tab-header .btn-primary:first-child')?.addEventListener('click', () => {
    alert('🚗 "Add Brand" form would open here');
});

document.querySelector('#brands .tab-header .btn-primary:last-child')?.addEventListener('click', () => {
    alert('🚗 "Add Model" form would open here');
});

// ===== Export Buttons =====
document.querySelectorAll('.btn-outline .fa-download').forEach(icon => {
    icon.closest('.btn-outline')?.addEventListener('click', function(e) {
        e.stopPropagation();
        alert('📥 Exporting data... (demo)');
    });
});

// ===== Filter Buttons =====
document.querySelectorAll('.btn-outline .fa-filter').forEach(icon => {
    icon.closest('.btn-outline')?.addEventListener('click', function(e) {
        e.stopPropagation();
        alert('🔍 Filter panel would open here');
    });
});

// ===== Generate Report Button =====
document.querySelector('#reports .tab-header .btn-primary')?.addEventListener('click', () => {
    alert('📄 Report generation wizard would open here');
});

// ===== Keyboard Shortcuts (for power users) =====
document.addEventListener('keydown', (e) => {
    // Ctrl+1-7 to switch tabs
    if (e.ctrlKey && e.key >= '1' && e.key <= '7') {
        e.preventDefault();
        const tabs = ['dashboard', 'customers', 'cars', 'rentals', 'payments', 'brands', 'reports'];
        const index = parseInt(e.key) - 1;
        if (tabs[index]) {
            openTab(tabs[index]);
        }
    }
    // Escape to close sidebar
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
    }
    // Ctrl+/ to focus search
    if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-bar input');
        if (searchInput) searchInput.focus();
    }
});

// ===== Initialize: Default tab =====
// The first nav item is already active by default

console.log('🚗 CarRentalPro initialized!');
console.log('📌 Keyboard shortcuts: Ctrl+1-7 for tabs, Ctrl+/ for search, Escape to close sidebar');

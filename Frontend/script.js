const API_BASE_URL = 'http://127.0.0.1:8000/api';
const state = { cars: [], rentals: [], editingCarId: null, modalType: 'car' };
const carOptions = {
    brands: ['TOYOTA', 'HONDA', 'LEXUS', 'BMW'],
    models: ['CIVIC', 'COROLLA', 'CAMRY', 'RAV4', 'RX350'],
    years: [2010, 2011, 2012, 2013, 2014, 2015, 2016],
    statuses: ['AVAILABLE', 'RENTED', 'MAINTENANCE']
};

document.addEventListener('DOMContentLoaded', async () => {
    const session = readSession();
    if (!session) { window.location.href = 'login.html'; return; }
    renderUser(session);
    bindNavigation(); bindModal(); bindSearch(); bindLogout();
    await refreshData();
});

function readSession() {
    try { return JSON.parse(localStorage.getItem('carRentalSession') || 'null'); }
    catch { return null; }
}

function renderUser(session) {
    const name = session.name || session.email || 'Admin';
    document.getElementById('userName').textContent = name;
    document.getElementById('userRole').textContent = session.role || 'Admin';
    document.getElementById('userAvatar').textContent = name.split(' ').map(part => part[0]).join('').slice(0, 2).toUpperCase();
}

async function apiRequest(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options
    });
    if (!response.ok) {
        let message = 'The request could not be completed';
        try { message = (await response.json()).detail || message; } catch { /* Empty error response. */ }
        throw new Error(message);
    }
    return response.status === 204 ? null : response.json();
}

async function refreshData() {
    try {
        const [dashboard, cars, rentals] = await Promise.all([apiRequest('/dashboard'), apiRequest('/cars'), apiRequest('/rentals')]);
        state.cars = cars; state.rentals = rentals;
        renderDashboard(dashboard); renderCars(); renderRentals(); renderBrands();
    } catch (error) { showToast(error.message, 'error'); }
}

function renderDashboard(dashboard) {
    document.getElementById('availableCars').textContent = dashboard.available_cars;
    document.getElementById('activeRentals').textContent = dashboard.active_rentals;
    document.getElementById('totalFleet').textContent = dashboard.total_fleet;
    document.getElementById('monthlyRevenue').textContent = `$${Number(dashboard.revenue).toLocaleString()}`;
    document.getElementById('carsCount').textContent = state.cars.length;
    document.getElementById('rentalsCount').textContent = state.rentals.filter(rental => rental.is_active).length;
    document.getElementById('recentActivity').innerHTML = state.rentals.slice(-5).reverse().map(rental => `
        <div class="activity-item"><div class="activity-icon"><i class="fas fa-car"></i></div><div>
        <p class="activity-text">Rental for <strong>${escapeHtml(rental.customer_name)}</strong></p>
        <p class="activity-time">${formatDate(rental.rental_datetime)}</p></div></div>`).join('') || '<p class="empty-state">No rentals yet.</p>';
}

function renderCars() {
    const tableBody = document.getElementById('carsTableBody');
    tableBody.innerHTML = state.cars.map(car => `
        <tr><td><strong>${escapeHtml(car.plate_number)}</strong></td><td>${car.model}</td><td>${car.brand}</td>
        <td>${car.release_year}</td><td>$${Number(car.daily_price).toFixed(2)}</td><td><span class="status-badge ${car.car_state.toLowerCase()}">${car.car_state}</span></td>
        <td class="row-actions"><button class="action-icon" data-action="edit-car" data-id="${car.id}" title="Edit"><i class="fas fa-edit"></i></button>
        <button class="action-icon danger" data-action="delete-car" data-id="${car.id}" title="Delete"><i class="fas fa-trash"></i></button></td></tr>`).join('') || emptyRow(7, 'No cars have been added.');
    tableBody.querySelectorAll('[data-action="edit-car"]').forEach(button => button.addEventListener('click', () => openCarModal(button.dataset.id)));
    tableBody.querySelectorAll('[data-action="delete-car"]').forEach(button => button.addEventListener('click', () => deleteCar(button.dataset.id)));
}

function renderRentals() {
    const tableBody = document.getElementById('rentalsTableBody');
    tableBody.innerHTML = state.rentals.map(rental => {
        const car = state.cars.find(item => item.id === rental.car_id);
        const status = rental.is_active ? 'Active' : 'Completed';
        return `<tr><td><strong>#${rental.id.slice(0, 8)}</strong></td><td>${escapeHtml(rental.customer_name)}</td>
        <td>${car ? `${car.brand} ${car.model}` : 'Removed car'}</td><td>${formatDate(rental.rental_datetime)}</td>
        <td>${formatDate(rental.expected_return_date)}</td><td>$${Number(rental.price).toFixed(2)}</td>
        <td><span class="status-badge ${status.toLowerCase()}">${status}</span></td><td class="row-actions">
        ${rental.is_active ? `<button class="action-icon" data-action="complete-rental" data-id="${rental.id}" title="Complete"><i class="fas fa-check"></i></button>` : ''}
        <button class="action-icon danger" data-action="delete-rental" data-id="${rental.id}" title="Delete"><i class="fas fa-trash"></i></button></td></tr>`;
    }).join('') || emptyRow(8, 'No rentals have been created.');
    tableBody.querySelectorAll('[data-action="complete-rental"]').forEach(button => button.addEventListener('click', () => completeRental(button.dataset.id)));
    tableBody.querySelectorAll('[data-action="delete-rental"]').forEach(button => button.addEventListener('click', () => deleteRental(button.dataset.id)));
}

function renderBrands() {
    const grouped = state.cars.reduce((result, car) => { (result[car.brand] ||= []).push(car); return result; }, {});
    document.getElementById('brandsGrid').innerHTML = Object.entries(grouped).map(([brand, cars]) => `
        <div class="card brand-card"><div class="brand-header"><i class="fas fa-car brand-icon"></i><div><h3>${brand}</h3>
        <span class="model-count">${cars.length} vehicles</span></div></div><div class="brand-models">
        ${cars.map(car => `<span class="model-tag">${car.model} (${car.release_year})</span>`).join('')}</div></div>`).join('') || '<p class="empty-state">Brands appear when cars are added.</p>';
}

function bindNavigation() {
    const sidebar = document.getElementById('sidebar');
    document.getElementById('toggleSidebar').addEventListener('click', () => sidebar.classList.toggle('open'));
    document.querySelectorAll('.sidebar-nav li').forEach(item => item.addEventListener('click', () => {
        document.querySelectorAll('.sidebar-nav li').forEach(nav => nav.classList.remove('active')); item.classList.add('active');
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.getElementById(item.dataset.tab).classList.add('active'); document.getElementById('pageTitle').textContent = item.querySelector('span').textContent; sidebar.classList.remove('open');
    }));
    document.querySelectorAll('.action-btn').forEach(button => button.addEventListener('click', () => {
        const action = button.querySelector('span').textContent;
        if (action === 'Add Car') openCarModal(); else if (action === 'New Rental') openRentalModal(); else openTab(action === 'Manage Brands' ? 'brands' : 'reports');
    }));
    document.querySelector('#cars .tab-header .btn-primary').addEventListener('click', () => openCarModal());
    document.querySelector('#rentals .tab-header .btn-primary').addEventListener('click', () => openRentalModal());
}

function openTab(tabId) { document.querySelector(`.sidebar-nav li[data-tab="${tabId}"]`)?.click(); }

function bindSearch() {
    document.querySelectorAll('.table-search input, .search-bar input').forEach(input => input.addEventListener('input', () => {
        const term = input.value.toLowerCase(); const table = input.closest('.card')?.querySelector('tbody');
        table?.querySelectorAll('tr').forEach(row => { row.hidden = !row.textContent.toLowerCase().includes(term); });
    }));
}

function bindModal() {
    document.querySelectorAll('[data-close-modal]').forEach(button => button.addEventListener('click', closeModal));
    document.getElementById('modalBackdrop').addEventListener('click', event => { if (event.target.id === 'modalBackdrop') closeModal(); });
    document.getElementById('adminForm').addEventListener('submit', saveForm);
}

function setupSelect(name, values, selected = '') {
    const select = document.querySelector(`#adminForm [name="${name}"]`);
    select.innerHTML = values.map(value => {
        const option = typeof value === 'object' ? value : { value, label: value };
        return `<option value="${option.value}" ${String(option.value) === String(selected) ? 'selected' : ''}>${option.label}</option>`;
    }).join('');
}

function openCarModal(id = null) {
    state.modalType = 'car'; state.editingCarId = id; const car = state.cars.find(item => item.id === id);
    document.getElementById('modalTitle').textContent = car ? 'Edit car' : 'Add car'; document.getElementById('carFields').hidden = false; document.getElementById('rentalFields').hidden = true;
    setupSelect('brand', carOptions.brands, car?.brand); setupSelect('model', carOptions.models, car?.model); setupSelect('release_year', carOptions.years, car?.release_year); setupSelect('car_state', carOptions.statuses, car?.car_state || 'AVAILABLE');
    document.querySelector('[name="plate_number"]').value = car?.plate_number || '';
    document.querySelector('[name="daily_price"]').value = car?.daily_price || 0;
    setFieldsDisabled('carFields', false); setFieldsDisabled('rentalFields', true); showModal();
}

function openRentalModal() {
    const cars = state.cars.filter(car => car.car_state === 'AVAILABLE');
    if (!cars.length) { showToast('Add an available car before creating a rental.', 'error'); return; }
    state.modalType = 'rental'; state.editingCarId = null; document.getElementById('modalTitle').textContent = 'New rental'; document.getElementById('carFields').hidden = true; document.getElementById('rentalFields').hidden = false;
    setupSelect('car_id', cars.map(car => ({ value: car.id, label: `${car.plate_number} - ${car.brand} ${car.model}` })), cars[0].id);
    document.querySelectorAll('#rentalFields input').forEach(input => { input.value = ''; });
    setFieldsDisabled('carFields', true); setFieldsDisabled('rentalFields', false); showModal();
}

function setFieldsDisabled(sectionId, disabled) {
    document.querySelectorAll(`#${sectionId} input, #${sectionId} select`).forEach(field => { field.disabled = disabled; });
}

function showModal() { document.getElementById('formError').textContent = ''; document.getElementById('modalBackdrop').hidden = false; }
function closeModal() { document.getElementById('modalBackdrop').hidden = true; }

async function saveForm(event) {
    event.preventDefault(); const data = Object.fromEntries(new FormData(event.target).entries());
    try {
        if (state.modalType === 'car') await apiRequest(state.editingCarId ? `/cars/${state.editingCarId}` : '/cars', { method: state.editingCarId ? 'PUT' : 'POST', body: JSON.stringify(data) });
        else await apiRequest('/rentals', { method: 'POST', body: JSON.stringify(data) });
        closeModal(); await refreshData(); showToast('Changes saved.', 'success');
    } catch (error) { document.getElementById('formError').textContent = error.message; }
}

async function deleteCar(id) { if (confirm('Delete this car permanently?')) await performAction(`/cars/${id}`, 'DELETE', 'Car deleted.'); }
async function completeRental(id) { await performAction(`/rentals/${id}/complete`, 'PUT', 'Rental completed.'); }
async function deleteRental(id) { if (confirm('Delete this rental record?')) await performAction(`/rentals/${id}`, 'DELETE', 'Rental deleted.'); }
async function performAction(path, method, message) { try { await apiRequest(path, { method }); await refreshData(); showToast(message, 'success'); } catch (error) { showToast(error.message, 'error'); } }

function bindLogout() {
    document.querySelector('.logout-btn').addEventListener('click', async () => {
        if (!confirm('Are you sure you want to logout?')) return; const session = readSession();
        if (session?.email) await apiRequest(`/auth/logout?email=${encodeURIComponent(session.email)}`, { method: 'POST' }).catch(() => {});
        localStorage.removeItem('carRentalSession'); window.location.href = 'login.html';
    });
}

function emptyRow(columns, message) { return `<tr><td colspan="${columns}" class="empty-state">${message}</td></tr>`; }
function formatDate(value) { return value ? new Date(value).toLocaleDateString() : '-'; }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character])); }
function showToast(message, type = 'success') { const toast = document.createElement('div'); toast.className = `admin-toast ${type}`; toast.textContent = message; document.body.appendChild(toast); setTimeout(() => toast.remove(), 3500); }

document.addEventListener('keydown', event => { if (event.key === 'Escape') closeModal(); if (event.ctrlKey && event.key >= '1' && event.key <= '5') openTab(['dashboard', 'cars', 'rentals', 'brands', 'reports'][Number(event.key) - 1]); });

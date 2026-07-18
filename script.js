// Stock Market Tracker Application

const DEFAULT_SYMBOLS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'KPRMILL.NS'];
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000'
    : '/';

// Application State
const state = {
    watchlist: [],
    activityLog: []
};

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const searchResults = document.getElementById('searchResults');
const watchlistContainer = document.getElementById('watchlist');
const activityLog = document.getElementById('activity');
const clearWatchlistBtn = document.getElementById('clearWatchlist');
const toast = document.getElementById('toast');
const portfolioValue = document.getElementById('portfolioValue');
const totalGainLoss = document.getElementById('totalGainLoss');
const watchedCount = document.getElementById('watchedCount');
const topGainer = document.getElementById('topGainer');
const lastUpdate = document.getElementById('lastUpdate');

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    loadWatchlistFromStorage();
    if (state.watchlist.length === 0) {
        state.watchlist = DEFAULT_SYMBOLS.map(symbol => ({
            symbol,
            name: symbol,
            price: 0,
            change: 0,
            changePercent: 0
        }));
        saveWatchlistToStorage();
    }
    setupEventListeners();
    updateUI();
    updateTime();
    refreshWatchlist();
    setInterval(updateTime, 1000);
    setInterval(refreshWatchlist, 15000);
});

// Event Listeners
function setupEventListeners() {
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
    searchInput.addEventListener('input', handleSearchInput);
    clearWatchlistBtn.addEventListener('click', clearWatchlist);
    document.addEventListener('click', handleClickOutside);
}

// Search functionality
function handleSearchInput(e) {
    const query = e.target.value.trim().toUpperCase();
    
    if (!query) {
        searchResults.classList.add('hidden');
        return;
    }

    searchResults.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--text-secondary);">Searching live quotes…</div>';
    searchResults.classList.remove('hidden');

    fetchQuote(query)
        .then(stock => {
            if (!stock) {
                searchResults.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--text-secondary);">No live quote available for that symbol</div>';
                return;
            }

            searchResults.innerHTML = `
                <div class="search-result-item" onclick="addToWatchlist('${stock.symbol}')">
                    <div>
                        <span class="result-symbol">${stock.symbol}</span>
                        <span class="result-name">${stock.name}</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 600;">$${stock.price.toFixed(2)}</div>
                        <div class="${stock.change >= 0 ? 'change-positive' : 'change-negative'}">
                            ${stock.change >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%
                        </div>
                    </div>
                </div>
            `;
        })
        .catch(() => {
            searchResults.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--text-secondary);">Unable to load quote right now</div>';
        });
}

function handleSearch() {
    const query = searchInput.value.trim().toUpperCase();
    
    if (!query) {
        showToast('Please enter a stock symbol', 'warning');
        return;
    }

    fetchQuote(query)
        .then(stock => {
            if (!stock) {
                showToast(`Unable to fetch live quote for '${query}'`, 'error');
                return;
            }

            addToWatchlist(stock.symbol);
            searchInput.value = '';
            searchResults.classList.add('hidden');
        })
        .catch(() => {
            showToast(`Unable to fetch live quote for '${query}'`, 'error');
        });
}

function handleClickOutside(e) {
    if (!e.target.closest('.search-section')) {
        searchResults.classList.add('hidden');
    }
}

// Add stock to watchlist
function addToWatchlist(symbol) {
    const normalized = symbol.toUpperCase();
    if (state.watchlist.find(s => s.symbol === normalized)) {
        showToast(`${normalized} is already in your watchlist`, 'warning');
        return;
    }

    const placeholder = { symbol: normalized, name: normalized, price: 0, change: 0, changePercent: 0 };
    state.watchlist.push(placeholder);
    addActivity(`Added ${normalized} to watchlist`, 'positive');
    showToast(`${normalized} added to watchlist`, 'success');
    saveWatchlistToStorage();
    refreshWatchlist();
}

// Remove stock from watchlist
function removeFromWatchlist(symbol) {
    state.watchlist = state.watchlist.filter(s => s.symbol !== symbol);
    addActivity(`Removed ${symbol} from watchlist`, 'negative');
    showToast(`${symbol} removed from watchlist`, 'success');
    updateUI();
    saveWatchlistToStorage();
}

// Clear entire watchlist
function clearWatchlist() {
    if (state.watchlist.length === 0) {
        showToast('Watchlist is already empty', 'warning');
        return;
    }

    if (confirm('Are you sure you want to clear your entire watchlist?')) {
        state.watchlist = [];
        addActivity('Cleared entire watchlist', 'negative');
        showToast('Watchlist cleared', 'success');
        updateUI();
        saveWatchlistToStorage();
    }
}

// Fetch live quotes for the active watchlist
async function refreshWatchlist() {
    if (state.watchlist.length === 0) {
        updateUI();
        return;
    }

    const refreshed = [];
    for (const stock of state.watchlist) {
        const quote = await fetchQuote(stock.symbol);
        refreshed.push(quote ? { ...stock, ...quote } : stock);
    }

    state.watchlist = refreshed;
    saveWatchlistToStorage();
    updateUI();
}

async function fetchQuote(symbol) {
    const response = await fetch(`${API_BASE_URL}/quote?symbol=${encodeURIComponent(symbol)}`);
    const payload = await response.json();
    if (!payload.ok) {
        return null;
    }
    return payload.quote;
}

// Render watchlist
function renderWatchlist() {
    if (state.watchlist.length === 0) {
        watchlistContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <p>No stocks in watchlist. Search and add stocks to track them.</p>
            </div>
        `;
        return;
    }

    watchlistContainer.innerHTML = state.watchlist.map(stock => `
        <div class="stock-card">
            <div class="stock-info">
                <div class="stock-symbol">${stock.symbol}</div>
                <div class="stock-name">${stock.name}</div>
            </div>
            <div class="stock-price-section">
                <div class="stock-price">$${stock.price.toFixed(2)}</div>
                <div class="stock-change ${stock.change >= 0 ? 'change-positive' : 'change-negative'}">
                    <i class="fas fa-arrow-${stock.change >= 0 ? 'up' : 'down'}"></i>
                    ${stock.change >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%
                </div>
            </div>
            <div class="stock-actions">
                <button class="btn-action" onclick="viewDetails('${stock.symbol}')">
                    <i class="fas fa-chart-bar"></i> Chart
                </button>
                <button class="btn-action btn-remove" onclick="removeFromWatchlist('${stock.symbol}')">
                    <i class="fas fa-trash-alt"></i> Remove
                </button>
            </div>
        </div>
    `).join('');
}

// Update statistics
function updateStats() {
    const totalValue = state.watchlist.reduce((sum, stock) => sum + stock.price, 0);
    const totalGain = state.watchlist.reduce((sum, stock) => sum + stock.change, 0);
    const topStock = state.watchlist.length > 0
        ? state.watchlist.reduce((max, stock) => stock.changePercent > max.changePercent ? stock : max)
        : null;

    portfolioValue.textContent = `$${totalValue.toFixed(2)}`;
    totalGainLoss.textContent = `${totalGain >= 0 ? '+' : ''}$${totalGain.toFixed(2)}`;
    totalGainLoss.style.color = totalGain >= 0 ? 'var(--success-color)' : 'var(--danger-color)';
    watchedCount.textContent = state.watchlist.length;
    topGainer.textContent = topStock ? `${topStock.symbol} (${topStock.changePercent.toFixed(2)}%)` : '--';
}

// Add activity
function addActivity(message, type) {
    state.activityLog.unshift({
        message,
        type,
        timestamp: new Date(),
        value: message
    });

    // Keep only last 20 activities
    if (state.activityLog.length > 20) {
        state.activityLog.pop();
    }

    renderActivityLog();
}

// Render activity log
function renderActivityLog() {
    if (state.activityLog.length === 0) {
        activityLog.innerHTML = `
            <div class="empty-state">
                <p>No recent activity</p>
            </div>
        `;
        return;
    }

    activityLog.innerHTML = state.activityLog.map(activity => `
        <div class="activity-item ${activity.type}">
            <div class="activity-text">
                <div class="activity-message">${activity.message}</div>
                <div class="activity-time">${formatTime(activity.timestamp)}</div>
            </div>
            <div class="activity-value" style="color: ${activity.type === 'positive' ? 'var(--success-color)' : 'var(--danger-color)'}">
                ${activity.type === 'positive' ? '✓' : '✕'}
            </div>
        </div>
    `).join('');
}

// View stock details
function viewDetails(symbol) {
    const stock = state.watchlist.find(s => s.symbol === symbol);
    if (stock) {
        alert(`${stock.symbol} - ${stock.name}\n\nPrice: $${stock.price.toFixed(2)}\nChange: ${stock.change >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%\n\nLive data is refreshed from Yahoo Finance.`);
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Update UI
function updateUI() {
    renderWatchlist();
    renderActivityLog();
    updateStats();
}

// Update time display
function updateTime() {
    const now = new Date();
    lastUpdate.textContent = `Last updated: ${now.toLocaleTimeString()}`;
}

// Format time
function formatTime(date) {
    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (seconds < 60) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
}

// Local Storage Management
function saveWatchlistToStorage() {
    localStorage.setItem('stockWatchlist', JSON.stringify(state.watchlist));
}

function loadWatchlistFromStorage() {
    const saved = localStorage.getItem('stockWatchlist');
    if (saved) {
        state.watchlist = JSON.parse(saved);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === '/') {
        searchInput.focus();
        e.preventDefault();
    }
});

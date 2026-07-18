// Stock Market Tracker Application

// Mock stock data - Replace with real API calls
const mockStocks = {
    'AAPL': { symbol: 'AAPL', name: 'Apple Inc.', price: 189.45, change: 2.35, changePercent: 1.25 },
    'GOOGL': { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 142.80, change: -1.20, changePercent: -0.84 },
    'MSFT': { symbol: 'MSFT', name: 'Microsoft Corporation', price: 378.91, change: 5.45, changePercent: 1.46 },
    'AMZN': { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 182.50, change: 3.75, changePercent: 2.10 },
    'TSLA': { symbol: 'TSLA', name: 'Tesla Inc.', price: 242.84, change: -8.20, changePercent: -3.27 },
    'META': { symbol: 'META', name: 'Meta Platforms Inc.', price: 498.75, change: 12.45, changePercent: 2.56 },
    'NVDA': { symbol: 'NVDA', name: 'NVIDIA Corporation', price: 875.20, change: 25.30, changePercent: 2.97 },
    'NFLX': { symbol: 'NFLX', name: 'Netflix Inc.', price: 456.78, change: -5.12, changePercent: -1.11 },
};

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
    setupEventListeners();
    updateUI();
    updateTime();
    setInterval(updateTime, 1000);
    setInterval(simulatePriceUpdate, 5000); // Update prices every 5 seconds
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

    const filtered = Object.values(mockStocks).filter(stock =>
        stock.symbol.includes(query) || stock.name.toUpperCase().includes(query)
    );

    if (filtered.length === 0) {
        searchResults.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--text-secondary);">No stocks found</div>';
    } else {
        searchResults.innerHTML = filtered.map(stock => `
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
        `).join('');
    }

    searchResults.classList.remove('hidden');
}

function handleSearch() {
    const query = searchInput.value.trim().toUpperCase();
    
    if (!query) {
        showToast('Please enter a stock symbol', 'warning');
        return;
    }

    if (mockStocks[query]) {
        addToWatchlist(query);
        searchInput.value = '';
        searchResults.classList.add('hidden');
    } else {
        showToast(`Stock '${query}' not found`, 'error');
    }
}

function handleClickOutside(e) {
    if (!e.target.closest('.search-section')) {
        searchResults.classList.add('hidden');
    }
}

// Add stock to watchlist
function addToWatchlist(symbol) {
    if (state.watchlist.find(s => s.symbol === symbol)) {
        showToast(`${symbol} is already in your watchlist`, 'warning');
        return;
    }

    const stock = mockStocks[symbol];
    if (stock) {
        state.watchlist.push({ ...stock });
        addActivity(`Added ${symbol} to watchlist`, 'positive');
        showToast(`${symbol} added to watchlist`, 'success');
        updateUI();
        saveWatchlistToStorage();
    }
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

// Simulate price updates
function simulatePriceUpdate() {
    state.watchlist.forEach(stock => {
        const changeAmount = (Math.random() - 0.5) * 2; // Random change between -1 and 1
        stock.change = parseFloat((stock.change + changeAmount).toFixed(2));
        stock.changePercent = parseFloat((stock.change / stock.price * 100).toFixed(2));
        stock.price = parseFloat((stock.price + changeAmount).toFixed(2));
    });
    renderWatchlist();
    updateStats();
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
        alert(`${stock.symbol} - ${stock.name}\n\nPrice: $${stock.price.toFixed(2)}\nChange: ${stock.change >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%\n\nNote: Full charting feature coming soon!`);
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

// Stock Market Tracker Application

const DEFAULT_SYMBOLS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'KPRMILL.NS'];
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000'
    : '/';

// Application State
const state = {
    watchlist: [],
    activityLog: [],
    portfolio: {
        cash: 10000, // Starting cash balance
        holdings: {}, // Symbol -> { shares, avgCost }
        transactions: [], // Transaction history
        valueHistory: [] // Portfolio value over time
    },
    alerts: {}, // Symbol -> { above: price, below: price }
    triggeredAlerts: [], // History of triggered alerts
    dailySummary: null // Last daily summary
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
    loadPortfolioFromStorage();
    loadAlertsFromStorage();
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
    updatePortfolioUI();
    updateTime();
    refreshWatchlist();
    setInterval(updateTime, 1000);
    setInterval(refreshWatchlist, 15000);
    setInterval(trackPortfolioValue, 60000); // Track portfolio value every minute
    setInterval(checkAlerts, 30000); // Check alerts every 30 seconds
    setInterval(generateDailySummary, 86400000); // Daily summary every 24 hours
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

    watchlistContainer.innerHTML = state.watchlist.map(stock => {
        const holding = state.portfolio.holdings[stock.symbol];
        const shares = holding ? holding.shares : 0;
        
        return `
        <div class="stock-card">
            <div class="stock-info">
                <div class="stock-symbol">${stock.symbol}</div>
                <div class="stock-name">${stock.name}</div>
                ${shares > 0 ? `<div class="stock-holding">Owned: ${shares} shares</div>` : ''}
            </div>
            <div class="stock-price-section">
                <div class="stock-price">$${stock.price.toFixed(2)}</div>
                <div class="stock-change ${stock.change >= 0 ? 'change-positive' : 'change-negative'}">
                    <i class="fas fa-arrow-${stock.change >= 0 ? 'up' : 'down'}"></i>
                    ${stock.change >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%
                </div>
            </div>
            <div class="stock-actions">
                <button class="btn-action btn-buy" onclick="openTradeModal('${stock.symbol}', 'buy')">
                    <i class="fas fa-plus"></i> Buy
                </button>
                ${shares > 0 ? `
                <button class="btn-action btn-sell" onclick="openTradeModal('${stock.symbol}', 'sell')">
                    <i class="fas fa-minus"></i> Sell
                </button>
                ` : ''}
                <button class="btn-action" onclick="openAlertModal('${stock.symbol}')">
                    <i class="fas fa-bell"></i> Alert
                </button>
                <button class="btn-action" onclick="viewDetails('${stock.symbol}')">
                    <i class="fas fa-chart-bar"></i> Chart
                </button>
                <button class="btn-action btn-remove" onclick="removeFromWatchlist('${stock.symbol}')">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        </div>
    `}).join('');
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
        openChartModal(symbol);
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

function savePortfolioToStorage() {
    localStorage.setItem('stockPortfolio', JSON.stringify(state.portfolio));
}

function loadPortfolioFromStorage() {
    const saved = localStorage.getItem('stockPortfolio');
    if (saved) {
        state.portfolio = JSON.parse(saved);
    }
}

function saveAlertsToStorage() {
    localStorage.setItem('stockAlerts', JSON.stringify(state.alerts));
}

function loadAlertsFromStorage() {
    const saved = localStorage.getItem('stockAlerts');
    if (saved) {
        state.alerts = JSON.parse(saved);
    }
}

// Portfolio Functions
function calculatePortfolioValue() {
    let holdingsValue = 0;
    for (const symbol in state.portfolio.holdings) {
        const holding = state.portfolio.holdings[symbol];
        const stock = state.watchlist.find(s => s.symbol === symbol);
        if (stock && holding.shares > 0) {
            holdingsValue += stock.price * holding.shares;
        }
    }
    return state.portfolio.cash + holdingsValue;
}

function trackPortfolioValue() {
    const value = calculatePortfolioValue();
    state.portfolio.valueHistory.push({
        timestamp: Date.now(),
        value: value
    });
    // Keep only last 30 days of history
    const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
    state.portfolio.valueHistory = state.portfolio.valueHistory.filter(h => h.timestamp > thirtyDaysAgo);
    savePortfolioToStorage();
}

function buyStock(symbol, shares) {
    const stock = state.watchlist.find(s => s.symbol === symbol);
    if (!stock) {
        showToast('Stock not found in watchlist', 'error');
        return false;
    }

    const cost = stock.price * shares;
    if (cost > state.portfolio.cash) {
        showToast('Insufficient funds', 'error');
        return false;
    }

    // Update cash
    state.portfolio.cash -= cost;

    // Update holdings
    if (!state.portfolio.holdings[symbol]) {
        state.portfolio.holdings[symbol] = { shares: 0, avgCost: 0 };
    }

    const holding = state.portfolio.holdings[symbol];
    const totalShares = holding.shares + shares;
    const totalCost = (holding.shares * holding.avgCost) + cost;
    holding.avgCost = totalCost / totalShares;
    holding.shares = totalShares;

    // Record transaction
    state.portfolio.transactions.push({
        type: 'BUY',
        symbol,
        shares,
        price: stock.price,
        total: cost,
        timestamp: Date.now()
    });

    addActivity(`Bought ${shares} shares of ${symbol} at $${stock.price.toFixed(2)}`, 'positive');
    savePortfolioToStorage();
    updatePortfolioUI();
    return true;
}

function sellStock(symbol, shares) {
    const stock = state.watchlist.find(s => s.symbol === symbol);
    if (!stock) {
        showToast('Stock not found in watchlist', 'error');
        return false;
    }

    const holding = state.portfolio.holdings[symbol];
    if (!holding || holding.shares < shares) {
        showToast('Insufficient shares', 'error');
        return false;
    }

    const proceeds = stock.price * shares;

    // Update cash
    state.portfolio.cash += proceeds;

    // Update holdings
    holding.shares -= shares;
    if (holding.shares === 0) {
        delete state.portfolio.holdings[symbol];
    }

    // Record transaction
    state.portfolio.transactions.push({
        type: 'SELL',
        symbol,
        shares,
        price: stock.price,
        total: proceeds,
        timestamp: Date.now()
    });

    addActivity(`Sold ${shares} shares of ${symbol} at $${stock.price.toFixed(2)}`, 'negative');
    savePortfolioToStorage();
    updatePortfolioUI();
    return true;
}

// Alert Functions
function setAlert(symbol, above, below) {
    if (!above && !below) {
        delete state.alerts[symbol];
    } else {
        state.alerts[symbol] = { above: above || null, below: below || null };
    }
    saveAlertsToStorage();
}

function checkAlerts() {
    for (const symbol in state.alerts) {
        const alert = state.alerts[symbol];
        const stock = state.watchlist.find(s => s.symbol === symbol);
        
        if (!stock) continue;
        
        let triggered = false;
        let message = '';
        
        if (alert.above && stock.price >= alert.above) {
            message = `${symbol} reached $${stock.price.toFixed(2)} (above threshold $${alert.above.toFixed(2)})`;
            triggered = true;
        }
        
        if (alert.below && stock.price <= alert.below) {
            message = `${symbol} dropped to $${stock.price.toFixed(2)} (below threshold $${alert.below.toFixed(2)})`;
            triggered = true;
        }
        
        if (triggered) {
            state.triggeredAlerts.push({
                symbol,
                price: stock.price,
                alert,
                timestamp: Date.now(),
                message
            });
            
            // Keep only last 50 triggered alerts
            if (state.triggeredAlerts.length > 50) {
                state.triggeredAlerts.shift();
            }
            
            showToast(message, 'warning');
            addActivity(`Alert triggered: ${message}`, 'warning');
        }
    }
}

function generateDailySummary() {
    const portfolioValue = calculatePortfolioValue();
    const initialCash = 10000;
    const totalReturn = portfolioValue - initialCash;
    const returnPercent = (totalReturn / initialCash * 100);
    
    const holdingsSummary = Object.entries(state.portfolio.holdings).map(([symbol, holding]) => {
        const stock = state.watchlist.find(s => s.symbol === symbol);
        if (!stock) return null;
        const currentValue = stock.price * holding.shares;
        const costBasis = holding.shares * holding.avgCost;
        const gain = currentValue - costBasis;
        const gainPercent = (gain / costBasis * 100);
        
        return {
            symbol,
            shares: holding.shares,
            avgCost: holding.avgCost,
            currentPrice: stock.price,
            currentValue,
            gain,
            gainPercent
        };
    }).filter(Boolean);
    
    state.dailySummary = {
        date: new Date().toISOString(),
        portfolioValue,
        totalReturn,
        returnPercent,
        holdings: holdingsSummary,
        cash: state.portfolio.cash
    };
    
    // Show summary notification
    const summaryMessage = `Daily Summary: Portfolio $${portfolioValue.toFixed(2)} (${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%)`;
    showToast(summaryMessage, returnPercent >= 0 ? 'success' : 'warning');
    addActivity(summaryMessage, returnPercent >= 0 ? 'positive' : 'negative');
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === '/') {
        searchInput.focus();
        e.preventDefault();
    }
    if (e.key === 'Escape') {
        closeChartModal();
        closeTradeModal();
        closeAlertModal();
    }
});

// Alert Modal Functions
let currentAlertSymbol = null;

function openAlertModal(symbol) {
    currentAlertSymbol = symbol;
    
    const stock = state.watchlist.find(s => s.symbol === symbol);
    if (!stock) return;
    
    document.getElementById('alertTitle').textContent = `Set Alert for ${symbol}`;
    document.getElementById('alertSymbol').textContent = symbol;
    document.getElementById('alertCurrentPrice').textContent = `$${stock.price.toFixed(2)}`;
    
    // Pre-fill existing alert values
    const existingAlert = state.alerts[symbol];
    document.getElementById('alertAbove').value = existingAlert?.above || '';
    document.getElementById('alertBelow').value = existingAlert?.below || '';
    
    document.getElementById('alertModal').classList.remove('hidden');
    document.getElementById('alertModal').classList.add('show');
}

function closeAlertModal() {
    document.getElementById('alertModal').classList.remove('show');
    document.getElementById('alertModal').classList.add('hidden');
    currentAlertSymbol = null;
}

function saveAlert() {
    const above = parseFloat(document.getElementById('alertAbove').value) || null;
    const below = parseFloat(document.getElementById('alertBelow').value) || null;
    
    if (!above && !below) {
        showToast('Please set at least one alert threshold', 'warning');
        return;
    }
    
    setAlert(currentAlertSymbol, above, below);
    showToast(`Alert set for ${currentAlertSymbol}`, 'success');
    addActivity(`Set alert for ${currentAlertSymbol}: above $${above || 'N/A'}, below $${below || 'N/A'}`, 'positive');
    closeAlertModal();
}

function clearAlert() {
    setAlert(currentAlertSymbol, null, null);
    showToast(`Alert cleared for ${currentAlertSymbol}`, 'success');
    addActivity(`Cleared alert for ${currentAlertSymbol}`, 'negative');
    closeAlertModal();
}

// Trade Modal Functions
let currentTradeSymbol = null;
let currentTradeType = null;

function openTradeModal(symbol, type) {
    currentTradeSymbol = symbol;
    currentTradeType = type;
    
    const stock = state.watchlist.find(s => s.symbol === symbol);
    if (!stock) return;
    
    document.getElementById('tradeTitle').textContent = type === 'buy' ? `Buy ${symbol}` : `Sell ${symbol}`;
    document.getElementById('tradeSymbol').textContent = symbol;
    document.getElementById('tradePrice').textContent = `$${stock.price.toFixed(2)}`;
    document.getElementById('tradeCash').textContent = `$${state.portfolio.cash.toFixed(2)}`;
    document.getElementById('tradeShares').value = 1;
    
    const holding = state.portfolio.holdings[symbol];
    if (type === 'sell' && holding) {
        document.getElementById('tradeShares').max = holding.shares;
    } else {
        document.getElementById('tradeShares').removeAttribute('max');
    }
    
    updateTradeTotal();
    
    document.getElementById('tradeModal').classList.remove('hidden');
    document.getElementById('tradeModal').classList.add('show');
}

function closeTradeModal() {
    document.getElementById('tradeModal').classList.remove('show');
    document.getElementById('tradeModal').classList.add('hidden');
    currentTradeSymbol = null;
    currentTradeType = null;
}

function updateTradeTotal() {
    const shares = parseInt(document.getElementById('tradeShares').value) || 0;
    const stock = state.watchlist.find(s => s.symbol === currentTradeSymbol);
    if (stock) {
        const total = stock.price * shares;
        document.getElementById('tradeTotal').textContent = `$${total.toFixed(2)}`;
    }
}

function executeTrade() {
    const shares = parseInt(document.getElementById('tradeShares').value) || 0;
    if (shares <= 0) {
        showToast('Please enter a valid number of shares', 'error');
        return;
    }
    
    if (currentTradeType === 'buy') {
        if (buyStock(currentTradeSymbol, shares)) {
            closeTradeModal();
        }
    } else if (currentTradeType === 'sell') {
        if (sellStock(currentTradeSymbol, shares)) {
            closeTradeModal();
        }
    }
}

// Portfolio UI Functions
function updatePortfolioUI() {
    const portfolioValue = calculatePortfolioValue();
    const initialCash = 10000; // Starting cash
    const totalReturn = portfolioValue - initialCash;
    const returnPercent = (totalReturn / initialCash * 100);
    
    // Update portfolio stats in the main UI
    portfolioValue.textContent = `$${portfolioValue.toFixed(2)}`;
    totalGainLoss.textContent = `${totalReturn >= 0 ? '+' : ''}$${totalReturn.toFixed(2)} (${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%)`;
    totalGainLoss.style.color = totalReturn >= 0 ? 'var(--success-color)' : 'var(--danger-color)';
    
    // Update portfolio chart
    renderPortfolioChart();
}

function renderPortfolioChart() {
    const container = document.getElementById('portfolioChart');
    if (!container) return;
    
    const history = state.portfolio.valueHistory;
    if (history.length < 2) {
        container.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: var(--text-secondary);">
                <p>Portfolio performance chart will appear after tracking data is collected</p>
            </div>
        `;
        return;
    }
    
    const timestamps = history.map(h => new Date(h.timestamp));
    const values = history.map(h => h.value);
    
    const trace = {
        x: timestamps,
        y: values,
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        name: 'Portfolio Value',
        line: { color: '#3b82f6', width: 2 }
    };
    
    const layout = {
        title: '',
        xaxis: {
            type: 'date',
            gridcolor: '#334155',
            showgrid: true,
            showticklabels: true
        },
        yaxis: {
            title: 'Portfolio Value ($)',
            gridcolor: '#334155',
            showgrid: true
        },
        plot_bgcolor: 'transparent',
        paper_bgcolor: 'transparent',
        font: { color: '#f1f5f9' },
        margin: { l: 60, r: 20, t: 20, b: 40 },
        showlegend: false,
        hovermode: 'x unified'
    };
    
    const config = {
        responsive: true,
        displayModeBar: false,
        displaylogo: false
    };
    
    Plotly.newPlot(container, [trace], layout, config);
}

function openPortfolioChart() {
    // For now, just scroll to the portfolio chart section
    document.getElementById('portfolioChart').scrollIntoView({ behavior: 'smooth' });
}

// Chart Modal Functions
let currentChartSymbol = null;

function openChartModal(symbol) {
    currentChartSymbol = symbol;
    const stock = state.watchlist.find(s => s.symbol === symbol);
    if (stock) {
        document.getElementById('chartTitle').textContent = `${stock.symbol} - ${stock.name}`;
    }
    document.getElementById('chartModal').classList.remove('hidden');
    document.getElementById('chartModal').classList.add('show');
    updateChart();
}

function closeChartModal() {
    document.getElementById('chartModal').classList.remove('show');
    document.getElementById('chartModal').classList.add('hidden');
    currentChartSymbol = null;
}

async function updateChart() {
    if (!currentChartSymbol) return;

    const timeRange = document.getElementById('timeRange').value;
    const interval = document.getElementById('interval').value;
    const showMA = document.getElementById('showMA').checked;
    const showVolume = document.getElementById('showVolume').checked;

    document.getElementById('chartLoading').classList.remove('hidden');
    document.getElementById('chartContainer').innerHTML = '';

    try {
        const response = await fetch(`${API_BASE_URL}/historical?symbol=${encodeURIComponent(currentChartSymbol)}&interval=${interval}&range=${timeRange}`);
        const payload = await response.json();
        
        if (!payload.ok) {
            throw new Error(payload.error);
        }

        const data = payload.data;
        renderCandlestickChart(data, showMA, showVolume);
    } catch (error) {
        document.getElementById('chartContainer').innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: var(--text-secondary);">
                <p>Unable to load chart data: ${error.message}</p>
            </div>
        `;
    } finally {
        document.getElementById('chartLoading').classList.add('hidden');
    }
}

function calculateMovingAverages(data, periods = [20, 50]) {
    const closePrices = data.map(d => d.close);
    const mas = {};
    
    periods.forEach(period => {
        mas[period] = [];
        for (let i = 0; i < closePrices.length; i++) {
            if (i < period - 1) {
                mas[period].push(null);
            } else {
                const sum = closePrices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                mas[period].push(sum / period);
            }
        }
    });
    
    return mas;
}

function renderCandlestickChart(data, showMA, showVolume) {
    const timestamps = data.map(d => new Date(d.timestamp * 1000));
    const opens = data.map(d => d.open);
    const highs = data.map(d => d.high);
    const lows = data.map(d => d.low);
    const closes = data.map(d => d.close);
    const volumes = data.map(d => d.volume);

    const traces = [];

    // Candlestick trace
    const candlestick = {
        x: timestamps,
        open: opens,
        high: highs,
        low: lows,
        close: closes,
        type: 'candlestick',
        name: 'Price',
        increasing: { line: { color: '#10b981' } },
        decreasing: { line: { color: '#ef4444' } },
        xaxis: 'x',
        yaxis: 'y'
    };
    traces.push(candlestick);

    // Moving averages
    if (showMA) {
        const mas = calculateMovingAverages(data, [20, 50]);
        
        if (mas[20]) {
            traces.push({
                x: timestamps,
                y: mas[20],
                type: 'scatter',
                mode: 'lines',
                name: 'MA 20',
                line: { color: '#3b82f6', width: 1.5 },
                xaxis: 'x',
                yaxis: 'y'
            });
        }
        
        if (mas[50]) {
            traces.push({
                x: timestamps,
                y: mas[50],
                type: 'scatter',
                mode: 'lines',
                name: 'MA 50',
                line: { color: '#f59e0b', width: 1.5 },
                xaxis: 'x',
                yaxis: 'y'
            });
        }
    }

    // Volume
    if (showVolume) {
        const colors = closes.map((close, i) => {
            if (i === 0) return '#10b981';
            return close >= opens[i] ? '#10b981' : '#ef4444';
        });

        traces.push({
            x: timestamps,
            y: volumes,
            type: 'bar',
            name: 'Volume',
            marker: { color: colors },
            xaxis: 'x',
            yaxis: 'y2',
            opacity: 0.7
        });
    }

    const layout = {
        title: '',
        xaxis: {
            rangeslider: { visible: false },
            type: 'date',
            gridcolor: '#334155',
            showgrid: true
        },
        yaxis: {
            title: 'Price',
            gridcolor: '#334155',
            showgrid: true,
            side: 'left'
        },
        yaxis2: {
            title: 'Volume',
            overlaying: 'y',
            side: 'right',
            showgrid: false,
            visible: showVolume
        },
        plot_bgcolor: '#1e293b',
        paper_bgcolor: '#1e293b',
        font: { color: '#f1f5f9' },
        margin: { l: 60, r: 60, t: 30, b: 60 },
        legend: {
            x: 0,
            y: 1,
            bgcolor: 'rgba(30, 41, 59, 0.8)',
            bordercolor: '#334155',
            borderwidth: 1
        },
        dragmode: 'zoom',
        showlegend: true
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['lasso2d', 'select2d'],
        displaylogo: false
    };

    Plotly.newPlot('chartContainer', traces, layout, config);
}

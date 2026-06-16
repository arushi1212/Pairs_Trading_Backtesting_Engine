import matplotlib.pyplot as plt

def plot_results(spread, z_score, signals, cumulative_pnl, pair_name):
    rolling_max = cumulative_pnl.cummax()
    drawdown = cumulative_pnl - rolling_max

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle(f'Pairs Trading: {pair_name}', fontsize=14)

    # Subplot 1 - Equity Curve
    axes[0].plot(cumulative_pnl.index, cumulative_pnl, color='green', linewidth=2)
    axes[0].axhline(0, color='black', linestyle='--', alpha=0.5)
    axes[0].set_ylabel('Cumulative PnL')
    axes[0].grid(True, linestyle=':', alpha=0.6)

    # Subplot 2 - Drawdown
    axes[1].fill_between(drawdown.index, drawdown, 0, color='crimson', alpha=0.3, label='Drawdown')
    axes[1].plot(drawdown.index, drawdown, color='crimson', linewidth=1, alpha=0.7)
    axes[1].axhline(0, color='black', linestyle='-', alpha=0.3)
    axes[1].set_ylabel('Drawdown Value')
    axes[1].set_xlabel('Date')
    axes[1].grid(True, linestyle=':', alpha=0.5)

    # Suplot 3 - Z-score
    # Plot the continuous Z-score line
    axes[2].plot(z_score.index, z_score, color='orange', label='Z-Score', alpha=0.8)
    
    # Draw horizontal rule bands for thresholds
    axes[2].axhline(2, color='red', linestyle='--', alpha=0.7, label='Short Threshold (+2)')
    axes[2].axhline(-2, color='green', linestyle='--', alpha=0.7, label='Buy Threshold (-2)')
    axes[2].axhline(0.5, color='gray', linestyle=':', alpha=0.5)
    axes[2].axhline(-0.5, color='gray', linestyle=':', alpha=0.5, label='Exit Band (±0.5)')
    
    # Highlight positions: Shade green when Long (1) and red when Short (-1)
    axes[2].fill_between(signals.index, -3, 3, where=(signals == 1), color='green', alpha=0.1, label='Long State')
    axes[2].fill_between(signals.index, -3, 3, where=(signals == -1), color='red', alpha=0.1, label='Short State')
    
    axes[2].set_ylabel('Z-Score')
    axes[2].set_ylim(-4, 4)
    axes[2].grid(True, linestyle=':', alpha=0.5)
    axes[2].legend(loc='upper left', ncol=2, fontsize='small')

    plt.tight_layout()
    plt.show()


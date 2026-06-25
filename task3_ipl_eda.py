import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Load Data ──────────────────────────────────────────────────────────────
df = pd.read_csv('ipl_matches.csv')

print("=" * 50)
print("       IPL EDA – Dataset Summary")
print("=" * 50)
print(f"Total Matches  : {len(df)}")
print(f"Seasons        : {df['season'].min()} – {df['season'].max()}")
print(f"Teams          : {df['team1'].nunique()}")
print(f"Venues         : {df['venue'].nunique()}")
print(f"\nMost Wins      : {df['winner'].value_counts().idxmax()}")
print(f"Top PoM Player : {df['player_of_match'].value_counts().idxmax()}")

# ── Theme Setup ────────────────────────────────────────────────────────────
sns.set_theme(style='darkgrid')
BG      = '#0d1117'
AX_BG   = '#161b22'
TEXT    = 'white'
GRID    = '#30363d'

plt.rcParams.update({
    'text.color': TEXT, 'axes.labelcolor': TEXT,
    'xtick.color': TEXT, 'ytick.color': TEXT,
    'axes.titlecolor': TEXT, 'figure.facecolor': BG
})

ipl_colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd',
              '#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']

fig = plt.figure(figsize=(22, 24))
fig.patch.set_facecolor(BG)

def style(ax, title, xlabel='', ylabel=''):
    ax.set_facecolor(AX_BG)
    ax.set_title(title, fontsize=13, fontweight='bold', color=TEXT, pad=12)
    ax.set_xlabel(xlabel, fontsize=10, color=TEXT)
    ax.set_ylabel(ylabel, fontsize=10, color=TEXT)
    ax.grid(color=GRID, linestyle='--', linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('#444')

# ── Chart 1: Most Winning Teams (All Time) ────────────────────────────────
ax1 = fig.add_subplot(4, 2, 1)
wins = df['winner'].value_counts()
bars = ax1.barh(wins.index[::-1], wins.values[::-1], color=ipl_colors)
style(ax1, '🏆 Most Winning Teams (All Time)', 'Number of Wins')
for bar, val in zip(bars[::-1], wins.values):
    ax1.text(val + 1, bar.get_y() + bar.get_height()/2,
             str(val), va='center', color=TEXT, fontsize=9)

# ── Chart 2: Season-wise Total Matches ────────────────────────────────────
ax2 = fig.add_subplot(4, 2, 2)
season_matches = df.groupby('season').size()
ax2.bar(season_matches.index, season_matches.values,
        color=sns.color_palette('viridis', len(season_matches)))
style(ax2, '📅 Season-wise Total Matches', 'Season', 'Matches')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# ── Chart 3: Wins Per Team Per Season (Stacked) ───────────────────────────
ax3 = fig.add_subplot(4, 2, (3, 4))
top6 = wins.head(6).index.tolist()
season_team = df[df['winner'].isin(top6)].groupby(['season','winner']).size().unstack(fill_value=0)
season_team[top6].plot(kind='bar', stacked=True, ax=ax3,
                       color=ipl_colors[:6], width=0.8)
style(ax3, '📊 Season-wise Wins – Top 6 Teams', 'Season', 'Wins')
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
leg = ax3.legend(loc='upper right', facecolor=AX_BG, edgecolor='#555',
                 labelcolor=TEXT, fontsize=8)

# ── Chart 4: Top Player of the Match Winners ──────────────────────────────
ax4 = fig.add_subplot(4, 2, 5)
top_pom = df['player_of_match'].value_counts().head(10)
ax4.barh(top_pom.index[::-1], top_pom.values[::-1],
         color=sns.color_palette('magma', 10))
style(ax4, '🌟 Top 10 Player of the Match Winners', 'Awards')
for i, val in enumerate(top_pom.values[::-1]):
    ax4.text(val + 0.2, i, str(val), va='center', color=TEXT, fontsize=9)

# ── Chart 5: Toss Decision Analysis ──────────────────────────────────────
ax5 = fig.add_subplot(4, 2, 6)
toss = df['toss_decision'].value_counts()
wedges, texts, autotexts = ax5.pie(
    toss.values, labels=toss.index, autopct='%1.1f%%',
    colors=['#4fc3f7','#ff8a65'], startangle=90,
    textprops={'color': TEXT, 'fontsize': 11})
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight('bold')
ax5.set_facecolor(AX_BG)
ax5.set_title('🏏 Toss Decision – Bat vs Field', fontsize=13,
              fontweight='bold', color=TEXT, pad=12)

# ── Chart 6: Toss Winner = Match Winner Analysis ──────────────────────────
ax6 = fig.add_subplot(4, 2, 7)
df['toss_match_win'] = df['toss_winner'] == df['winner']
toss_win_rate = df['toss_match_win'].value_counts()
labels = ['Toss Winner\nWon Match', 'Toss Winner\nLost Match']
ax6.bar(labels, toss_win_rate.values,
        color=['#66bb6a','#ef5350'], width=0.4)
style(ax6, '🎯 Does Winning Toss = Winning Match?', ylabel='Count')
for i, val in enumerate(toss_win_rate.values):
    ax6.text(i, val + 2, str(val), ha='center', color=TEXT, fontsize=11, fontweight='bold')

# ── Chart 7: Top Venues by Matches Hosted ────────────────────────────────
ax7 = fig.add_subplot(4, 2, 8)
venue_counts = df['venue'].value_counts().head(8)
short_names = [v.replace(' Stadium','').replace(' Cricket','')[:25]
               for v in venue_counts.index]
ax7.barh(short_names[::-1], venue_counts.values[::-1],
         color=sns.color_palette('coolwarm', 8))
style(ax7, '🏟️ Top Venues by Matches Hosted', 'Matches Hosted')
for i, val in enumerate(venue_counts.values[::-1]):
    ax7.text(val + 0.5, i, str(val), va='center', color=TEXT, fontsize=9)

# ── Final ──────────────────────────────────────────────────────────────────
fig.suptitle('🏏 IPL Exploratory Data Analysis Dashboard (2008–2023)',
             fontsize=18, fontweight='bold', color=TEXT, y=0.998)
plt.tight_layout(rect=[0, 0, 1, 0.998])
plt.savefig('ipl_eda_analysis.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("\n✅ IPL EDA Chart saved successfully!")

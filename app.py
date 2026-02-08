import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os
import io

# ==========================================
# 1. 設定 & フォント読み込み
# ==========================================
st.set_page_config(
    page_title="米国主要小売業 財務分析ダッシュボード",
    layout="wide",
    page_icon="🇺🇸"
)

def setup_font():
    """
    fontsフォルダから日本語フォントを読み込む。
    Cloud環境とローカル環境の両方に対応。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "fonts", "ipaexg.ttf")
    
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = prop.get_name()
        return prop.get_name()
    else:
        # フォールバック
        default_fonts = ['Meiryo', 'Yu Gothic', 'Hiragino Sans', 'TakaoGothic', 'IPAGothic']
        plt.rcParams['font.family'] = default_fonts
        return 'sans-serif'

font_name = setup_font()
sns.set_theme(style="whitegrid", rc={"font.family": font_name})

# ==========================================
# 2. カラーパレット定義（app_compare.pyと統一）
# ==========================================
COLORS = {
    'primary': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#95C623', '#5C4D7D'],
    'accent': '#FF6B6B',
    'background': '#F8F9FA',
    'text': '#2C3E50'
}

def get_company_colors(companies):
    """企業ごとに一貫した色を割り当て"""
    return {company: COLORS['primary'][i % len(COLORS['primary'])] for i, company in enumerate(companies)}

# ==========================================
# 3. ユーティリティ関数
# ==========================================
def format_fy(year):
    """年度をFYフォーマットに変換"""
    try:
        return f"FY{int(year)}"
    except:
        return year

def safe_divide(numerator, denominator, default=0):
    """ゼロ除算を回避する除算"""
    return np.where(denominator != 0, numerator / denominator, default)

def get_html_report(df, title, fig=None):
    """HTMLダウンロード用データの生成（テーブル＋チャート）"""
    import base64
    from io import BytesIO
    
    # チャートをbase64エンコード
    chart_html = ""
    if fig is not None:
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        chart_html = f'<div style="text-align:center; margin: 20px 0;"><img src="data:image/png;base64,{img_base64}" style="max-width:100%;"/></div>'
    
    return f"""
    <html><head><meta charset='utf-8'>
    <style>
        body {{ font-family: 'Hiragino Sans', 'Meiryo', sans-serif; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; background: white; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: right; }}
        th {{ background: linear-gradient(135deg, #2E86AB, #A23B72); color: white; text-align: center; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        tr:hover {{ background-color: #f0f0f0; }}
        h2 {{ color: #2C3E50; border-left: 5px solid #2E86AB; padding-left: 15px; margin-top: 0; }}
        .timestamp {{ color: #888; font-size: 12px; text-align: right; margin-top: 20px; }}
    </style></head>
    <body>
    <div class="container">
        <h2>{title}</h2>
        {chart_html}
        <h3>📋 詳細データ</h3>
        {df.to_html(classes='data-table')}
        <p class="timestamp">生成日時: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    </body></html>
    """

# ==========================================
# 4. カテゴリグループ定義
# ==========================================
CATEGORY_GROUPS = {
    'スーパー/BigBox': [
        'Walmart', 'Target', 'Kroger', 'Costco', 'Albertsons', 
        'PriceSmart', "BJ's Wholesale", 'Sprouts Farmers Market', 
        'Ingles Markets', 'Weis Markets'
    ],
    'ドラッグストア/医薬卸': [
        'CVS Health', 'McKesson', 'Cencora', 'Cardinal Health'
    ],
    'ホームセンター': [
        'Home Depot', "Lowe's", 'Floor & Decor'
    ],
    'Eコマース': [
        'Amazon', 'eBay', 'Etsy'
    ],
    'カスタム': []
}

# ==========================================
# 5. データ読み込み & 前処理
# ==========================================
@st.cache_data
def load_data():
    """Excelデータを読み込む"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "data", "financial_data_us.xlsx")
    
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_excel(file_path)
    return df

# ==========================================
# 6. メイン UI
# ==========================================
st.title("🇺🇸 米国主要小売業 財務分析ダッシュボード")

# カスタムCSS（app_compare.pyと同様）
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f0f2f6; 
        border-radius: 8px 8px 0 0; 
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #2E86AB; 
        color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

df_raw = load_data()

# ==========================================
# 7. サイドバー設定
# ==========================================
if df_raw is None:
    st.error("""
    ⚠️ データファイルが見つかりません。
    
    以下の手順でデータを配置してください：
    1. `data/` フォルダを作成
    2. `financial_data_us.xlsx` を配置
    """)
    st.stop()

st.sidebar.header("🔧 分析条件")

# --- 通貨単位選択 ---
unit_option = st.sidebar.radio(
    "表示通貨単位",
    ["10億ドル ($B)", "百万ドル ($M)"],
    index=0
)

if unit_option == "10億ドル ($B)":
    unit_scale = 1_000_000_000
    unit_label = "10億ドル"
else:
    unit_scale = 1_000_000
    unit_label = "百万ドル"

st.sidebar.markdown("---")

# --- 業態カテゴリ選択 ---
st.sidebar.subheader("1️⃣ 業態を選択")
available_companies = sorted(df_raw['企業名'].unique().tolist())

selected_category_group = st.sidebar.radio(
    "カテゴリ",
    list(CATEGORY_GROUPS.keys())
)

# --- 企業選択 ---
st.sidebar.subheader("2️⃣ 企業を選択")

if selected_category_group == 'カスタム':
    options = available_companies
    default_selection = options[:3] if len(options) >= 3 else options
else:
    target_list = CATEGORY_GROUPS[selected_category_group]
    options = [c for c in target_list if c in available_companies]
    default_selection = options

selected_companies = st.sidebar.multiselect(
    "比較対象企業",
    options,
    default=default_selection
)

if not selected_companies:
    st.warning("⚠️ 少なくとも1社選択してください。")
    st.stop()

# --- 年度選択 ---
st.sidebar.markdown("---")
st.sidebar.subheader("3️⃣ 決算年度")

all_years = sorted(df_raw['決算年度'].unique())
selected_year = st.sidebar.selectbox(
    "比較基準年度",
    all_years,
    index=len(all_years) - 1
)

# --- トレンド分析オプション ---
show_trend = st.sidebar.checkbox("📈 過去トレンドを表示", value=True)

# データフィルタリング
df_compare = df_raw[
    (df_raw['企業名'].isin(selected_companies)) & 
    (df_raw['決算年度'] == selected_year)
].copy()

# トレンド用データ（過去5年）
if show_trend:
    trend_years = [y for y in range(selected_year - 4, selected_year + 1) if y in all_years]
    df_trend = df_raw[
        (df_raw['企業名'].isin(selected_companies)) & 
        (df_raw['決算年度'].isin(trend_years))
    ].copy()
else:
    df_trend = pd.DataFrame()

# 企業ごとの色を設定
company_colors = get_company_colors(selected_companies)

# ==========================================
# 8. メインコンテンツ（タブ）
# ==========================================
st.markdown(f"**カテゴリ:** {selected_category_group} | **基準年度:** {format_fy(selected_year)} | **表示単位:** {unit_option}")

# タブ作成
tab_pl, tab_bs, tab_metrics, tab_cf, tab_prod = st.tabs([
    "💰 損益計算書", 
    "📊 貸借対照表", 
    "📈 財務指標", 
    "💵 キャッシュフロー",
    "👥 労働生産性"
])

# ---------------------------------------------------------
# Tab 1: 損益計算書
# ---------------------------------------------------------
with tab_pl:
    st.subheader(f"損益計算書の比較 - {format_fy(selected_year)}")
    
    if df_compare.empty:
        st.warning(f"{format_fy(selected_year)}年度のデータがありません。")
    else:
        df_display = df_compare.sort_values('売上高', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### 📊 売上構成（積み上げ）")
            plot_data = df_display[['企業名', '売上原価', '販管費', '営業利益']].set_index('企業名')
            plot_data = plot_data / unit_scale
            
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            plot_data.plot(
                kind='bar', 
                stacked=True, 
                ax=ax1, 
                color=['#A9A9A9', '#87CEEB', '#FF8C00']
            )
            ax1.set_ylabel(f"金額 ({unit_label})")
            ax1.set_xlabel("")
            ax1.legend(["売上原価", "販管費", "営業利益"], loc='upper right')
            ax1.set_title(f'{format_fy(selected_year)} 売上構成', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig1)
        
        with col2:
            st.markdown("##### 📈 営業利益率比較")
            fig2, ax2 = plt.subplots(figsize=(5, 6))
            colors_list = [company_colors[c] for c in df_display['企業名']]
            sns.barplot(
                data=df_display, 
                y='企業名', 
                x='営業利益率', 
                ax=ax2, 
                palette=colors_list
            )
            ax2.set_xlabel("営業利益率 (%)")
            ax2.set_ylabel("")
            ax2.grid(axis='x', linestyle='--', alpha=0.7)
            ax2.set_title('営業利益率', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig2)
        
        # データテーブル
        st.markdown("---")
        st.markdown("##### 📋 詳細データ")
        
        table_data = df_display[[
            '企業名', '売上高', '売上原価', '販管費', '営業利益', 
            '売上総利益率', '営業利益率', '販管費率'
        ]].copy()
        
        # 金額を単位変換
        for col in ['売上高', '売上原価', '販管費', '営業利益']:
            table_data[col] = table_data[col] / unit_scale
        
        table_data = table_data.set_index('企業名')
        st.dataframe(
            table_data.style.format({
                '売上高': '{:,.1f}',
                '売上原価': '{:,.1f}',
                '販管費': '{:,.1f}',
                '営業利益': '{:,.1f}',
                '売上総利益率': '{:.1f}%',
                '営業利益率': '{:.1f}%',
                '販管費率': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # HTMLダウンロード
        html_content = get_html_report(table_data, f"損益計算書比較 - {format_fy(selected_year)}", fig1)
        st.download_button(
            "📥 HTMLでダウンロード（チャート＋テーブル）", 
            html_content, 
            "pl_comparison.html", 
            "text/html",
            key="pl_dl"
        )

# ---------------------------------------------------------
# Tab 2: 貸借対照表
# ---------------------------------------------------------
with tab_bs:
    st.subheader(f"貸借対照表の比較 - {format_fy(selected_year)}")
    
    if df_compare.empty:
        st.warning(f"{format_fy(selected_year)}年度のデータがありません。")
    else:
        df_display = df_compare.sort_values('総資産', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 総資産規模")
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            colors_list = [company_colors[c] for c in df_display['企業名']]
            ax3.bar(
                df_display['企業名'], 
                df_display['総資産'] / unit_scale,
                color=colors_list
            )
            ax3.set_ylabel(f"総資産 ({unit_label})")
            ax3.set_title('総資産比較', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig3)
        
        with col2:
            st.markdown("##### 💼 自己資本比率")
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            sns.barplot(
                data=df_display,
                x='企業名',
                y='自己資本比率',
                palette=colors_list,
                ax=ax4
            )
            ax4.set_ylabel("自己資本比率 (%)")
            ax4.set_xlabel("")
            ax4.set_title('自己資本比率', fontweight='bold')
            ax4.axhline(y=50, color='red', linestyle='--', linewidth=1, alpha=0.7, label='50%基準線')
            ax4.legend()
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig4)
        
        # データテーブル
        st.markdown("---")
        st.markdown("##### 📋 詳細データ")
        
        table_data = df_display[[
            '企業名', '総資産', '流動資産', '棚卸資産', 
            '純資産', '有利子負債', '自己資本比率'
        ]].copy()
        
        # 金額を単位変換
        for col in ['総資産', '流動資産', '棚卸資産', '純資産', '有利子負債']:
            if col in table_data.columns:
                table_data[col] = table_data[col] / unit_scale
        
        table_data = table_data.set_index('企業名')
        st.dataframe(
            table_data.style.format({
                '総資産': '{:,.1f}',
                '流動資産': '{:,.1f}',
                '棚卸資産': '{:,.1f}',
                '純資産': '{:,.1f}',
                '有利子負債': '{:,.1f}',
                '自己資本比率': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # HTMLダウンロード
        html_content = get_html_report(table_data, f"貸借対照表比較 - {format_fy(selected_year)}", fig3)
        st.download_button(
            "📥 HTMLでダウンロード（チャート＋テーブル）", 
            html_content, 
            "bs_comparison.html", 
            "text/html",
            key="bs_dl"
        )

# ---------------------------------------------------------
# Tab 3: 財務指標
# ---------------------------------------------------------
with tab_metrics:
    st.subheader(f"財務指標の比較 - {format_fy(selected_year)}")
    
    if df_compare.empty:
        st.warning(f"{format_fy(selected_year)}年度のデータがありません。")
    else:
        df_display = df_compare.copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📦 在庫効率 vs 収益性")
            fig5, ax5 = plt.subplots(figsize=(8, 6))
            
            for company in df_display['企業名']:
                company_data = df_display[df_display['企業名'] == company]
                ax5.scatter(
                    company_data['棚卸資産回転率'],
                    company_data['営業利益率'],
                    s=200,
                    color=company_colors[company],
                    label=company,
                    alpha=0.7
                )
                # ラベル追加
                ax5.text(
                    company_data['棚卸資産回転率'].values[0],
                    company_data['営業利益率'].values[0] + 0.3,
                    company,
                    fontsize=9,
                    ha='center'
                )
            
            ax5.set_xlabel("棚卸資産回転率 (回)")
            ax5.set_ylabel("営業利益率 (%)")
            ax5.set_title('在庫効率と収益性', fontweight='bold')
            ax5.grid(True, linestyle=':', alpha=0.7)
            plt.tight_layout()
            st.pyplot(fig5)
        
        with col2:
            st.markdown("##### 🔄 総資産回転率")
            fig6, ax6 = plt.subplots(figsize=(8, 6))
            colors_list = [company_colors[c] for c in df_display['企業名']]
            ax6.barh(
                df_display['企業名'],
                df_display['総資産回転率'],
                color=colors_list
            )
            ax6.set_xlabel("総資産回転率 (回)")
            ax6.set_title('総資産回転率', fontweight='bold')
            ax6.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            st.pyplot(fig6)
        
        # データテーブル
        st.markdown("---")
        st.markdown("##### 📋 詳細データ")
        
        table_data = df_display[[
            '企業名', '営業利益率', '売上総利益率', '販管費率',
            '棚卸資産回転率', '総資産回転率', '自己資本比率'
        ]].copy()
        
        table_data = table_data.set_index('企業名')
        st.dataframe(
            table_data.style.format({
                '営業利益率': '{:.1f}%',
                '売上総利益率': '{:.1f}%',
                '販管費率': '{:.1f}%',
                '棚卸資産回転率': '{:.2f}',
                '総資産回転率': '{:.2f}',
                '自己資本比率': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # HTMLダウンロード
        html_content = get_html_report(table_data, f"財務指標比較 - {format_fy(selected_year)}", fig5)
        st.download_button(
            "📥 HTMLでダウンロード（チャート＋テーブル）", 
            html_content, 
            "metrics_comparison.html", 
            "text/html",
            key="metrics_dl"
        )

# ---------------------------------------------------------
# Tab 4: キャッシュフロー
# ---------------------------------------------------------
with tab_cf:
    st.subheader(f"キャッシュフローの比較 - {format_fy(selected_year)}")
    
    if df_compare.empty:
        st.warning(f"{format_fy(selected_year)}年度のデータがありません。")
    else:
        df_display = df_compare.copy()
        
        # CF項目の確認
        cf_columns = ['営業CF', '投資CF', 'フリーCF']
        available_cf = [col for col in cf_columns if col in df_display.columns]
        
        if not available_cf:
            st.info("キャッシュフローデータが利用できません。")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 💵 営業キャッシュフロー")
                fig7, ax7 = plt.subplots(figsize=(10, 6))
                cf_colors = ['#2E86AB' if v >= 0 else '#C73E1D' 
                            for v in df_display['営業CF']]
                ax7.bar(
                    df_display['企業名'],
                    df_display['営業CF'] / unit_scale,
                    color=cf_colors
                )
                ax7.axhline(y=0, color='black', linewidth=0.5)
                ax7.set_ylabel(f"営業CF ({unit_label})")
                ax7.set_title('営業キャッシュフロー', fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig7)
            
            with col2:
                st.markdown("##### 💰 フリーキャッシュフロー")
                fig8, ax8 = plt.subplots(figsize=(10, 6))
                free_colors = ['#95C623' if v >= 0 else '#C73E1D' 
                              for v in df_display['フリーCF']]
                ax8.bar(
                    df_display['企業名'],
                    df_display['フリーCF'] / unit_scale,
                    color=free_colors
                )
                ax8.axhline(y=0, color='black', linewidth=0.5)
                ax8.set_ylabel(f"フリーCF ({unit_label})")
                ax8.set_title('フリーキャッシュフロー', fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig8)
            
            # CF比較チャート
            st.markdown("---")
            st.markdown("##### 📊 キャッシュフロー構成比較")
            
            fig9, ax9 = plt.subplots(figsize=(12, 5))
            x = np.arange(len(df_display))
            width = 0.25
            
            ax9.bar(x - width, df_display['営業CF'] / unit_scale, 
                   width, label='営業CF', color='#2E86AB')
            ax9.bar(x, df_display['投資CF'] / unit_scale, 
                   width, label='投資CF', color='#F18F01')
            ax9.bar(x + width, df_display['フリーCF'] / unit_scale, 
                   width, label='フリーCF', color='#95C623')
            
            ax9.axhline(y=0, color='black', linewidth=0.5)
            ax9.set_xticks(x)
            ax9.set_xticklabels(df_display['企業名'], rotation=45, ha='right')
            ax9.legend()
            ax9.set_ylabel(f'金額 ({unit_label})')
            ax9.set_title('キャッシュフロー比較', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig9)
            
            # データテーブル
            st.markdown("---")
            st.markdown("##### 📋 詳細データ")
            
            table_columns = ['企業名'] + available_cf
            table_data = df_display[table_columns].copy()
            
            # 金額を単位変換
            for col in available_cf:
                table_data[col] = table_data[col] / unit_scale
            
            table_data = table_data.set_index('企業名')
            st.dataframe(
                table_data.style.format('{:,.1f}'),
                use_container_width=True
            )
            
            # HTMLダウンロード
            html_content = get_html_report(table_data, f"キャッシュフロー比較 - {format_fy(selected_year)}", fig9)
            st.download_button(
                "📥 HTMLでダウンロード（チャート＋テーブル）", 
                html_content, 
                "cf_comparison.html", 
                "text/html",
                key="cf_dl"
            )

# ---------------------------------------------------------
# Tab 5: 労働生産性
# ---------------------------------------------------------
with tab_prod:
    st.subheader(f"労働生産性の比較 - {format_fy(selected_year)}")
    
    if df_compare.empty:
        st.warning(f"{format_fy(selected_year)}年度のデータがありません。")
    else:
        df_display = df_compare.copy()
        
        # 生産性指標の確認
        has_productivity = '全従業員1人当り売上高' in df_display.columns
        
        if not has_productivity:
            # データにない場合は計算
            df_display['全従業員1人当り売上高'] = safe_divide(
                df_display['売上高'], 
                df_display['従業員数']
            ) / 1000  # 千ドル単位
            
            df_display['全従業員1人当り営業利益'] = safe_divide(
                df_display['営業利益'], 
                df_display['従業員数']
            ) / 1000  # 千ドル単位
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 👥 従業員1人当り売上高")
            fig10, ax10 = plt.subplots(figsize=(10, 6))
            colors_list = [company_colors[c] for c in df_display['企業名']]
            ax10.bar(
                df_display['企業名'],
                df_display['全従業員1人当り売上高'],
                color=colors_list
            )
            ax10.set_ylabel("売上高 (千ドル / 人)")
            ax10.set_title('従業員1人当り売上高', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig10)
        
        with col2:
            st.markdown("##### 💼 従業員1人当り営業利益")
            fig11, ax11 = plt.subplots(figsize=(10, 6))
            ax11.bar(
                df_display['企業名'],
                df_display['全従業員1人当り営業利益'],
                color='#F18F01'
            )
            ax11.set_ylabel("営業利益 (千ドル / 人)")
            ax11.set_title('従業員1人当り営業利益', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig11)
        
        # データテーブル
        st.markdown("---")
        st.markdown("##### 📋 詳細データ")
        
        table_data = df_display[[
            '企業名', '従業員数', 
            '全従業員1人当り売上高', '全従業員1人当り営業利益'
        ]].copy()
        
        table_data = table_data.set_index('企業名')
        st.dataframe(
            table_data.style.format({
                '従業員数': '{:,.0f}',
                '全従業員1人当り売上高': '{:.1f}',
                '全従業員1人当り営業利益': '{:.1f}'
            }),
            use_container_width=True
        )
        
        st.caption("※「従業員1人当り」指標の単位は千ドルです。")
        
        # HTMLダウンロード
        html_content = get_html_report(table_data, f"労働生産性比較 - {format_fy(selected_year)}", fig10)
        st.download_button(
            "📥 HTMLでダウンロード（チャート＋テーブル）", 
            html_content, 
            "productivity_comparison.html", 
            "text/html",
            key="prod_dl"
        )

# ---------------------------------------------------------
# トレンド分析（オプション）
# ---------------------------------------------------------
if show_trend and not df_trend.empty:
    st.divider()
    st.subheader(f"📈 過去トレンド分析 ({format_fy(min(trend_years))}〜{format_fy(max(trend_years))})")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 売上高推移")
        fig_trend1, ax_trend1 = plt.subplots(figsize=(10, 6))
        
        for company in selected_companies:
            company_trend = df_trend[df_trend['企業名'] == company].sort_values('決算年度')
            if not company_trend.empty:
                ax_trend1.plot(
                    company_trend['決算年度'].apply(format_fy),
                    company_trend['売上高'] / unit_scale,
                    marker='o',
                    label=company,
                    color=company_colors[company],
                    linewidth=2
                )
        
        ax_trend1.set_ylabel(f'売上高 ({unit_label})')
        ax_trend1.set_title('売上高推移', fontweight='bold')
        ax_trend1.legend(loc='best', fontsize=9)
        ax_trend1.grid(True, linestyle=':', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig_trend1)
    
    with col2:
        st.markdown("##### 営業利益率推移")
        fig_trend2, ax_trend2 = plt.subplots(figsize=(10, 6))
        
        for company in selected_companies:
            company_trend = df_trend[df_trend['企業名'] == company].sort_values('決算年度')
            if not company_trend.empty:
                ax_trend2.plot(
                    company_trend['決算年度'].apply(format_fy),
                    company_trend['営業利益率'],
                    marker='s',
                    label=company,
                    color=company_colors[company],
                    linewidth=2
                )
        
        ax_trend2.set_ylabel('営業利益率 (%)')
        ax_trend2.set_title('営業利益率推移', fontweight='bold')
        ax_trend2.legend(loc='best', fontsize=9)
        ax_trend2.grid(True, linestyle=':', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig_trend2)

# ---------------------------------------------------------
# フッター
# ---------------------------------------------------------
st.divider()
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
    🇺🇸 米国主要小売業 財務分析ダッシュボード | Powered by Streamlit
</div>
""", unsafe_allow_html=True)

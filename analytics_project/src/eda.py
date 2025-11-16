from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def run_basic_eda(csv_path, output_dir=None):
    p = Path(csv_path)
    # try utf-8 first, fall back to latin-1
    try:
        df = pd.read_csv(p)
    except Exception:
        df = pd.read_csv(p, encoding='latin-1')

    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
    else:
        out = None

    # simple plots
    plt.figure(figsize=(10, 6))
    sns.countplot(y=df['category'].fillna('Unknown'), order=df['category'].value_counts().index[:20])
    plt.title('Top categories (by count in dataset)')
    plt.tight_layout()
    if out:
        plt.savefig(out / 'top_categories.png')
    else:
        plt.show()
    plt.close()

    # subscribers distribution (numeric)
    if 'subscribers' in df.columns:
        df_sub = pd.to_numeric(df['subscribers'], errors='coerce')
        plt.figure(figsize=(8, 5))
        sns.histplot(df_sub.dropna(), bins=50)
        plt.title('Subscribers distribution')
        plt.tight_layout()
        if out:
            plt.savefig(out / 'subscribers_dist.png')
        else:
            plt.show()
        plt.close()

    # top 20 channels by subscribers
    try:
        if 'subscribers' in df.columns and 'Youtuber' in df.columns:
            df['subscribers_num'] = pd.to_numeric(df['subscribers'], errors='coerce')
            top20 = df.sort_values('subscribers_num', ascending=False).head(20)
            plt.figure(figsize=(10, 8))
            sns.barplot(x='subscribers_num', y='Youtuber', data=top20)
            plt.title('Top 20 channels by subscribers')
            plt.xlabel('Subscribers')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'top20_by_subscribers.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # scatter: subscribers vs video views
    try:
        # support both 'video_views' and 'video views' column names
        if 'subscribers' in df.columns and ('video_views' in df.columns or 'video views' in df.columns):
            subs = pd.to_numeric(df['subscribers'], errors='coerce')
            if 'video_views' in df.columns:
                vids = pd.to_numeric(df['video_views'], errors='coerce')
            else:
                vids = pd.to_numeric(df['video views'], errors='coerce')
            scatter_df = pd.DataFrame({'subscribers': subs, 'video_views': vids}).dropna()
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x='subscribers', y='video_views', data=scatter_df)
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('Subscribers (log scale)')
            plt.ylabel('Video views (log scale)')
            plt.title('Subscribers vs Video Views (log-log)')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'subs_vs_video_views_scatter.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # correlation heatmap for numeric features
    try:
        num_df = df.select_dtypes(include=['number'])
        if num_df.shape[1] >= 2:
            corr = num_df.corr()
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr, cmap='vlag', center=0, annot=False)
            plt.title('Correlation matrix (numeric features)')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'correlation_heatmap.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # additional visualizations
    # top countries by count
    try:
        if 'Country' in df.columns:
            top_countries = df['Country'].fillna('Unknown').value_counts().head(20)
            plt.figure(figsize=(10, 8))
            sns.barplot(x=top_countries.values, y=top_countries.index)
            plt.title('Top 20 Countries by channel count')
            plt.xlabel('Count')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'top_countries.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # uploads distribution
    try:
        if 'uploads' in df.columns:
            uploads = pd.to_numeric(df['uploads'], errors='coerce')
            plt.figure(figsize=(8, 5))
            sns.histplot(uploads.dropna(), bins=50)
            plt.title('Uploads distribution')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'uploads_distribution.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # median subscribers by category (top 20 categories by count)
    try:
        if 'category' in df.columns and 'subscribers' in df.columns:
            subs = pd.to_numeric(df['subscribers'], errors='coerce')
            cat_counts = df['category'].fillna('Unknown').value_counts()
            top_cats = cat_counts.head(20).index.tolist()
            medians = df.loc[df['category'].fillna('Unknown').isin(top_cats)].groupby(df['category'].fillna('Unknown'))['subscribers'].apply(lambda s: pd.to_numeric(s, errors='coerce').median()).sort_values(ascending=False)
            plt.figure(figsize=(10, 8))
            sns.barplot(x=medians.values, y=medians.index)
            plt.title('Median subscribers by category (top 20 categories)')
            plt.xlabel('Median Subscribers')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'median_subs_by_category.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # boxplot of subscribers for top categories (to show spread)
    try:
        if 'category' in df.columns and 'subscribers' in df.columns:
            top_cats = df['category'].fillna('Unknown').value_counts().head(10).index.tolist()
            df_box = df[df['category'].fillna('Unknown').isin(top_cats)].copy()
            df_box['subscribers_num'] = pd.to_numeric(df_box['subscribers'], errors='coerce')
            plt.figure(figsize=(12, 8))
            sns.boxplot(x='subscribers_num', y=df_box['category'].fillna('Unknown'), data=df_box)
            plt.xscale('log')
            plt.title('Subscribers distribution by top 10 categories (log x)')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'subs_boxplot_by_category.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # top 20 channels by video views
    try:
        if ('video_views' in df.columns or 'video views' in df.columns) and 'Youtuber' in df.columns:
            if 'video_views' in df.columns:
                df['video_views_num'] = pd.to_numeric(df['video_views'], errors='coerce')
            else:
                df['video_views_num'] = pd.to_numeric(df['video views'], errors='coerce')
            top_vids = df.sort_values('video_views_num', ascending=False).head(20)
            plt.figure(figsize=(10, 8))
            sns.barplot(x='video_views_num', y='Youtuber', data=top_vids)
            plt.title('Top 20 channels by video views')
            plt.xlabel('Video views')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'top20_by_video_views.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    # created_year counts
    try:
        if 'created_year' in df.columns:
            cy = pd.to_numeric(df['created_year'], errors='coerce')
            cy_counts = cy.dropna().astype(int).value_counts().sort_index()
            plt.figure(figsize=(12, 6))
            sns.barplot(x=cy_counts.index.astype(str), y=cy_counts.values)
            plt.xticks(rotation=45)
            plt.title('Channels created by year')
            plt.xlabel('Year')
            plt.tight_layout()
            if out:
                plt.savefig(out / 'created_year_counts.png')
            else:
                plt.show()
            plt.close()
    except Exception:
        pass

    return df


if __name__ == '__main__':
    import sys
    csv = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'Global YouTube Statistics.csv'
    # save outputs inside the project folder `analytics_project/outputs` (parents[1])
    run_basic_eda(csv, output_dir=Path(__file__).resolve().parents[1] / 'outputs')
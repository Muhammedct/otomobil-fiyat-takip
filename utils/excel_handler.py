import pandas as pd
import os

def save_to_excel(df: pd.DataFrame, filename: str):
    """DataFrame'i belirtilen Excel dosyasına kaydeder."""
    try:
        df.to_excel(filename, index=False)
        print(f"Veriler başarıyla '{filename}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"HATA: Excel dosyasına kaydederken bir sorun oluştu: {e}")

def read_from_excel(filename: str) -> pd.DataFrame:
    """Belirtilen Excel dosyasını okur ve DataFrame olarak döndürür."""
    if not os.path.exists(filename):
        return pd.DataFrame()
    try:
        return pd.read_excel(filename)
    except Exception as e:
        print(f"HATA: Excel dosyasını okurken bir sorun oluştu: {e}")
        return pd.DataFrame()

def compare_dataframes(old_df: pd.DataFrame, new_df: pd.DataFrame) -> (bool, str):
    """
    İki DataFrame'i karşılaştırır. Değişiklik varsa True ve özet metni döndürür.
    """
    if old_df.empty:
        return True, "İlk veri toplama işlemi. Fiyat listesi oluşturuldu."

    key_columns = [col for col in new_df.columns if col != 'Fiyat']

    for df in [old_df, new_df]:
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    merged_df = pd.merge(
        old_df, new_df,
        on=key_columns,
        how='outer',
        suffixes=('_eski', '_yeni')
    )

    # Fiyatı değişenler
    changed_prices = merged_df[merged_df['Fiyat_eski'] != merged_df['Fiyat_yeni']].dropna(subset=['Fiyat_eski', 'Fiyat_yeni'])

    # Eklenen araçlar (eskide olmayıp yenide olanlar)
    added_cars = merged_df[merged_df['Fiyat_eski'].isna()]

    # Kaldırılan araçlar (yenide olmayıp eskide olanlar)
    removed_cars = merged_df[merged_df['Fiyat_yeni'].isna()]

    if changed_prices.empty and added_cars.empty and removed_cars.empty:
        return False, ""

    summary = ""
    if not changed_prices.empty:
        summary += "FİYATI DEĞİŞEN ARAÇLAR:\n"
        for _, row in changed_prices.iterrows():
            summary += f"- {row['Marka']} {row['Model']} ({row.get('Donanım', row.get('Yakıt/Donanım'))}): {row['Fiyat_eski']} -> {row['Fiyat_yeni']}\n"
        summary += "\n"

    if not added_cars.empty:
        summary += "LİSTEYE YENİ EKLENEN ARAÇLAR:\n"
        for _, row in added_cars.iterrows():
            summary += f"- {row['Marka']} {row['Model']} ({row.get('Donanım', row.get('Yakıt/Donanım'))}): {row['Fiyat_yeni']}\n"
        summary += "\n"

    if not removed_cars.empty:
        summary += "LİSTEDEN KALDIRILAN ARAÇLAR:\n"
        for _, row in removed_cars.iterrows():
            summary += f"- {row['Marka']} {row['Model']} ({row.get('Donanım', row.get('Yakıt/Donanım'))}): {row['Fiyat_eski']}\n"

    return True, summary.strip()
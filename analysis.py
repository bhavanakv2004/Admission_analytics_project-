import pandas as pd

# =========================
# LOAD FILE (CSV / EXCEL)
# =========================
def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")


# =========================
# LOAD + MERGE DATASETS
# =========================
def load_and_merge(leads_file, counselling_file, applications_file, enrollment_file):
    leads = load_file(leads_file)
    counselling = load_file(counselling_file)
    applications = load_file(applications_file)
    enrollment = load_file(enrollment_file)

    df = leads.merge(counselling, on="Lead_ID", how="left")
    df = df.merge(applications, on="Lead_ID", how="left")
    df = df.merge(enrollment, on="Lead_ID", how="left")

    # ✅ SAFE NULL HANDLING
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("No")
        else:
            df[col] = df[col].fillna(pd.NA)

    return df


# =========================
# FUNNEL METRICS
# =========================
def funnel_metrics(df):
    total = df.shape[0]
    counselling = df[df["Counselling_Attended"] == "Yes"].shape[0]
    application = df[df["Application_Submitted"] == "Yes"].shape[0]
    enrolled = df[df["Enrolled"] == "Yes"].shape[0]

    return total, counselling, application, enrolled


# =========================
# CONVERSION RATES
# =========================
def conversion_rates(total, counselling, application, enrolled):
    return {
        "Lead → Counselling": counselling / total if total else 0,
        "Counselling → Application": application / counselling if counselling else 0,
        "Application → Enrollment": enrolled / application if application else 0,
        "Overall Conversion": enrolled / total if total else 0
    }


# =========================
# CHANNEL ANALYSIS
# =========================
def channel_analysis(df):
    return df.groupby("Source_Channel").agg(
        leads=("Lead_ID", "count"),
        enrolled=("Enrolled", lambda x: (x == "Yes").sum())
    ).sort_values(by="enrolled", ascending=False)


# =========================
# CITY ANALYSIS
# =========================
def city_analysis(df):
    return df.groupby("City")["Enrolled"].apply(
        lambda x: (x == "Yes").sum()
    ).sort_values(ascending=False)


# =========================
# COUNSELLOR PERFORMANCE
# =========================
def counsellor_performance(df):
    return df.groupby("Counsellor").agg(
        counselling=("Counselling_Attended", lambda x: (x == "Yes").sum()),
        enrolled=("Enrolled", lambda x: (x == "Yes").sum())
    ).sort_values(by="enrolled", ascending=False)


# =========================
# DROP-OFF ANALYSIS
# =========================
def drop_off_analysis(total, counselling, application, enrolled):
    return {
        "Leads → Counselling": total - counselling,
        "Counselling → Application": counselling - application,
        "Application → Enrollment": application - enrolled
    }


# =========================
# STAGE ANALYSIS
# =========================
def stage_analysis(df):
    total, counselling, application, enrolled = funnel_metrics(df)

    data = {
        "Stage": ["Leads", "Counselling", "Application", "Enrolled"],
        "Count": [total, counselling, application, enrolled]
    }

    stage_df = pd.DataFrame(data)

    stage_df["Conversion %"] = stage_df["Count"].pct_change().fillna(1) * 100
    stage_df["Drop-off %"] = 100 - stage_df["Conversion %"]

    return stage_df


# =========================
# BEST PERFORMERS
# =========================
def best_performers(df):
    channel_df = channel_analysis(df)
    city_df = city_analysis(df)
    counsellor_df = counsellor_performance(df)

    best_channel = channel_df.index[0] if not channel_df.empty else "N/A"
    best_city = city_df.index[0] if not city_df.empty else "N/A"
    best_counsellor = counsellor_df.index[0] if not counsellor_df.empty else "N/A"

    return best_channel, best_city, best_counsellor

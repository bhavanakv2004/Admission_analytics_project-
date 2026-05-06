
import pandas as pd

def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")
def load_and_merge():
    leads = pd.read_csv("data/leads.csv")
    counselling = pd.read_csv("data/counselling.csv")
    applications = pd.read_csv("data/applications.csv")
    enrollment = pd.read_csv("data/enrollment.csv")

    df = leads.merge(counselling, on="Lead_ID", how="left")
    df = df.merge(applications, on="Lead_ID", how="left")
    df = df.merge(enrollment, on="Lead_ID", how="left")

    return df


def funnel_metrics(df):
    total = df.shape[0]
    counselling = df[df["Counselling_Attended"] == "Yes"].shape[0]
    application = df[df["Application_Submitted"] == "Yes"].shape[0]
    enrolled = df[df["Enrolled"] == "Yes"].shape[0]

    return total, counselling, application, enrolled


def conversion_rates(total, counselling, application, enrolled):
    return {
        "Lead → Counselling": counselling / total if total else 0,
        "Counselling → Application": application / counselling if counselling else 0,
        "Application → Enrollment": enrolled / application if application else 0,
        "Overall Conversion": enrolled / total if total else 0
    }


def channel_analysis(df):
    return df.groupby("Source_Channel").agg(
        leads=("Lead_ID", "count"),
        enrolled=("Enrolled", lambda x: (x == "Yes").sum())
    )


def city_analysis(df):
    return df.groupby("City")["Enrolled"].apply(lambda x: (x == "Yes").sum())


def counsellor_performance(df):
    return df.groupby("Counsellor").agg(
        counselling=("Counselling_Attended", lambda x: (x == "Yes").sum()),
        enrolled=("Enrolled", lambda x: (x == "Yes").sum())
    )


def drop_off_analysis(total, counselling, application, enrolled):
    return {
        "Leads → Counselling": total - counselling,
        "Counselling → Application": counselling - application,
        "Application → Enrollment": application - enrolled
    }

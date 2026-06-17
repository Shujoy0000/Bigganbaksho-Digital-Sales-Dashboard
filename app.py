import streamlit as stimport pandas as pdimport plotly.express as pximport streamlit.components.v1 as componentsimport osimport datetimeimport jsonimport re

১. পেজ সেটিংস ও লোগো

logo_path = "logo.png"if not os.path.exists(logo_path):logo_path = "logo.jpg"

st.set_page_config(page_title="Bigganbaksho Digital Sales Dashboard",layout="wide",page_icon="📊")

২. কাস্টম CSS

st.markdown("""html, body, [class*="css"] {color: #333333 !important;font-family: 'Segoe UI', sans-serif;}

.main-title { 
    text-align: center; 
    color: #FF6600; 
    font-size: 55px; 
    font-weight: 800; 
    margin-top: -100px; 
    margin-bottom: 5px; 
}

.developer-text { 
    text-align: center; 
    font-style: italic; 
    font-size: 18px; 
    color: #666; 
    margin-bottom: 10px; 
}

.slogan-text { 
    text-align: center; 
    font-size: 30px; 
    font-weight: 800; 
    color: #222; 
    margin-top: 10px; 
}

.vision-text { 
    text-align: center; 
    font-size: 20px; 
    color: #777; 
    margin-bottom: 30px; 
}

.metric-card { 
    background: #FFFFFF; 
    padding: 0px 2px; 
    border-radius: 12px; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
    text-align: center; 
    border-top: 8px solid #FF6600; 
    margin-bottom: 10px;
    display: flex; 
    align-items: center;
    justify-content: center;
    height: 152px;
    min-height: 152px; 
    overflow: hidden; 
}

.metric-content {
    transform: scale(1.42);
    transform-origin: center;
    width: 100%;
}

.metric-label { 
    font-size: 20px; 
    color: #444444; 
    margin: 0 0 10px 0; 
    font-weight: 900; 
    text-transform: uppercase; 
    white-space: nowrap; 
    line-height: 1;
}

.metric-value { 
    font-size: 40px; 
    color: #2b2b2b; 
    font-weight: 900; 
    margin: 0; 
    line-height: 1; 
    white-space: nowrap; 
    letter-spacing: -0.5px;
}

.section-header { 
    font-size: 28px; 
    color: #333; 
    background-color: #F0F2F6; 
    padding: 12px 20px; 
    border-radius: 8px; 
    border-left: 10px solid #FF6600; 
    margin-top: 45px; 
    margin-bottom: 25px; 
    font-weight: 700;
}

.copy-note {
    font-size: 13px;
    color: #666;
    margin-top: -4px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

৩. Helper Functions

def clean_number(series):return pd.to_numeric(series.astype(str).str.replace(",", "", regex=False).str.replace("৳", "", regex=False).str.strip(),errors="coerce").fillna(0)

def clean_key(text):text = str(text).lower()text = re.sub(r'[^a-z0-9]+', '', text)return text.strip('')

def show_copyable_table(df_display, key_name):if df_display.empty:st.info("No data found.")return

table_height = min(600, max(180, 38 * (len(df_display) + 1)))

st.markdown(
    '<div class="copy-note">Table থেকে cell, row বা full table copy করা যাবে। নিচের button দিয়ে full table copy হবে।</div>',
    unsafe_allow_html=True
)

safe_key = clean_key(key_name)
table_text = df_display.to_csv(sep="\t", index=False)
table_json = json.dumps(table_text, ensure_ascii=False)
html_table = df_display.to_html(index=False, escape=False)

components.html(f"""
    <style>
        .table-wrap-{safe_key} {{
            max-height: {table_height}px;
            overflow: auto;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            background: white;
            margin-bottom: 8px;
        }}

        .table-wrap-{safe_key} table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            color: #111827;
        }}

        .table-wrap-{safe_key} thead th {{
            font-weight: 900 !important;
            color: #000000 !important;
            background: #F8F9FB;
            border: 1px solid #E0E0E0;
            padding: 9px 10px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 2;
            white-space: nowrap;
        }}

        .table-wrap-{safe_key} tbody td {{
            border: 1px solid #E8E8E8;
            padding: 8px 10px;
            text-align: left;
            white-space: nowrap;
        }}

        .table-wrap-{safe_key} tbody tr:last-child td {{
            font-weight: 900 !important;
            color: #000000 !important;
        }}

        .copy-btn-{safe_key} {{
            background: #FF6600;
            color: white;
            border: none;
            border-radius: 7px;
            padding: 8px 14px;
            font-weight: 700;
            cursor: pointer;
            font-size: 14px;
            margin-top: 4px;
        }}
    </style>

    <div class="table-wrap-{safe_key}">
        {html_table}
    </div>

    <button class="copy-btn-{safe_key}" id="copy_btn_{safe_key}">
        📋 Copy full table
    </button>

    <script>
    const btn = document.getElementById("copy_btn_{safe_key}");
    const tableText = {table_json};

    btn.onclick = async function() {{
        try {{
            await navigator.clipboard.writeText(tableText);
            btn.innerText = "✅ Copied!";
            setTimeout(() => btn.innerText = "📋 Copy full table", 1300);
        }} catch (err) {{
            btn.innerText = "Copy failed";
            setTimeout(() => btn.innerText = "📋 Copy full table", 1300);
        }}
    }};
    </script>
""", height=table_height + 70)

৪. ডাটা লোডিং

@st.cache_data(ttl=300)def load_data():url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vROzw82VfyjCSLWm0lxBh9lylW9t7D17AIRuznYyQQKa5umze0iBWEXGXCyHBIT5LJZzODlqgQRm7Ai/pub?gid=1622849396&single=true&output=csv"df = pd.read_csv(url, dtype={"AD ID": str})

# Column clean
df.columns = df.columns.astype(str).str.strip()
df = df.dropna(how="all")

# Date column
if "Date" in df.columns:
    df["Report Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
elif "Order Date" in df.columns:
    df["Report Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
else:
    df["Report Date"] = pd.NaT

# Date না থাকলে report-এ আসবে না
df = df.dropna(subset=["Report Date"])

# প্রয়োজনীয় numeric column
needed_numeric_cols = [
    "Total Amount",
    "Shipping Charge",
    "Discount",
    "Total Qty",
    "Discount per product",
    "Product Price"
]

for col in needed_numeric_cols:
    if col not in df.columns:
        df[col] = 0
    df[col] = clean_number(df[col])

# Product QTY এবং Product Price-1 to 15 clean
for i in range(1, 16):
    qty_col = f"Product QTY-{i}"
    price_col = f"Product Price-{i}"

    if qty_col in df.columns:
        df[qty_col] = clean_number(df[qty_col])
    else:
        df[qty_col] = 0

    if price_col in df.columns:
        df[price_col] = clean_number(df[price_col])
    else:
        df[price_col] = 0

# Text column clean
for col in ["Order Collector", "Source", "District", "Class", "Age", "Profession", "AD ID"]:
    if col not in df.columns:
        df[col] = "Unknown"

    df[col] = df[col].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    df[col] = df[col].replace(["", "nan", "None", "0", "0.0"], "Unknown")

# Source spelling normalize
df["Source"] = df["Source"].replace({
    "FaceBook": "Facebook",
    "facebook": "Facebook",
    "FACEBOOK": "Facebook",
    "Face Book": "Facebook",
    "FB": "Facebook"
})

# Revenue = শীটের শেষের Product Price column
# fallback: Product Price blank হলে Total Amount - Shipping Charge
fallback_revenue = df["Total Amount"] - df["Shipping Charge"]
df["Revenue"] = df["Product Price"].where(df["Product Price"] > 0, fallback_revenue)
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0)
df["Revenue"] = df["Revenue"].clip(lower=0)

# Total Sales = Revenue + Discount
df["Total Sales"] = df["Revenue"] + df["Discount"]
df["Total Sales"] = pd.to_numeric(df["Total Sales"], errors="coerce").fillna(0)
df["Total Sales"] = df["Total Sales"].clip(lower=0)

# Product-wise sales price করার জন্য per product discount
exact_unit_discount = df["Discount"] / df["Total Qty"].where(df["Total Qty"] > 0)
df["Unit Discount"] = exact_unit_discount.fillna(df["Discount per product"]).fillna(0)
df["Unit Discount"] = df["Unit Discount"].clip(lower=0)

return df

৫. সাধারণ টেবিল প্রসেসিং

def process_table_data(df, label_col, val_col, total_val, is_currency=False, limit_15=False):if df.empty:return df

df = df.copy()

numeric_cols = df.select_dtypes(include="number").columns.tolist()
if label_col in numeric_cols:
    numeric_cols.remove(label_col)

if limit_15 and len(df) > 15:
    top_df = df.head(14).copy()
    others_dict = {label_col: "Others"}

    for col in numeric_cols:
        others_dict[col] = df.iloc[14:][col].sum()

    others_row = pd.DataFrame([others_dict])
    final_df = pd.concat([top_df, others_row], ignore_index=True)
else:
    final_df = df.copy()

final_df["%"] = (
    final_df[val_col] / (total_val if total_val > 0 else 1) * 100
).map("{:.1f}%".format)

total_dict = {label_col: "Total", "%": "100.0%"}

for col in numeric_cols:
    if col == val_col:
        total_dict[col] = total_val
    else:
        total_dict[col] = final_df[col].sum()

final_df = pd.concat([final_df, pd.DataFrame([total_dict])], ignore_index=True)

for col in numeric_cols:
    if is_currency and col == val_col:
        final_df[col] = final_df[col].apply(
            lambda x: f"৳{int(round(float(x))):,}" if pd.notna(x) else ""
        )
    else:
        final_df[col] = final_df[col].apply(
            lambda x: f"{int(round(float(x))):,}" if pd.notna(x) else ""
        )

return final_df

৬. Product data তৈরি

def build_product_long_data(df_in):all_items = []

for i in range(1, 16):
    name_col = f"Product Name-{i}"
    price_col = f"Product Price-{i}"
    qty_col = f"Product QTY-{i}"

    if name_col in df_in.columns:
        temp = df_in[[name_col, price_col, qty_col, "Unit Discount", "AD ID"]].copy()
        temp = temp.rename(columns={
            name_col: "Product",
            price_col: "Unit Price",
            qty_col: "Qty"
        })

        temp["Product"] = temp["Product"].astype(str).str.strip()
        temp["AD ID"] = temp["AD ID"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
        temp["Qty"] = pd.to_numeric(temp["Qty"], errors="coerce").fillna(0)
        temp["Unit Price"] = pd.to_numeric(temp["Unit Price"], errors="coerce").fillna(0)
        temp["Unit Discount"] = pd.to_numeric(temp["Unit Discount"], errors="coerce").fillna(0)

        temp = temp[
            (temp["Product"] != "") &
            (temp["Product"] != "0") &
            (temp["Product"] != "nan") &
            (temp["Qty"] > 0)
        ]

        # Sales Price = (Product Price - Discount per product) * QTY
        temp["Sales Price"] = (temp["Unit Price"] - temp["Unit Discount"]).clip(lower=0) * temp["Qty"]

        all_items.append(temp[["AD ID", "Product", "Qty", "Sales Price"]])

if all_items:
    return pd.concat(all_items, ignore_index=True)

return pd.DataFrame(columns=["AD ID", "Product", "Qty", "Sales Price"])

def render_product_report(df_in, total_qty):st.markdown("### Product Sales Analytics")

product_long = build_product_long_data(df_in)

if product_long.empty:
    st.info("No product data found.")
    return

product_stats = product_long.groupby("Product").agg(
    Value=("Qty", "sum"),
    Sales_Price=("Sales Price", "sum")
).reset_index()

product_stats["Value"] = product_stats["Value"].round().astype(int)
product_stats["Sales_Price"] = product_stats["Sales_Price"].round().astype(int)

product_stats = product_stats.sort_values("Value", ascending=False)

total_product_sales = product_stats["Sales_Price"].sum()

product_stats["%"] = (
    product_stats["Sales_Price"] / (total_product_sales if total_product_sales > 0 else 1) * 100
)

c1, c2 = st.columns([2, 1])

with c1:
    plot_data = product_stats.head(10).copy()

    fig = px.bar(
        plot_data,
        x="Value",
        y="Product",
        orientation="h",
        color="Product",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text_auto=True
    )

    fig.update_traces(
        textangle=0,
        textposition="outside",
        texttemplate="%{x:,}"
    )

    fig.update_layout(
        height=len(plot_data) * 45 + 50,
        margin=dict(t=20, b=20, l=10, r=80),
        yaxis={
            "type": "category",
            "categoryorder": "array",
            "categoryarray": plot_data["Product"].tolist()
        },
        xaxis=dict(showticklabels=False, title=""),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:
    product_table = product_stats.copy()
    product_table = product_table.rename(columns={"Sales_Price": "Sales Price"})

    product_table["Sales Price"] = product_table["Sales Price"].apply(lambda x: f"৳{int(x):,}")
    product_table["%"] = product_table["%"].map("{:.1f}%".format)
    product_table["Value"] = product_table["Value"].apply(lambda x: f"{int(x):,}")

    total_row = pd.DataFrame([{
        "Product": "Total",
        "Value": f"{int(total_qty):,}",
        "Sales Price": f"৳{int(total_product_sales):,}",
        "%": "100.0%"
    }])

    product_table = pd.concat([product_table, total_row], ignore_index=True)

    show_copyable_table(
        product_table[["Product", "Value", "Sales Price", "%"]],
        "product_table"
    )

৭. AD ID Report

def render_ad_id_report(df_in):st.markdown('AD ID Report',unsafe_allow_html=True)

if "AD ID" not in df_in.columns:
    st.info("AD ID column not found.")
    return

ad_df = df_in.copy()
ad_df["AD ID"] = ad_df["AD ID"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)

ad_df = ad_df[
    (ad_df["AD ID"] != "") &
    (ad_df["AD ID"] != "nan") &
    (ad_df["AD ID"] != "0") &
    (ad_df["AD ID"] != "Unknown")
]

if ad_df.empty:
    st.info("No AD ID data found.")
    return

# Main AD ID summary
ad_stats = ad_df.groupby("AD ID").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Revenue", "count"),
    Qty=("Total Qty", "sum")
).reset_index()

ad_stats = ad_stats.sort_values("Revenue", ascending=False)
ad_stats = ad_stats.rename(columns={"AD ID": "AD ID Name"})

total_ad_revenue = ad_stats["Revenue"].sum()
total_ad_orders = ad_stats["Orders"].sum()
total_ad_qty = ad_stats["Qty"].sum()

ad_stats["%"] = (
    ad_stats["Revenue"] / (total_ad_revenue if total_ad_revenue > 0 else 1) * 100
)

# প্রথমে শুধু chart, পাশে কিছু থাকবে না
st.markdown("### AD ID-wise Revenue Chart")

plot_data = ad_stats.head(10).copy()

fig_ad = px.bar(
    plot_data,
    x="Revenue",
    y="AD ID Name",
    orientation="h",
    color="AD ID Name",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    text_auto=True
)

fig_ad.update_traces(
    textfont=dict(size=14, color="black"),
    textangle=0,
    textposition="outside",
    texttemplate="৳%{x:,}"
)

fig_ad.update_layout(
    height=len(plot_data) * 45 + 70,
    margin=dict(t=20, b=40, l=10, r=80),
    yaxis={
        "categoryorder": "array",
        "categoryarray": plot_data["AD ID Name"].tolist()
    },
    xaxis=dict(tickformat=",d", title="Revenue"),
    showlegend=False
)

st.plotly_chart(fig_ad, use_container_width=True)

# নিচে AD ID main table
st.markdown("### AD ID-wise Summary Table")

ad_table = ad_stats.copy()
ad_table["Revenue"] = ad_table["Revenue"].apply(lambda x: f"৳{int(round(float(x))):,}")
ad_table["Orders"] = ad_table["Orders"].apply(lambda x: f"{int(round(float(x))):,}")
ad_table["Qty"] = ad_table["Qty"].apply(lambda x: f"{int(round(float(x))):,}")
ad_table["%"] = ad_table["%"].map("{:.1f}%".format)

total_row = pd.DataFrame([{
    "AD ID Name": "Total",
    "Revenue": f"৳{int(round(float(total_ad_revenue))):,}",
    "Orders": f"{int(round(float(total_ad_orders))):,}",
    "Qty": f"{int(round(float(total_ad_qty))):,}",
    "%": "100.0%"
}])

ad_table = pd.concat([ad_table, total_row], ignore_index=True)

show_copyable_table(
    ad_table[["AD ID Name", "Revenue", "Orders", "Qty", "%"]],
    "ad_id_summary_table"
)

# নিচে কোন AD ID থেকে কোন product কত পিস এবং revenue
st.markdown("### AD ID-wise Product Sales Table")

product_long = build_product_long_data(ad_df)

if product_long.empty:
    st.info("No AD ID product data found.")
    return

product_long = product_long[
    (product_long["AD ID"] != "") &
    (product_long["AD ID"] != "nan") &
    (product_long["AD ID"] != "0") &
    (product_long["AD ID"] != "Unknown")
]

ad_product_stats = product_long.groupby(["AD ID", "Product"]).agg(
    Value=("Qty", "sum"),
    Revenue=("Sales Price", "sum")
).reset_index()

ad_product_stats = ad_product_stats.sort_values(["AD ID", "Revenue"], ascending=[True, False])
ad_product_stats = ad_product_stats.rename(columns={"AD ID": "AD ID Name"})

total_product_revenue = ad_product_stats["Revenue"].sum()
total_product_qty = ad_product_stats["Value"].sum()

ad_product_stats["%"] = (
    ad_product_stats["Revenue"] / (total_product_revenue if total_product_revenue > 0 else 1) * 100
)

ad_product_table = ad_product_stats.copy()
ad_product_table["Value"] = ad_product_table["Value"].apply(lambda x: f"{int(round(float(x))):,}")
ad_product_table["Revenue"] = ad_product_table["Revenue"].apply(lambda x: f"৳{int(round(float(x))):,}")
ad_product_table["%"] = ad_product_table["%"].map("{:.1f}%".format)

total_product_row = pd.DataFrame([{
    "AD ID Name": "Total",
    "Product": "",
    "Value": f"{int(round(float(total_product_qty))):,}",
    "Revenue": f"৳{int(round(float(total_product_revenue))):,}",
    "%": "100.0%"
}])

ad_product_table = pd.concat([ad_product_table, total_product_row], ignore_index=True)

show_copyable_table(
    ad_product_table[["AD ID Name", "Product", "Value", "Revenue", "%"]],
    "ad_id_product_sales_table"
)

৮. Dynamic report

def render_report_dynamic(title, df_in, group_col, val_col, grand_total, is_currency=False, chart_top_10=True, table_limit_15=False):st.markdown(f"### {title}")

if df_in.empty:
    st.info("No data found.")
    return

df_work = df_in.copy()

if group_col not in df_work.columns:
    st.warning(f"{group_col} column not found.")
    return

df_work[group_col] = df_work[group_col].astype(str).str.strip()
df_work = df_work[
    (df_work[group_col] != "") &
    (df_work[group_col] != "nan") &
    (df_work[group_col] != "0") &
    (df_work[group_col] != "Unknown")
]

if df_work.empty:
    st.info("No valid data found.")
    return

if is_currency:
    stats = df_work.groupby(group_col).agg(
        Value=(val_col, "sum")
    ).reset_index()
else:
    stats = df_work.groupby(group_col).agg(
        Value=(val_col, "count")
    ).reset_index()

stats = stats.sort_values("Value", ascending=False)
cat_array = stats[group_col].tolist()

c1, c2 = st.columns([2, 1])

with c1:
    plot_data = stats.head(10).copy() if chart_top_10 else stats.copy()

    fig = px.bar(
        plot_data,
        x="Value",
        y=group_col,
        orientation="h",
        color=group_col,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text_auto=True
    )

    fig.update_traces(
        textangle=0,
        textposition="outside",
        texttemplate="৳%{x:,}" if is_currency else "%{x:,}"
    )

    fig.update_layout(
        height=len(plot_data) * 45 + 50,
        margin=dict(t=20, b=20, l=10, r=80),
        yaxis={
            "type": "category",
            "categoryorder": "array",
            "categoryarray": cat_array
        },
        xaxis=dict(showticklabels=False, title=""),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:
    table_df = process_table_data(
        stats,
        group_col,
        "Value",
        grand_total,
        is_currency=is_currency,
        limit_15=False
    )

    show_copyable_table(table_df, title)

try:df = load_data()

# --- হেডার ---
if os.path.exists(logo_path):
    st.image(logo_path, width=120)

st.markdown(
    '<div class="main-title">Bigganbaksho Digital Sales Dashboard</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="developer-text">Web App Developed By-Shujoy Shaha</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="slogan-text">ম্যানুয়েল কাজের দিন শেষ, বিজ্ঞানবাক্সে বাংলাদেশ</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="vision-text">অন্যরকম বাংলাদেশের স্বপ্ন নিয়ে</div>',
    unsafe_allow_html=True
)

# --- ফিল্টার ---
st.sidebar.header("📅 Select Date Range")

today = datetime.date.today()

min_date = df["Report Date"].dt.date.min()
max_date = df["Report Date"].dt.date.max()

default_start = max(min_date, today - datetime.timedelta(days=30)) if pd.notna(min_date) else today - datetime.timedelta(days=30)
default_end = max_date if pd.notna(max_date) else today

start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", default_end)

f_df = df[
    (df["Report Date"].dt.date >= start_date) &
    (df["Report Date"].dt.date <= end_date)
]

# --- ১. সামারি ---
total_sales = int(round(f_df["Total Sales"].sum()))
revenue = int(round(f_df["Revenue"].sum()))
ords = len(f_df)
qty = int(round(f_df["Total Qty"].sum()))
dis = int(round(f_df["Discount"].sum()))

aov = int(revenue / ords) if ords > 0 else 0
dis_p = (dis / total_sales * 100) if total_sales > 0 else 0

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

summaries = [
    ("Total Sales", f"৳{total_sales:,}"),
    ("Revenue", f"৳{revenue:,}"),
    ("Orders", f"{ords:,}"),
    ("AOV", f"৳{aov:,}"),
    ("Product Qty", f"{qty:,}"),
    ("Discount", f"৳{dis:,}"),
    ("Discount %", f"{dis_p:.1f}%")
]

for col, (label, value) in zip([c1, c2, c3, c4, c5, c6, c7], summaries):
    col.markdown(
        f"<div class='metric-card'><div class='metric-content'><p class='metric-label'>{label}</p><p class='metric-value'>{value}</p></div></div>",
        unsafe_allow_html=True
    )

# --- ২. Agent-wise Report ---
st.markdown(
    '<div class="section-header">Agent-wise Revenue Report</div>',
    unsafe_allow_html=True
)

agent_data = f_df.groupby("Order Collector").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Revenue", "count"),
    Qty=("Total Qty", "sum")
).reset_index()

agent_data = agent_data.sort_values("Revenue", ascending=False)

fig_a = px.bar(
    agent_data,
    x="Revenue",
    y="Order Collector",
    orientation="h",
    color="Order Collector",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    text_auto=True
)

fig_a.update_traces(
    textfont=dict(size=14, color="black"),
    textangle=0,
    textposition="outside",
    texttemplate="৳%{x:,}"
)

fig_a.update_layout(
    height=len(agent_data) * 45 + 70,
    margin=dict(t=20, b=40, l=10, r=80),
    yaxis={
        "categoryorder": "array",
        "categoryarray": agent_data["Order Collector"].tolist()
    },
    xaxis=dict(tickformat=",d", title="Revenue"),
    showlegend=False
)

st.plotly_chart(fig_a, use_container_width=True)

agent_table = process_table_data(
    agent_data,
    "Order Collector",
    "Revenue",
    revenue,
    is_currency=True,
    limit_15=False
)

show_copyable_table(agent_table, "agent_table")

# --- ৩. Source-wise Report ---
st.markdown(
    '<div class="section-header">Source-wise Revenue Report</div>',
    unsafe_allow_html=True
)

source_data = f_df.groupby("Source").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Revenue", "count"),
    Qty=("Total Qty", "sum")
).reset_index()

source_data = source_data.sort_values("Revenue", ascending=False)

fig_s = px.bar(
    source_data,
    x="Revenue",
    y="Source",
    orientation="h",
    color="Source",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    text_auto=True
)

fig_s.update_traces(
    textfont=dict(size=14, color="black"),
    textangle=0,
    textposition="outside",
    texttemplate="৳%{x:,}"
)

fig_s.update_layout(
    height=len(source_data) * 45 + 70,
    margin=dict(t=20, b=40, l=10, r=80),
    yaxis={
        "categoryorder": "array",
        "categoryarray": source_data["Source"].tolist()
    },
    xaxis=dict(tickformat=",d", title="Revenue"),
    showlegend=False
)

st.plotly_chart(fig_s, use_container_width=True)

source_table = process_table_data(
    source_data,
    "Source",
    "Revenue",
    revenue,
    is_currency=True,
    limit_15=False
)

show_copyable_table(source_table, "source_table")

# --- ৪. AD ID Report ---
render_ad_id_report(f_df)

# --- ৫. বিস্তারিত অ্যানালিটিক্স ড্রপডাউন ---
st.markdown(
    '<div class="section-header">Detailed Category Analytics</div>',
    unsafe_allow_html=True
)

# Source Filter + Agent Filter
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    source_options = ["All Sources"] + sorted(list(f_df["Source"].dropna().unique()))
    sel_source = st.selectbox(
        "Filter Reports by Source:",
        source_options,
        index=0,
        key="detailed_source_filter"
    )

source_filtered_df = f_df.copy()

if sel_source != "All Sources":
    source_filtered_df = source_filtered_df[source_filtered_df["Source"] == sel_source]

with filter_col2:
    agent_options = ["All Agents"] + sorted(list(source_filtered_df["Order Collector"].dropna().unique()))
    sel_agent = st.selectbox(
        "Filter Reports by Agent:",
        agent_options,
        index=0,
        key="detailed_agent_filter"
    )

p_df_f = source_filtered_df.copy()

if sel_agent != "All Agents":
    p_df_f = p_df_f[p_df_f["Order Collector"] == sel_agent]

curr_revenue = p_df_f["Revenue"].sum()
curr_qty = p_df_f["Total Qty"].sum()
curr_ords = len(p_df_f)

# Product report: chart Top 10, table all
render_product_report(p_df_f, curr_qty)

# অন্যান্য রিপোর্ট: chart Top 10, table full
render_report_dynamic(
    "Class-wise Distribution",
    p_df_f,
    "Class",
    "Revenue",
    curr_ords,
    chart_top_10=True,
    table_limit_15=False
)

render_report_dynamic(
    "Age-wise Distribution",
    p_df_f,
    "Age",
    "Revenue",
    curr_ords,
    chart_top_10=True,
    table_limit_15=False
)

render_report_dynamic(
    "Guardian Profession",
    p_df_f,
    "Profession",
    "Revenue",
    curr_ords,
    chart_top_10=True,
    table_limit_15=False
)

render_report_dynamic(
    "District-wise Revenue",
    p_df_f,
    "District",
    "Revenue",
    curr_revenue,
    is_currency=True,
    chart_top_10=True,
    table_limit_15=False
)

except Exception as e:st.error(f"Error: {e}")

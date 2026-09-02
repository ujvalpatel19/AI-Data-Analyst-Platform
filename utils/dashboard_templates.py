import pandas as pd
import numpy as np

# 21 Industry Dashboard Templates Catalog
DASHBOARD_TEMPLATES = {
    "amazon_sales": {
        "name": "🛒 Amazon Store Sales Dashboard",
        "category": "E-Commerce & Retail",
        "description": "Black & Gold PowerBI Executive Dashboard with Sales by Segment, Payment Mode, Ship Mode, Quarterly Profits, and Category breakdown.",
        "accent_color": "#F59E0B",
        "bg_color": "#0D0F12",
        "default_metrics": ["Sales", "Profit", "Quantity", "Discount"]
    },
    "csuite_executive": {
        "name": "💼 Executive C-Suite Performance",
        "category": "Executive & Strategy",
        "description": "High-level overview of revenue streams, operating margin, EBITDA growth, and key strategic KPI scorecards.",
        "accent_color": "#6366F1",
        "bg_color": "#0F172A",
        "default_metrics": ["Revenue", "Net_Profit", "Operating_Margin", "EBITDA"]
    },
    "finance_profitability": {
        "name": "📊 Financial Performance & Profitability",
        "category": "Finance & Accounting",
        "description": "Cash flow, gross profit margin, OPEX ratio, revenue breakdown, and quarterly financial health metrics.",
        "accent_color": "#10B981",
        "bg_color": "#064E3B",
        "default_metrics": ["Revenue", "Expenses", "Gross_Profit", "Net_Income"]
    },
    "retail_operations": {
        "name": "🛍️ Retail Store Operations",
        "category": "Retail & Sales",
        "description": "Store location sales, inventory turnover rate, average order value (AOV), and POS payment mode split.",
        "accent_color": "#EC4899",
        "bg_color": "#1E1B4B",
        "default_metrics": ["Store_Sales", "Transactions", "Avg_Basket_Size", "Inventory_Units"]
    },
    "marketing_roi": {
        "name": "🎯 Marketing & Campaign ROI",
        "category": "Marketing & Ads",
        "description": "CAC, LTV, ROAS, channel attribution (Google Ads, Meta, Email, Organic), and conversion funnel performance.",
        "accent_color": "#8B5CF6",
        "bg_color": "#1E1E2E",
        "default_metrics": ["Spend", "Conversions", "CAC", "ROAS"]
    },
    "saas_mrr": {
        "name": "⚡ SaaS Subscription & MRR/ARR",
        "category": "Technology & SaaS",
        "description": "MRR, ARR, Net Revenue Retention (NRR), Churn Rate, ARPU, and subscription tier breakdown (Basic, Pro, Enterprise).",
        "accent_color": "#06B6D4",
        "bg_color": "#083344",
        "default_metrics": ["MRR", "ARR", "Active_Subscriptions", "Churn_Rate"]
    },
    "customer_churn": {
        "name": "👥 Customer Churn & Retention",
        "category": "Customer Analytics",
        "description": "Customer lifetime value, attrition rate by cohort, customer satisfaction score (CSAT), and NPS breakdown.",
        "accent_color": "#EF4444",
        "bg_color": "#450A0A",
        "default_metrics": ["Total_Customers", "Active_Users", "Churned_Users", "NPS_Score"]
    },
    "supply_chain": {
        "name": "📦 Supply Chain & Inventory Logistics",
        "category": "Operations & Logistics",
        "description": "Order fulfillment time, stockout rate, supplier lead time, shipping cost analysis, and warehouse throughput.",
        "accent_color": "#F97316",
        "bg_color": "#1F2937",
        "default_metrics": ["Stock_Level", "Fulfillment_Days", "Shipping_Cost", "Defect_Rate"]
    },
    "healthcare": {
        "name": "🏥 Healthcare & Patient Analytics",
        "category": "Healthcare & Medical",
        "description": "Patient admission rate, average length of stay (ALOS), bed occupancy, treatment costs, and department breakdown.",
        "accent_color": "#14B8A6",
        "bg_color": "#042F2E",
        "default_metrics": ["Patients_Admitted", "Avg_Stay_Days", "Treatment_Cost", "Occupancy_Rate"]
    },
    "hr_workforce": {
        "name": "🏢 HR & Workforce Analytics",
        "category": "Human Resources",
        "description": "Employee headcount growth, attrition rate, training cost, department salary distribution, and diversity score.",
        "accent_color": "#3B82F6",
        "bg_color": "#1E3A8A",
        "default_metrics": ["Headcount", "Turnover_Rate", "Avg_Salary", "Training_Hours"]
    },
    "banking_risk": {
        "name": "🏦 Banking & Credit Risk",
        "category": "Banking & Fintech",
        "description": "Loan portfolio value, non-performing loans (NPL), credit score distribution, and default probability metrics.",
        "accent_color": "#EAB308",
        "bg_color": "#1C1917",
        "default_metrics": ["Total_Loans", "Default_Rate", "Avg_Credit_Score", "Interest_Income"]
    },
    "food_delivery": {
        "name": "🍕 Food Delivery & Restaurant",
        "category": "Food & Beverage",
        "description": "Daily food orders, average delivery time, top dish items, peak ordering hours, and courier rating.",
        "accent_color": "#E11D48",
        "bg_color": "#27272A",
        "default_metrics": ["Order_Count", "Delivery_Time_Mins", "Revenue", "Customer_Rating"]
    },
    "customer_support": {
        "name": "🎧 Customer Support & Helpdesk KPI",
        "category": "Operations & CS",
        "description": "First response time (FRT), resolution rate, ticket volume by category, SLA compliance, and CSAT score.",
        "accent_color": "#A855F7",
        "bg_color": "#3B0764",
        "default_metrics": ["Total_Tickets", "Avg_Resolution_Mins", "CSAT", "SLA_Compliance"]
    },
    "mobile_app": {
        "name": "📱 Mobile App & Engagement",
        "category": "Product & Mobile",
        "description": "DAU/MAU ratio, app downloads, session duration, in-app purchases, and crash-free session rate.",
        "accent_color": "#38BDF8",
        "bg_color": "#0C4A6E",
        "default_metrics": ["DAU", "MAU", "Session_Duration", "In_App_Revenue"]
    },
    "hospitality": {
        "name": "🏨 Hospitality & Hotel Occupancy",
        "category": "Hospitality & Tourism",
        "description": "RevPAR, Average Daily Rate (ADR), room occupancy percentage, booking channels, and guest reviews.",
        "accent_color": "#F43F5E",
        "bg_color": "#4C0519",
        "default_metrics": ["RevPAR", "ADR", "Occupancy_Rate", "Total_Bookings"]
    },
    "education": {
        "name": "🎓 Education & Student Analytics",
        "category": "Education",
        "description": "Student enrollment, course completion rate, average GPA distribution, attendance rate, and tuition revenue.",
        "accent_color": "#10B981",
        "bg_color": "#022C22",
        "default_metrics": ["Enrollment", "Completion_Rate", "Avg_GPA", "Attendance_Pct"]
    },
    "automotive": {
        "name": "🚗 Automotive Fleet Operations",
        "category": "Automotive & Fleet",
        "description": "Fleet fuel efficiency, total mileage, maintenance downtime, vehicle utilization rate, and EV vs ICE split.",
        "accent_color": "#64748B",
        "bg_color": "#0F172A",
        "default_metrics": ["Total_Distance", "Fuel_Consumption", "Maintenance_Cost", "Active_Vehicles"]
    },
    "energy_utilities": {
        "name": "⚡ Energy & Utilities Consumption",
        "category": "Energy & Sustainability",
        "description": "KWh energy consumption, renewable percentage (solar/wind), peak grid demand, and carbon emissions.",
        "accent_color": "#FACC15",
        "bg_color": "#16200B",
        "default_metrics": ["kWh_Usage", "Peak_Demand", "Solar_Gen_kWh", "CO2_Emissions"]
    },
    "construction": {
        "name": "🏗️ Construction & Project Management",
        "category": "Construction & Real Estate",
        "description": "Project budget variance, task completion percentage, safety incidents, milestone timeline, and site costs.",
        "accent_color": "#D97706",
        "bg_color": "#1C1917",
        "default_metrics": ["Budget_Allocated", "Budget_Spent", "Completion_Pct", "Safety_Incidents"]
    },
    "fitness_wellness": {
        "name": "🏋️ Fitness & Wellness Analytics",
        "category": "Health & Fitness",
        "description": "Gym active memberships, peak hour attendance, personal training sessions, renewal rate, and class fill rate.",
        "accent_color": "#22C55E",
        "bg_color": "#052E16",
        "default_metrics": ["Memberships", "Daily_Checkins", "Class_Attendees", "Renewal_Pct"]
    },
    "global_sales": {
        "name": "🌐 Global Multi-Region Sales",
        "category": "International Business",
        "description": "Cross-border sales volume, currency exchange impact, regional growth rates (APAC, EMEA, AMER), and top countries.",
        "accent_color": "#60A5FA",
        "bg_color": "#172554",
        "default_metrics": ["Global_Sales", "Export_Volume", "Countries_Covered", "YoY_Growth"]
    }
}

def auto_map_columns(df):
    """
    Intelligently scans dataset columns to match Date, Sales/Value, Profit, 
    Category, Region, Payment Mode, and Customer Segment fields.
    """
    mapping = {
        "date": None,
        "sales": None,
        "profit": None,
        "category": None,
        "region": None,
        "payment": None,
        "segment": None,
        "ship_mode": None
    }

    if df is None or df.empty:
        return mapping

    cols = list(df.columns)
    
    # 1. Date Detection
    for c in cols:
        if pd.api.types.is_datetime64_any_dtype(df[c]) or any(k in c.lower() for k in ['date', 'time', 'dt', 'year', 'month']):
            mapping["date"] = c
            break

    # 2. Sales / Metric Detection
    for c in cols:
        if any(k in c.lower() for k in ['sales', 'revenue', 'amount', 'total', 'price', 'spend', 'val', 'cost']):
            mapping["sales"] = c
            break
    if not mapping["sales"]:
        num_cols = list(df.select_dtypes(include=[np.number]).columns)
        if num_cols:
            mapping["sales"] = num_cols[0]

    # 3. Profit / Secondary Metric Detection
    for c in cols:
        if c != mapping["sales"] and any(k in c.lower() for k in ['profit', 'margin', 'earning', 'income', 'net']):
            mapping["profit"] = c
            break

    # 4. Category Detection
    for c in cols:
        if any(k in c.lower() for k in ['category', 'product', 'type', 'item', 'genre', 'department']):
            mapping["category"] = c
            break

    # 5. Region Detection
    for c in cols:
        if any(k in c.lower() for k in ['region', 'zone', 'country', 'state', 'location', 'area', 'territory']):
            mapping["region"] = c
            break

    # 6. Payment Mode Detection
    for c in cols:
        if any(k in c.lower() for k in ['payment', 'pay', 'mode', 'method', 'card']):
            mapping["payment"] = c
            break

    # 7. Customer Segment Detection
    for c in cols:
        if any(k in c.lower() for k in ['segment', 'customer', 'tier', 'group', 'user']):
            mapping["segment"] = c
            break

    # 8. Ship Mode / Shipping Detection
    for c in cols:
        if any(k in c.lower() for k in ['ship', 'delivery', 'channel', 'status', 'speed']):
            mapping["ship_mode"] = c
            break

    return mapping

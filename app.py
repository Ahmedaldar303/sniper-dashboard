import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة الذكاء الاصطناعي - خيارات", layout="wide")
st.title("📊 لوحة تحكم اختيار العقود")

def options_selector_agent(df):
    # فلترة: الدلتا أكبر من الثيتا
    filtered_df = df[df['Delta'].abs() > df['Theta'].abs()].copy()
    
    # تجهيز الأعمدة
    filtered_df['التكلفة (أقصى خسارة)'] = filtered_df['Ask'] * 100
    filtered_df['صافي الربح'] = (filtered_df['Delta'].abs() * 100) - (filtered_df['Theta'].abs() * 100)
    filtered_df['السترايكات'] = filtered_df['Strike'].astype(str) + " " + filtered_df['Type']
    
    # اختيار الأعمدة والترتيب المالي تصاعدياً
    final_columns = ['التكلفة (أقصى خسارة)', 'صافي الربح', 'السترايكات', 'Delta', 'Theta']
    result_df = filtered_df[final_columns].sort_values(by='التكلفة (أقصى خسارة)', ascending=True)
    
    return result_df

# بيانات محاكاة مؤقتة
mock_data = {
    'Strike': [5000, 5010, 5020, 4990],
    'Type': ['Call', 'Call', 'Call', 'Put'],
    'Ask': [10.50, 5.20, 1.10, 8.50],
    'Delta': [0.60, 0.45, 0.15, -0.55],
    'Theta': [-0.10, -0.15, -0.25, -0.12]
}
df = pd.DataFrame(mock_data)

st.subheader("أفضل العقود المرشحة")
best_options = options_selector_agent(df)

# عرض الجدول
st.dataframe(best_options, use_container_width=True)

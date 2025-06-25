import streamlit as st
import pandas as pd
import requests
import re

st.title("Automomus Product Catalogue Cleaning System")
st.set_page_config(page_title="Product Dashboard", layout="wide")

# ----------------------- Session Initialization -----------------------
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if "failed_rows" not in st.session_state:
    st.session_state.failed_rows = []
if "save_results" not in st.session_state:
    st.session_state.save_results = []
if "view_df" not in st.session_state:
    st.session_state.view_df = None
if "product_details" not in st.session_state:
    st.session_state.product_details = None
if "delete_id" not in st.session_state:
    st.session_state.delete_id = ""
if "update_pid" not in st.session_state:
    st.session_state.update_pid = ""
if "_reset_delete" not in st.session_state:
    st.session_state._reset_delete = False
if "_reset_update" not in st.session_state:
    st.session_state._reset_update = False

# ------------------ Helper Functions ------------------
def clean_text_fields(product):
    for key in ["product_id", "name", "description", "category", "brand", "material", "color", "size"]:
        val = product.get(key)
        if isinstance(val, str):
            product[key] = re.sub(r"[\x00-\x1F\x7F]", " ", val).strip()
        else:
            product[key] = str(val or "")
    return product

def refresh_products():
    try:
        response = requests.get("http://localhost:8000/products")
        if response.status_code == 200:
            st.session_state.view_df = pd.DataFrame(response.json())
    except:
        st.error("Failed to refresh product list.")

# ----------------------- Tabs -----------------------
tab1, tab2, tab3 = st.tabs(["🧹 Clean & Save", "📦 View Products", "🔁 Update/Delete by ID"])

# ===================== Tab 1: Clean & Save =====================
with tab1:
    st.header("🧹 Clean Product File & Save to Database")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(df, use_container_width=True)

        if st.button("Clean File"):
            df = df.replace([pd.NA, pd.NaT, float('nan'), float('inf'), float('-inf')], None)
            raw_list = df.to_dict(orient="records")
            cleaned = []
            st.session_state.failed_rows = []
            for idx, product in enumerate(raw_list):
                product = clean_text_fields(product)
                try:
                    product["price"] = float(product.get("price") or 0.0)
                except ValueError:
                    product["price"] = 0.0
                try:
                    response = requests.post("http://localhost:8000/clean-product", json=product)
                    if response.status_code == 200:
                        cleaned.append(response.json()["clean_product"])
                    else:
                        st.session_state.failed_rows.append((idx + 1, product))
                        st.warning(f"Row {idx+1} failed: {response.text}")
                except Exception as e:
                    st.session_state.failed_rows.append((idx + 1, product))
                    st.error(f"Row {idx+1} error: {e}")
            if cleaned:
                st.session_state.cleaned_df = pd.DataFrame(cleaned)
    
    if st.session_state.cleaned_df is not None:
        st.subheader("Cleaned Data")
        st.dataframe(st.session_state.cleaned_df, use_container_width=True)
        csv = st.session_state.cleaned_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Cleaned CSV", csv, "cleaned_products.csv", "text/csv")

        if st.button("💾 Save cleaned products to DB"):
            save_logs = []
            for idx, row in st.session_state.cleaned_df.iterrows():
                try:
                    response = requests.post("http://localhost:8000/save-product", json=row.to_dict())
                    if response.status_code == 200:
                        save_logs.append(f"✅ Row {idx+1} saved.")
                    else:
                        save_logs.append(f"❌ Row {idx+1} failed: {response.text}")
                except Exception as e:
                    save_logs.append(f"❌ Row {idx+1} error: {e}")
            for log in save_logs:
                st.write(log)
            refresh_products()

# ===================== Tab 2: View Products =====================
with tab2:
    st.header("📦 View & Manage Products")

    # ✅ Refresh delete input field
    if st.session_state._reset_delete:
        st.session_state.delete_id = ""
        st.session_state._reset_delete = False

    if st.button("🔄 Load All Products"):
        refresh_products()

    if st.session_state.view_df is not None:
        df = st.session_state.view_df

        with st.expander("🔍 Filter Products"):
            name_filter = st.text_input("Name contains")
            brand_filter = st.text_input("Brand contains")
            category_filter = st.text_input("Category contains")
            if name_filter:
                df = df[df["name"].str.contains(name_filter, case=False, na=False)]
            if brand_filter:
                df = df[df["brand"].str.contains(brand_filter, case=False, na=False)]
            if category_filter:
                df = df[df["category"].str.contains(category_filter, case=False, na=False)]

        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Filtered Products", csv, "filtered_products.csv", "text/csv")

        st.subheader("🗑️ Delete a Product Inline")
        st.text_input("Enter Product ID to delete", key="delete_id")

        if st.button("Delete Product"):
            try:
                response = requests.delete(f"http://localhost:8000/product/{st.session_state.delete_id}")
                if response.status_code == 200:
                    st.success("Product deleted successfully.")
                    st.session_state._reset_delete = True  # Trigger field reset
                    refresh_products()
                    st.rerun()  # Force re-render
                else:
                    st.error(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# ===================== Tab 3: Update/Delete by ID =====================
with tab3:
    st.header("🔁 Get / Update / Delete Product by ID")

    # ✅ Reset update field
    if st.session_state._reset_update:
        st.session_state.update_pid = ""
        st.session_state.product_details = None
        st.session_state._reset_update = False

    st.text_input("Enter Product ID", key="update_pid")

    if st.button("🔍 Fetch Product"):
        try:
            response = requests.get(f"http://localhost:8000/product/{st.session_state.update_pid}")
            if response.status_code == 200:
                st.session_state.product_details = response.json()
                st.success("Product fetched.")
            else:
                st.error(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.product_details:
        prod = st.session_state.product_details
        st.subheader("✏️ Edit Product Details")
        prod["name"] = st.text_input("Name", prod["name"])
        prod["description"] = st.text_area("Description", prod["description"])
        prod["price"] = st.number_input("Price", value=float(prod["price"]))
        prod["category"] = st.text_input("Category", prod["category"])
        prod["brand"] = st.text_input("Brand", prod["brand"])
        prod["material"] = st.text_input("Material", prod["material"])
        prod["color"] = st.text_input("Color", prod["color"])
        prod["size"] = st.text_input("Size", prod["size"])

        if st.button("✅ Update Product"):
            try:
                response = requests.put(
                    f"http://localhost:8000/product/{prod['product_id']}",
                    json=prod,
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    st.success("Product updated successfully.")
                    st.session_state._reset_update = True
                    refresh_products()
                    st.rerun()
                else:
                    st.error(response.text)
            except Exception as e:
                st.error(f"Update failed: {e}")

        if st.button("🗑️ Delete This Product"):
            try:
                response = requests.delete(f"http://localhost:8000/product/{prod['product_id']}")
                if response.status_code == 200:
                    st.success("Product deleted.")
                    st.session_state._reset_update = True
                    refresh_products()
                    st.rerun()
                else:
                    st.error(response.text)
            except Exception as e:
                st.error(f"Delete failed: {e}")

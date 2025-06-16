
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap

st.set_page_config(page_title="Parent-Child Life Journey", layout="wide")
st.title("👪 Life Journey Chevron Chart: Parent & Children")

# Get parent info
parent_name = st.text_input("Parent's Name", "Rita Basu")
relationship = st.selectbox("Parent's Role", ["Mother", "Father"])
num_children = st.number_input("How many children?", min_value=1, max_value=5, value=2, step=1)

children_data = []
st.markdown("---")

# Input for each child
for i in range(num_children):
    st.subheader(f"Child {i+1} Details")
    child_name = st.text_input(f"Name of Child {i+1}", key=f"name_{i}")
    parent_age_at_birth = st.number_input(f"{parent_name}'s Age at {child_name}'s Birth", min_value=15, max_value=60, value=25, key=f"age_{i}")
    phase_input = st.text_area(
        f"Enter Life Phases for {child_name} (e.g. Together: 0-18)", 
        "Together: 0-18\nHostel: 18-22\nJob Outside Home: 22-26\nIn US: 26-40\nReunited: 40-60",
        key=f"phases_{i}"
    )
    children_data.append((child_name, parent_age_at_birth, phase_input))

# Color map for phase labels
colors = {
    "Together": "#4caf50",
    "Hostel": "#ff9800",
    "Job Outside Home": "#f44336",
    "In US": "#03a9f4",
    "Reunited": "#9c27b0"
}

if st.button("Generate Chevron Chart"):
    fig, ax = plt.subplots(figsize=(15, 3 + num_children))

    max_x = 0
    for idx, (child_name, parent_start_age, phases_text) in enumerate(children_data):
        y_offset = (num_children - idx - 1) * 1.5
        for line in phases_text.strip().split("\n"):
            try:
                label, range_str = line.split(":")
                label = label.strip()
                start, end = map(float, range_str.strip().split("-"))
                width = end - start
                xpos = start
                color = colors.get(label, "#9e9e9e")

                ax.add_patch(patches.FancyBboxPatch(
                    (xpos, y_offset), width, 0.6,
                    boxstyle="rarrow,pad=0.3",
                    linewidth=1,
                    facecolor=color,
                    edgecolor='black'
                ))

                wrapped_label = "\n".join(textwrap.wrap(label, width=15))
                ax.text(xpos + width / 2, y_offset + 0.3, wrapped_label,
                        ha='center', va='center', fontsize=8, color='white')

                max_x = max(max_x, xpos + width)
            except:
                continue

        ax.text(-1.5, y_offset + 0.3, f"{child_name} ({parent_name} age {parent_start_age})", fontsize=9, ha='right')

    # Build axis labels
    xticks = list(range(0, int(max_x) + 5, 5))
    tick_labels = []
    for x in xticks:
        label = f"{x}\n{parent_name}: {x + int(children_data[0][1])}"
        tick_labels.append(label)

    ax.set_xticks(xticks)
    ax.set_xticklabels(tick_labels)
    ax.set_ylim(-0.5, num_children * 1.5)
    ax.set_yticks([])
    ax.set_xlim(0, max_x + 2)
    ax.set_xlabel("Child's Age  |  Parent's Age")
    ax.set_title(f"Life Journey of {parent_name} ({relationship}) with Children")

    st.pyplot(fig)
    st.success("Chart generated! Right-click on the image to save or take a screenshot.")

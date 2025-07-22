import streamlit as st
import random
from math import gcd

st.set_page_config(page_title="GCD Subtraction Practice", layout="centered")
st.title("➖ GCD Practice (Euclidean Subtraction Method)")

# Sidebar with QR code
st.sidebar.header("Scan This QR Code to View Menu Online")

qr_link = "https://thai-tanic.streamlit.app"  # Replace with your actual URL
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)

st.sidebar.image(buf, width=300, caption=qr_link)

def generate_reasonable_pairs(n=5):
    pairs = []
    while len(pairs) < n:
        a = random.randint(20, 60)
        b = random.randint(10, a - 1)
        if gcd(a, b) <= 1:
            continue  # Skip if GCD is 1 (too many steps)

        # Estimate subtraction steps
        big, small = a, b
        steps = 0
        while big != small:
            if big > small:
                big -= small
            else:
                small -= big
            steps += 1
            if steps > 5:
                break  # Too many steps, skip
        else:
            pairs.append((a, b))  # Accept only if <= 5 steps
    return pairs

# Initialize session state
if "problems" not in st.session_state:
    st.session_state.problems = generate_reasonable_pairs(5)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.a = None
    st.session_state.b = None
    st.session_state.steps = []
    st.session_state.final_step_done = False
    st.session_state.gcd_checked = False
    st.session_state.gcd_correct = False

def reset_problem():
    if st.session_state.index >= len(st.session_state.problems):
        return  # Prevent crash
    a, b = st.session_state.problems[st.session_state.index]
    st.session_state.a = a
    st.session_state.b = b
    st.session_state.steps = []
    st.session_state.final_step_done = False
    st.session_state.gcd_checked = False
    st.session_state.gcd_correct = False
    
def full_reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# End of problems
if st.session_state.index >= 5:
    st.success(f"🎉 All done! Final score: {st.session_state.score} / 5")
    if st.button("🔁 Restart"):
        full_reset()

else:
    # Start or resume problem
    if st.session_state.a is None or st.session_state.b is None:
        reset_problem()

    a = st.session_state.a
    b = st.session_state.b
    orig_a, orig_b = st.session_state.problems[st.session_state.index]

    st.markdown(f"### Problem {st.session_state.index + 1} of 5")
    st.markdown(f"Find the GCD of **{orig_a}** and **{orig_b}** using repeated subtraction.")

    # Show steps so far
    if st.session_state.steps:
        st.markdown("#### Steps so far:")
        for i, (x, y, result) in enumerate(st.session_state.steps, 1):
            st.markdown(f"{i}. **{x} − {y} = {result}**")

    # Final subtraction step when a == b but not yet subtracted to 0
    if a == b and not st.session_state.final_step_done:
        st.markdown("### Final Subtraction Step")

        col1, col2, col3, col4, col5 = st.columns([2, 0.2, 2, 0.2, 2])
        with col1:
            minuend = st.number_input("Minuend", key=f"final_min_{st.session_state.index}", value=a, step=1, label_visibility="collapsed")
        with col2:
            st.markdown("−")
        with col3:
            subtrahend = st.number_input("Subtrahend", key=f"final_sub_{st.session_state.index}", value=b, step=1, label_visibility="collapsed")
        with col4:
            st.markdown("=")
        with col5:
            result = st.number_input("Result", key=f"final_res_{st.session_state.index}", step=1, label_visibility="collapsed", value=0)

        if st.button("✅ Check Final Step", key=f"check_final_{st.session_state.index}"):
            if minuend == subtrahend == a and result == 0:
                st.success("✅ Correct final subtraction.")
                st.session_state.steps.append((minuend, subtrahend, result))
                st.session_state.final_step_done = True
                st.rerun()
            else:
                st.error("❌ Incorrect. Try again.")

    # After final subtraction, ask for GCD
    elif st.session_state.final_step_done:
        st.markdown("### Final Answer")

        guess = st.text_input("What is the GCD?", key=f"gcd_input_{st.session_state.index}")
        if st.button("Check GCD", key=f"check_gcd_{st.session_state.index}"):
            try:
                val = int(guess.strip())
                if val == a:
                    st.success("🎯 Correct! That's the GCD.")
                    st.session_state.score += 1
                    st.session_state.gcd_correct = True
                else:
                    st.error("❌ That's not correct.")
                st.session_state.gcd_checked = True
            except ValueError:
                st.error("❌ Please enter a valid number.")

        if st.session_state.gcd_checked and st.session_state.gcd_correct:
            if st.button("➡️ Next Problem"):
                st.session_state.index += 1
                reset_problem()
                st.rerun()

    # Standard subtraction step when a ≠ b
    elif a != b:
        col1, col2, col3, col4, col5 = st.columns([2, 0.2, 2, 0.2, 2])
        with col1:
            min_input = st.number_input("Minuend", key=f"min_{st.session_state.index}_{len(st.session_state.steps)}", label_visibility="collapsed", step=1)
        with col2:
            st.markdown("−")
        with col3:
            sub_input = st.number_input("Subtrahend", key=f"sub_{st.session_state.index}_{len(st.session_state.steps)}", label_visibility="collapsed", step=1)
        with col4:
            st.markdown("=")
        with col5:
            res_input = st.number_input("Result", key=f"res_{st.session_state.index}_{len(st.session_state.steps)}", label_visibility="collapsed", step=1)

        if st.button("✅ Check Step", key=f"check_step_{st.session_state.index}_{len(st.session_state.steps)}"):
            valid = {a, b}
            if {min_input, sub_input} != {a, b}:
                st.error("❌ Use only the current numbers.")
            elif min_input != max(a, b):
                st.error(f"❌ Minuend must be the larger number ({max(a, b)}).")
            elif sub_input != min(a, b):
                st.error(f"❌ Subtrahend must be the smaller number ({min(a, b)}).")
            elif res_input != min_input - sub_input:
                st.error("❌ Incorrect subtraction.")
            else:
                st.session_state.steps.append((min_input, sub_input, res_input))
                if min_input == a:
                    st.session_state.a = res_input
                else:
                    st.session_state.b = res_input
                st.rerun()
